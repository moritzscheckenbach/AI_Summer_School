from fastapi import APIRouter
from ...models import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/day4", tags=["day4"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(reply=f"Chat (day 4): {request.message}")


@router.get("/health")
def health():
    return {"ok": True}
