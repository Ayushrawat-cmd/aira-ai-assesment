from pydantic import BaseModel, Field
from typing import Union, Optional


class Document(BaseModel):
    page_content: str = Field(description="Content of the document")
    metadata: dict = Field(description="Metadata associated with the document")

class RelevantDocsResSchema(BaseModel):
    documents: list[Document] = Field(description="List of relevant documents retrieved by the chatbot")


class ChatbotReqSchema(BaseModel):
    # chat_id: Optional[str] = Field(description="The chat id of the chatbot", default=None)
    query: str = Field(description="The query to be processed by the chatbot")
class ChatbotResSchema(BaseModel):
    event: str = Field(description="The event to be returned by the chatbot")
    data: Union[dict,str, list] = Field(description="The data to be returned by the chatbot")