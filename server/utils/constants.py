from enum import Enum

MONGODB_URI  = "MONGODB_URI"
REDIS_HOST = "REDIS_HOST"
REDIS_PASSWORD = "REDIS_PASSWORD"

class ResStatus(Enum):
    SUCCESS = "success"
    FAIL = "fail"