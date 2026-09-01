from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "voxnr",
    broker=settings.CELERY_BROKER_URL,
    include=[
        "app.tasks.dialogue_tasks",
    ],
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_ignore_result=True,
    broker_connection_retry_on_startup=True,
    worker_prefetch_multiplier=1,
)