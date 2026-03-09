import enum
from datetime import datetime, timezone
from sqlalchemy import String, Integer, ForeignKey, Text, DateTime, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class CaseType(str, enum.Enum):
    API = "api"           # 接口测试
    UI = "ui"             # UI 自动化
    PERF = "perf"         # 性能测试


class CasePriority(str, enum.Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class TestCase(Base):
    __tablename__ = "testcases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    case_type: Mapped[CaseType] = mapped_column(Enum(CaseType), default=CaseType.API)
    priority: Mapped[CasePriority] = mapped_column(Enum(CasePriority), default=CasePriority.P2)
    module_id: Mapped[int] = mapped_column(Integer, ForeignKey("modules.id"), nullable=False)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    # 接口测试配置（JSON存储）
    request_config: Mapped[dict] = mapped_column(
        JSON, nullable=True,
        comment="接口请求配置：method/url/headers/params/body/assertions"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # 关联
    module: Mapped["Module"] = relationship("Module", back_populates="testcases")  # noqa: F821
    steps: Mapped[list["TestStep"]] = relationship(
        "TestStep", back_populates="testcase", cascade="all, delete-orphan", order_by="TestStep.order"
    )


class TestStep(Base):
    __tablename__ = "test_steps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    testcase_id: Mapped[int] = mapped_column(Integer, ForeignKey("testcases.id"), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    action: Mapped[dict] = mapped_column(JSON, nullable=True, comment="步骤动作配置")
    expected: Mapped[dict] = mapped_column(JSON, nullable=True, comment="预期结果/断言")
    extract: Mapped[dict] = mapped_column(JSON, nullable=True, comment="变量提取规则")

    # 关联
    testcase: Mapped["TestCase"] = relationship("TestCase", back_populates="steps")
