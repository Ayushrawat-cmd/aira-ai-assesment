from enum import Enum

class IngestUrlStatus(Enum):
    PENDING = "PENDING"
    SCRAPPED = "SCRAPPED"
    PREPROCESSING_FAILED = "PREPROCESSING_FAILED"
    INGESTED = "INGESTED"

    def __str__(self):
        return self.value
