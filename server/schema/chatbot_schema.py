from pydantic import BaseModel, Field


class Document(BaseModel):
    page_content: str = Field(description="Content of the document")
    metadata: dict = Field(description="Metadata associated with the document")

class RelevantDocsResSchema(BaseModel):
    documents: list[Document] = Field(description="List of relevant documents retrieved by the chatbot")