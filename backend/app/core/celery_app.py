from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "autotest",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    # 任务结果保留 24 小时
    result_expires=86400,
    # 自动发现任务模块
    include=["app.tasks.test_runner"],
)
