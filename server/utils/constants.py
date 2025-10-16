from enum import Enum

MONGODB_URI  = "MONGODB_URI"
REDIS_HOST = "REDIS_HOST"
REDIS_PASSWORD = "REDIS_PASSWORD"
GPT_API_KEY = "GPT_API_KEY"
GPT_ORG_ID = "GPT_ORG_ID"

class ResStatus(Enum):
    SUCCESS = "success"
    FAIL = "fail"

VECTOR_DB_COLLECTION_NAME = "url_data"