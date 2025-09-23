import os

from dotenv import load_dotenv
from fastapi import APIRouter
from openai import OpenAI

from ...models import ChatRequest, ChatResponse

load_dotenv()

router = APIRouter(prefix="/api/day1", tags=["day1"])

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


@router.post("/echo", response_model=ChatResponse)
def echo(request: ChatRequest) -> ChatResponse:
    return ChatResponse(reply=f"Echo (day 1): {request.message}")


@router.post("/film_critic", response_model=ChatResponse)
def film_critic(request: ChatRequest) -> ChatResponse:

    cutoff_date = "2023-01-01"
    prompt = f"""
    # Role
    - Your a well respected film critic with deep knowledge about the mentioned films
    - You stay formal with the regulatories and writing style of film critics
    # Context
    - Your knoledge is not unlimited and you only know films back to {cutoff_date}. You don't know any older film and politely decline giving a critic of a film you haven't seen.
    # Task
    Return a short and concise film critic of the mentioned film. Here is the input: {request.message}
    # Output format
    Write a short text between four and six sentences in the definded language. Any given answer should be in the language mentioned in the input. If no language is mentioned, answer in English."""

    completion = client.chat.completions.create(
        extra_body={},
        model="openai/gpt-oss-20b:free",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    print(completion.choices[0].message.content)

    return ChatResponse(reply=f"Film Critic (day 1): {completion.choices[0].message.content}")


@router.get("/health")
def health():
    return {"ok": True}
