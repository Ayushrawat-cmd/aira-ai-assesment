from typing import Optional, Literal
from pydantic import BaseModel,Field

class ConvoSaveReqSchema(BaseModel):
    chat_id : Optional[str] = Field(description="Chat id", default=None)
    user_id: Optional[str] = Field(description="User id", default=None)
    query: str = Field(description="user Query")
    str_response : Optional[str] = Field(description="Bot Response", default=None)
    json_response : Optional[dict|list[dict]] = Field(description="Bot Response in json format", default=None)
    graph_response : Optional[str] = Field(description="Bot Response to create the graph", default=None)
    ai_helper_dict: Optional[dict] = Field(description="It will help ai to generate the response", default=None)    

    
class chatSaveReqSchema(BaseModel):
    user_id: str = Field(description="User id")
    chat_label :Optional[str] = Field(description="Chat label", default= None)
    pinned: Optional[bool] = Field(default=False)
    status : Optional[str] = Field(default="active")
    conversation: ConvoSaveReqSchema = Field(description="Conversation save request")
