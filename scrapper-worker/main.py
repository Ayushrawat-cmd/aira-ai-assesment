from celery_config import celery_app
from utils.constants import IngestUrlStatus
from celery import signals
import requests
from bs4 import BeautifulSoup
from utils.mongodb_connection import init_mongo_connnection, get_mongo_client
from utils.constants import DATABASE_NAME, Collections
from datetime import datetime, timezone

def scrape_wikipedia(url: str) -> dict:
    """
    Scrapes the full content of a Wikipedia page using BeautifulSoup.
    Returns a dictionary with title, URL, and text content.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Get page title
    title_tag = soup.find(id="firstHeading")
    title = title_tag.get_text(strip=True) if title_tag else "No Title"
    
    # Get all paragraphs in the main content
    content_div = soup.find(id="bodyContent")
    paragraphs = content_div.find_all("p") if content_div else []
    full_text = "\n".join(p.get_text(strip=True) for p in paragraphs)
    
    return {
        "title": title,
        "url": url,
        "content": full_text
    }

@signals.worker_process_init.connect
def setup_connections(sender, **kwargs):
    init_mongo_connnection()
    print("MongoDB connection initialized in worker process.")

@celery_app.task(name="tasks.scraper_task")
def scraper_task(url, email):
    client = get_mongo_client()
    db = client[DATABASE_NAME]
    collection = db.get_collection(Collections.JOB_TRACKERS.value)
    try:
        print(f"Scraping URL: {url}, email: {email}")
        task_id = scraper_task.request.id
        data = f"this is data for {url}, email: {email}"
        # result = {"url": url, "status": IngestUrlStatus.SCRAPPED.value, "email": email}
        # redis_cache.set(task_id,json.dumps(result), ex=86400)
        scraped_content = scrape_wikipedia(url)
        collection.update_one(
            {"_id": task_id},
            {"$set": {"status": IngestUrlStatus.SCRAPPED.value,"updated_at": datetime.now(timezone.utc)}})
        celery_app.send_task("tasks.preprocess_task", args=[task_id, url, email, scraped_content])
        return {"url":url, "status": IngestUrlStatus.SCRAPPED.value, "email":email, "scraped_content":scraped_content}
    except Exception as e:
        print(e)
        try:
            collection.update_one(
                {"_id": task_id},
                {"$set": {"status": IngestUrlStatus.SCRAPPING_FAILED.value, "error": str(e), "updated_at": datetime.now(timezone.utc)}}
            )
        except Exception as me:
            print("Failed to update MongoDB with error:", me)
        return {"url":url, "status": IngestUrlStatus.SCRAPPING_FAILED.value, "email":email}
