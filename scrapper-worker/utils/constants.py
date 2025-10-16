from enum import Enum

class IngestUrlStatus(Enum):
    PENDING = "PENDING"
    SCRAPPED = "SCRAPPED"
    SCRAPPING_FAILED = "SCRAPPING_FAILED"
    COMPLETED = "INGESTED"

    def __str__(self):
        return self.value

MONGODB_URI = "MONGODB_URI"
DATABASE_NAME = "aira"
class Collections(str, Enum):
    JOB_TRACKERS = "job_trackers"
    PROCESSED_CHUNKS = "processed_chunks"