import asyncio
import os
from typing import AsyncIterator, List, Tuple

from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from openai import OpenAI

from ...models import ChatMessage, ChatSession

load_dotenv()

router = APIRouter(prefix="/api/day3", tags=["day3"])


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def _build_reply_text(messages: list[ChatMessage]) -> str:
    for msg in reversed(messages):
        if msg.role == "user":
            return f"Chat (day 3) streaming: {msg.content}"
    return "Chat (day 3) ready when you are."


async def _stream_reply(messages: list[ChatMessage]) -> AsyncIterator[str]:
    reply = _build_reply_text(messages)
    for token in reply.split():
        yield f"{token} "
        await asyncio.sleep(0)


@router.post("/chat")
async def chat(session: ChatSession) -> StreamingResponse:
    stream = _stream_reply(session.messages)
    return StreamingResponse(stream, media_type="text/plain")


@router.get("/health")
def health():
    return {"ok": True}
