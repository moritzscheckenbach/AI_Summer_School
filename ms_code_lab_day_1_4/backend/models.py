from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User input text")


class ChatResponse(BaseModel):
    reply: str


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str = Field(..., min_length=1, description="Message content")


class ChatSession(BaseModel):
    messages: list[ChatMessage] = Field(
        default_factory=list,
        description="Ordered chat history exchanged between user and assistant",
    )
