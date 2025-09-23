from fastapi import APIRouter
from ...models import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/day2", tags=["day2"])


@router.post("/echo", response_model=ChatResponse)
def echo(request: ChatRequest) -> ChatResponse:
    return ChatResponse(reply=f"Echo (day 2): {request.message}")


@router.get("/health")
def health():
    return {"ok": True}