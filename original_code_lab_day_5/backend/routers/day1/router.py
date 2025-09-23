from fastapi import APIRouter
from ...models import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/day1", tags=["day1"])


@router.post("/echo", response_model=ChatResponse)
def echo(request: ChatRequest) -> ChatResponse:
    return ChatResponse(reply=f"Echo (day 1): {request.message}")


@router.get("/health")
def health():
    return {"ok": True}