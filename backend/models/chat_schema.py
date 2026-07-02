from pydantic import BaseModel, ConfigDict


class ChatBase(BaseModel):

    session_id: str

    user_message: str

    ai_response: str


class ChatCreate(ChatBase):

    pass


class ChatResponse(ChatBase):

    chat_id: int

    model_config = ConfigDict(from_attributes=True)