from enum import Enum

class IngestUrlStatus(Enum):
    PENDING = "PENDING"
    SCRAPPED = "SCRAPPED"
    FAILED = "FAILED"
    COMPLETED = "INGESTED"

    def __str__(self):
        return self.value
