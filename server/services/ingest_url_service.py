from utils.db_connection import get_celery
from utils.logger import Logger
from uuid import uuid1
from schema.ingest_url_schema import IngestUrlResSchema
from repository.job_tracker_repo import JobTrackerRepo 

logger = Logger.get_logger(__name__)

class IngestUrlService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IngestUrlService, cls).__new__(cls)
        return cls._instance
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.celery = get_celery()
            self._initialized = True
            self.job_tracker_repo = JobTrackerRepo()
    

    async def ingest_url(self, url, email):
        logger.info(f"{self.__class__.__name__} : ingest_url :: {url}")
        try:
            task_id = str(uuid1())
            await self.job_tracker_repo.create_job(task_id, url,email)
            self.celery.send_task('tasks.scraper_task', args=[url, email], task_id=task_id)
            return IngestUrlResSchema(task_id=task_id)

        except Exception as e:
            logger.error(f"{self.__class__.__name__} : ingest_url : {str(e)}")
            raise e

    async def get_job_status(self, task_id):
        logger.info(f"{self.__class__.__name__} : get_job_status :: {task_id}")
        try:
            result = await self.job_tracker_repo.get_job_status(task_id)
            return result
        except Exception as e:
            logger.error(f"{self.__class__.__name__} : get_job_status : {str(e)}")
            raise e


