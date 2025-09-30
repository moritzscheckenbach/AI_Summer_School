"""Integration-style tests for the Chainlit handlers.

These rely on Chainlit's testing utilities to simulate message events without
starting the full web server.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import chainlit as cl
import pytest

from src import main
from langchain_core.messages import AIMessage, HumanMessage


class _SimpleSession:
    """Minimal stand-in for chainlit.user_session during tests."""

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def get(self, key: str, default: Any | None = None) -> Any | None:
        return self._store.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value


@pytest.mark.asyncio
async def test_handle_message_runs_workflow(monkeypatch):
    """Ensure the chat workflow gets invoked and returns a response."""
    sent_messages: list[str] = []

    class DummyMessage:
        def __init__(self, content: str, elements: list[Any] | None = None) -> None:
            self.content = content
            self.elements = elements or []

    class DummyResponse:
        def __init__(self, content: str, elements: list[Any] | None = None) -> None:
            self.content = content
            self.elements = elements or []

        async def send(self) -> None:
            sent_messages.append(self.content)

    monkeypatch.setattr(main.cl, "Message", DummyResponse, raising=False)
    monkeypatch.setattr(main.cl, "user_session", _SimpleSession(), raising=False)

    workflow_mock = AsyncMock()
    workflow_mock.ainvoke.return_value = {
        "messages": [AIMessage(content="LLM response")],
        "response": "LLM response",
    }
    monkeypatch.setattr(main, "CHAT_WORKFLOW", workflow_mock)

    await main.handle_message(DummyMessage("Hello world"))

    workflow_mock.ainvoke.assert_awaited_once()
    call_args, _ = workflow_mock.ainvoke.await_args
    assert "messages" in call_args[0]
    assert isinstance(call_args[0]["messages"][-1], HumanMessage)
    assert call_args[0]["messages"][-1].content == "Hello world"
    assert any("LLM response" in msg for msg in sent_messages)


@pytest.mark.asyncio
async def test_handle_message_handles_errors(monkeypatch):
    """If the workflow raises, a friendly warning should be sent to the user."""
    sent_messages: list[str] = []

    class DummyMessage:
        def __init__(self, content: str, elements: list[Any] | None = None) -> None:
            self.content = content
            self.elements = elements or []

    class DummyResponse:
        def __init__(self, content: str, elements: list[Any] | None = None) -> None:
            self.content = content
            self.elements = elements or []

        async def send(self) -> None:
            sent_messages.append(self.content)

    monkeypatch.setattr(main.cl, "Message", DummyResponse, raising=False)
    monkeypatch.setattr(main.cl, "user_session", _SimpleSession(), raising=False)

    workflow_mock = AsyncMock()
    workflow_mock.ainvoke.side_effect = RuntimeError("failed")
    monkeypatch.setattr(main, "CHAT_WORKFLOW", workflow_mock)

    await main.handle_message(DummyMessage("boom"))

    assert any("Something went wrong" in msg for msg in sent_messages)
