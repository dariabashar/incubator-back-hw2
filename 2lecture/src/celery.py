from celery import Celery
from .config import settings

app = Celery(
    "src",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["src.tasks.example"]
)

# Optional configuration
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

app.autodiscover_tasks(["src.tasks"])
