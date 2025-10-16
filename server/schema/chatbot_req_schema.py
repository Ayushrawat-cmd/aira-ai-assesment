from pydantic import BaseModel, Field
from typing import Literal  ,Optional

class ChatbotReqSchema(BaseModel):
    chat_id: Optional[str] = Field(description="The chat id of the chatbot", default=None)
    query: str = Field(description="The query to be processed by the chatbot")