from pydantic import BaseModel, Field,EmailStr   
from utils.constants import ResStatus

class IngestUrlReqSchema(BaseModel):
    url: str = Field(description="URL to be ingested")
    email: EmailStr = Field(description="Email of the user on which he want to get notified once ingested in system.")

class IngestUrlResSchema(BaseModel):
    req_status: ResStatus = Field(description="Status of the request", default=ResStatus.SUCCESS)
    task_id: str
