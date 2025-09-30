"""Utilities for configuring LLM providers used by the template."""

from .openrouter import build_openrouter_chat_model, DEFAULT_OPENROUTER_MODEL

__all__ = ["build_openrouter_chat_model", "DEFAULT_OPENROUTER_MODEL"]
