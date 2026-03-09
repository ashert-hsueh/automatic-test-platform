from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.testcase import TestCase
from app.schemas import TestCaseCreate, TestCaseUpdate, TestCaseOut

router = APIRouter(prefix="/testcases", tags=["测试用例"])


@router.get("", response_model=list[TestCaseOut], summary="获取用例列表")
async def list_testcases(
    module_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    stmt = select(TestCase).order_by(TestCase.created_at.desc())
    if module_id:
        stmt = stmt.where(TestCase.module_id == module_id)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("", response_model=TestCaseOut, summary="创建测试用例")
async def create_testcase(
    payload: TestCaseCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    tc = TestCase(**payload.model_dump(), creator_id=user_id)
    db.add(tc)
    await db.flush()
    await db.refresh(tc)
    return tc


@router.get("/{case_id}", response_model=TestCaseOut, summary="获取用例详情")
async def get_testcase(
    case_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    result = await db.execute(select(TestCase).where(TestCase.id == case_id))
    tc = result.scalar_one_or_none()
    if not tc:
        raise HTTPException(status_code=404, detail="用例不存在")
    return tc


@router.put("/{case_id}", response_model=TestCaseOut, summary="更新测试用例")
async def update_testcase(
    case_id: int,
    payload: TestCaseUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    result = await db.execute(select(TestCase).where(TestCase.id == case_id))
    tc = result.scalar_one_or_none()
    if not tc:
        raise HTTPException(status_code=404, detail="用例不存在")
    for k, v in payload.model_dump(exclude_none=True).items():
        setattr(tc, k, v)
    await db.flush()
    await db.refresh(tc)
    return tc


@router.delete("/{case_id}", summary="删除测试用例")
async def delete_testcase(
    case_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    result = await db.execute(select(TestCase).where(TestCase.id == case_id))
    tc = result.scalar_one_or_none()
    if not tc:
        raise HTTPException(status_code=404, detail="用例不存在")
    await db.delete(tc)
    return {"detail": "删除成功"}
