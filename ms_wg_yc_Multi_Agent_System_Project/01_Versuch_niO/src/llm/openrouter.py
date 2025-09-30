"""Factory functions for OpenRouter-backed language models.

The template uses OpenRouter's OpenAI-compatible endpoint so students can
experiment with different models without changing the LangGraph workflow.
"""

from __future__ import annotations

import os
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
DEFAULT_OPENROUTER_MODEL = "deepseek/deepseek-chat-v3.1:free"


def _build_default_headers() -> Dict[str, str]:
    """Construct optional headers recommended by OpenRouter."""
    headers: Dict[str, str] = {}
    referer = os.getenv("OPENROUTER_APP_URL")
    if referer:
        headers["HTTP-Referer"] = referer
    app_name = os.getenv("OPENROUTER_APP_NAME")
    if app_name:
        headers["X-Title"] = app_name
    return headers


def build_openrouter_chat_model(
    model: str = DEFAULT_OPENROUTER_MODEL,
    **kwargs: Any,
) -> ChatOpenAI:
    """Return a ChatOpenAI instance configured for OpenRouter.

    Extra keyword arguments are forwarded to ``ChatOpenAI`` so students can
    override defaults (e.g., temperature, max tokens) if desired.
    """

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set. See `.env.example` for details.")

    headers = _build_default_headers()

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=OPENROUTER_API_BASE,
        default_headers=headers or None,
        **kwargs,
    )
