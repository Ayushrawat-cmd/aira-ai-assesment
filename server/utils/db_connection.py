from pymongo import AsyncMongoClient
from .constants import MONGODB_URI, REDIS_HOST, REDIS_PASSWORD
from functools import wraps
from datetime import timedelta
import os
import redis
import json
from celery import Celery

async def init_celery_connection():
    global celery_app
    celery_app = Celery(
        "tasks",
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/1"
    )
    celery_app.conf.task_routes = {
        "tasks.scraper_task": {"queue": "scraper_queue"},
        "tasks.preprocess_task" : {"queue": "preprocess_queue"}
    }

def get_celery():
    return celery_app

async def init_mongo_connnection():
    
    global client 
    client =  AsyncMongoClient(os.environ.get(MONGODB_URI))
    await client.admin.command('ping')
    print("Connected to MongoDB")



def get_mongo_client():
    return client

async def close_mongo_connection():
    await client.close()

async def init_cache():
    global cache
    cache = redis.Redis(host=os.environ.get(REDIS_HOST), port=6379, db=0, password=os.environ.get(REDIS_PASSWORD), socket_keepalive=60000)

def get_cache()->redis.Redis:
    return cache

