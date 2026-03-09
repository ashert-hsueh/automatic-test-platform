from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None
    role: UserRole = UserRole.INTERN


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ── Project ───────────────────────────────────────────────

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    description: Optional[str] = None
    base_url: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    base_url: Optional[str] = None


class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    base_url: Optional[str]
    owner_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Module ────────────────────────────────────────────────

class ModuleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    project_id: int


class ModuleOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    project_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── TestCase ──────────────────────────────────────────────

class TestCaseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    case_type: str = "api"
    priority: str = "P2"
    module_id: int
    request_config: Optional[dict] = None


class TestCaseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    request_config: Optional[dict] = None


class TestCaseOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    case_type: str
    priority: str
    module_id: int
    creator_id: int
    request_config: Optional[dict]
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Job & Report ──────────────────────────────────────────

class JobCreate(BaseModel):
    name: str
    project_id: int
    case_ids: list[int] = Field(..., min_length=1)


class JobOut(BaseModel):
    id: int
    name: str
    project_id: int
    creator_id: int
    celery_task_id: Optional[str]
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ReportOut(BaseModel):
    id: int
    job_id: int
    total: int
    passed: int
    failed: int
    skipped: int
    duration: float
    report_url: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
