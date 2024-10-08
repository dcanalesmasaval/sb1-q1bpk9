from pydantic import BaseModel
from typing import Dict, Optional

class Message(BaseModel):
    role: str
    content: str

class Thread(BaseModel):
    id: str
    messages: list[Message] = []

class User(BaseModel):
    id: str
    assistant_id: str
    thread_id: Optional[str] = None

class AssistantResponse(BaseModel):
    message: str
    thread_id: str