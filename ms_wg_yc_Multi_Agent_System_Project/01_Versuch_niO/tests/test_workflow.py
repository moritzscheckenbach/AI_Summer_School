"""Tests for the example LangGraph workflow."""

from __future__ import annotations

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from src.workflows.example_workflow import build_chat_workflow


class _StubLLM:
    """Simple async stub that returns an AI message quoting the user."""

    async def ainvoke(self, messages):  # type: ignore[override]
        last_user = messages[-1].content if messages else ""
        return AIMessage(content=f"Stub model heard: {last_user}")


@pytest.mark.asyncio
async def test_chat_workflow_uses_supplied_llm():
    workflow = build_chat_workflow(llm=_StubLLM())
    result = await workflow.ainvoke({"messages": [HumanMessage(content="Testing")]})

    assert result["response"] == "Stub model heard: Testing"
    assert isinstance(result["messages"][-1], AIMessage)


@pytest.mark.asyncio
async def test_chat_workflow_falls_back_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    workflow = build_chat_workflow()
    result = await workflow.ainvoke({"messages": [HumanMessage(content="Hello")]})

    assert "Echo fallback" in result["response"]
    assert "OPENROUTER_API_KEY" in result["notice"]
