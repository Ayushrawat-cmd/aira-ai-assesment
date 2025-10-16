from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)
celery_app.conf.task_routes = {
    "tasks.scraper_task": {"queue": "scraper_queue"},
    "tasks.preprocess_task" : {"queue": "preprocess_queue"}
}
