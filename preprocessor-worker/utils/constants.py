from enum import Enum

class IngestUrlStatus(Enum):
    PENDING = "PENDING"
    SCRAPPED = "SCRAPPED"
    PREPROCESSING_FAILED = "PREPROCESSING_FAILED"
    INGESTED = "INGESTED"

    def __str__(self):
        return self.value

VECTOR_DB_COLLECTION_NAME = "wiki_data"
MONGODB_URI = "MONGODB_URI"
DATABASE_NAME = "aira"
class Collections(str, Enum):
    JOB_TRACKERS = "job_trackers"
    PROCESSED_CHUNKS = "processed_chunks"