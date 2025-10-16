from pymongo import MongoClient
from utils.db_connection import get_mongo_client
from utils.constants import DATABASE_NAME, Collections  
from utils.logger import Logger
from schema.ingest_url_schema import IngestUrlReqSchema
import datetime
from datetime import datetime, timezone
from fastapi import HTTPException  

logger = Logger.get_logger(__name__)    

class JobTrackerRepo:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JobTrackerRepo, cls).__new__(cls)
        return cls._instance
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.client = get_mongo_client()
            self.db = self.client[DATABASE_NAME]
            
        
    async def create_job(self, tracker_id, url ,email):
        logger.debug(f"{self.__class__.__name__} : create_job")
        self.collection =await self.db.create_collection(Collections.JOB_TRACKERS.value, check_exists=False)
        try:
            result = await self.collection.insert_one({"_id": tracker_id, "url": url, "email": email, "status": "PENDING", "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)})
            if result.acknowledged:
                logger.debug(f"{self.__class__.__name__}: create_job : Job created with id {tracker_id}")
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: create_job : {str(e)}")
            raise e
    
    async def get_job_status(self, tracker_id):
        logger.debug(f"{self.__class__.__name__} : get_job")
        self.collection =await self.db.create_collection(Collections.JOB_TRACKERS.value, check_exists=False)
        try:
            result = await self.collection.find_one({"_id": tracker_id})
            if result:
                return result                   
            else:
                raise HTTPException(status_code=400, detail={"message": "User creation failed", "error": "BAD_REQUEST"})
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: get_job : {str(e)}")
            raise e    
        

    