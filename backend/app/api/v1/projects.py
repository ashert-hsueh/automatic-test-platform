from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.project import Project, Module
from app.schemas import ProjectCreate, ProjectUpdate, ProjectOut, ModuleCreate, ModuleOut

router = APIRouter(prefix="/projects", tags=["项目管理"])


# ─────────────── Project CRUD ──────────────────────────────


@router.get("", response_model=list[ProjectOut], summary="获取项目列表")
async def list_projects(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    result = await db.execute(select(Project).order_by(Project.created_at.desc()))
    return result.scalars().all()


@router.post("", response_model=ProjectOut, summary="创建项目")
async def create_project(
    payload: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    project = Project(**payload.model_dump(), owner_id=user_id)
    db.add(project)
    await db.flush()
    await db.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectOut, summary="获取项目详情")
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    return project


@router.put("/{project_id}", response_model=ProjectOut, summary="更新项目")
async def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    for k, v in payload.model_dump(exclude_none=True).items():
        setattr(project, k, v)
    await db.flush()
    await db.refresh(project)
    return project


@router.delete("/{project_id}", summary="删除项目")
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    await db.delete(project)
    return {"detail": "删除成功"}


# ─────────────── Module CRUD ───────────────────────────────


@router.get("/{project_id}/modules", response_model=list[ModuleOut], summary="获取模块列表")
async def list_modules(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    result = await db.execute(select(Module).where(Module.project_id == project_id))
    return result.scalars().all()


@router.post("/{project_id}/modules", response_model=ModuleOut, summary="创建模块")
async def create_module(
    project_id: int,
    payload: ModuleCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    module = Module(name=payload.name, description=payload.description, project_id=project_id)
    db.add(module)
    await db.flush()
    await db.refresh(module)
    return module
