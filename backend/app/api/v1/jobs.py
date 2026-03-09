import asyncio
import json
import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.core.config import settings
from app.models.report import TestJob, TestReport, JobStatus
from app.schemas import JobCreate, JobOut, ReportOut
from app.tasks.test_runner import run_test_job

router = APIRouter(prefix="/jobs", tags=["任务执行"])


@router.post("", response_model=JobOut, summary="创建并触发测试任务")
async def create_job(
    payload: JobCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    job = TestJob(name=payload.name, project_id=payload.project_id, creator_id=user_id)
    db.add(job)
    await db.flush()

    # 提交 Celery 异步任务
    task = run_test_job.delay(job.id, payload.case_ids)
    job.celery_task_id = task.id
    job.status = JobStatus.RUNNING

    await db.flush()
    await db.refresh(job)
    return job


@router.get("", response_model=list[JobOut], summary="获取任务列表")
async def list_jobs(
    project_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    stmt = select(TestJob).order_by(TestJob.created_at.desc())
    if project_id:
        stmt = stmt.where(TestJob.project_id == project_id)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{job_id}", response_model=JobOut, summary="获取任务详情")
async def get_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    result = await db.execute(select(TestJob).where(TestJob.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="任务不存在")
    return job


@router.get("/{job_id}/report", response_model=ReportOut, summary="获取任务报告")
async def get_report(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    result = await db.execute(select(TestReport).where(TestReport.job_id == job_id))
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="报告尚未生成")
    return report


# ─────────────── WebSocket 实时日志 ────────────────────────

@router.websocket("/ws/{task_id}")
async def websocket_log(websocket: WebSocket, task_id: str):
    """
    WebSocket 端点：订阅 Redis pub/sub 频道，实时推送执行日志
    连接方式：ws://host/api/v1/jobs/ws/{celery_task_id}
    """
    await websocket.accept()
    channel = f"task_log:{task_id}"
    redis_client = aioredis.Redis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
    )
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = message["data"]
                if isinstance(data, bytes):
                    data = data.decode("utf-8")
                await websocket.send_text(data)
                if data.startswith("[DONE]"):
                    break
    except WebSocketDisconnect:
        pass
    finally:
        await pubsub.unsubscribe(channel)
        await redis_client.aclose()
        await websocket.close()
