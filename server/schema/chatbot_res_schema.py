from pydantic import BaseModel, Field
from typing import Union

class ChatbotResSchema(BaseModel):
    event: str = Field(description="The event to be returned by the chatbot")
    data: Union[dict,str, list] = Field(description="The data to be returned by the chatbot")