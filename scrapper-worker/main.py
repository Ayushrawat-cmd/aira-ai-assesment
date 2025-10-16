from celery_config import celery_app
from constants import IngestUrlStatus

@celery_app.task(name="tasks.scraper_task")
def scraper_task(url, email):
    try:
        print(f"Scraping URL: {url}, email: {email}")
        task_id = scraper_task.request.id
        data = f"this is data for {url}, email: {email}"
        celery_app.send_task("tasks.preprocess_task", args=[url, email, data], task_id=task_id)
        return {"url": url, "status": IngestUrlStatus.SCRAPPED.value, "email": email}
    except Exception as e:
        print(e)
        return {"url":url, "status": IngestUrlStatus.FAILED.value, "email":email}
