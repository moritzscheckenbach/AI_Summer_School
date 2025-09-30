"""Shared state definitions for LangGraph workflows."""

from __future__ import annotations

from typing import NotRequired, TypedDict

from langchain_core.messages import AnyMessage
from typing_extensions import Annotated

from langgraph.graph.message import add_messages


class WorkflowState(TypedDict, total=False):
    """State passed between nodes in the core LangGraph workflows."""

    messages: Annotated[list[AnyMessage], add_messages]
    """Conversation history exchanged with the LLM component."""

    response: NotRequired[str]
    """Latest response text extracted for display in the Chainlit UI."""

    notice: NotRequired[str]
    """Optional diagnostic message surfaced to the user (e.g., fallbacks)."""
