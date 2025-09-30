"""Chainlit entry point for the multi-agent lab template.

Phase 3.2 established the baseline UI; Phase 3.3 wires in a simple
LangGraph workflow to demonstrate execution flow and error handling.
"""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List

import chainlit as cl
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage

from utils.logging import get_logger
from workflows.example_workflow import build_chat_workflow

UPLOADS_DIR = Path("outputs/uploads")
CHAT_WORKFLOW: Any = build_chat_workflow()
logger = get_logger(__name__)

SYSTEM_PROMPT = (
    "You are the friendly guide for a multi-agent lab template. "
    "Help students explore the project structure, explain how to extend the "
    "workflow, and offer practical tips when they ask questions."
)


def ensure_upload_dir() -> None:
    """Create the upload directory if it doesn't exist."""
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


@cl.on_chat_start
async def on_chat_start() -> None:
    """Initialize the session and greet the user."""
    ensure_upload_dir()
    cl.user_session.set("message_history", [])
    cl.user_session.set("llm_messages", [SystemMessage(content=SYSTEM_PROMPT)])

    await cl.Message(
        content=(
            "👋 Welcome to the multi-agent lab template!\n\n"
            "Send a message to try the OpenRouter-backed chat workflow. "
            "You can also upload files at any time; they will be stored "
            "for later workflow stages."
        )
    ).send()


def persist_uploaded_files(files: List[cl.File]) -> List[Path]:
    """Store uploaded files so later workflow phases can reuse them."""
    ensure_upload_dir()
    stored_paths: List[Path] = []

    for file in files:
        target_path = UPLOADS_DIR / file.name
        shutil.copy(file.path, target_path)
        stored_paths.append(target_path)

    return stored_paths


@cl.on_message
async def handle_message(message: cl.Message) -> None:
    """Run the LLM workflow, persist uploads, and track conversation history."""
    history: List[str] = cl.user_session.get("message_history", [])
    history.append(message.content)

    llm_messages: List[AnyMessage] = cl.user_session.get("llm_messages", [])
    if not llm_messages:
        llm_messages = [SystemMessage(content=SYSTEM_PROMPT)]

    attachment_note = ""
    stored_paths: List[Path] = []
    if message.elements:
        file_elements = [
            element for element in message.elements if isinstance(element, cl.File)
        ]
        if file_elements:
            stored_paths = persist_uploaded_files(file_elements)
            attachment_note = "📎 Stored files: " + ", ".join(
                path.name for path in stored_paths
            )

    try:
        conversation = [*llm_messages, HumanMessage(content=message.content)]
        result = await CHAT_WORKFLOW.ainvoke({"messages": conversation})
    except Exception as exc:  # noqa: BLE001 - surface workflow failures cleanly
        logger.exception("Chat workflow failed")
        await cl.Message(
            content=(
                "⚠️ Something went wrong while running the workflow. "
                "Check the server logs and try again."
            )
        ).send()
        return

    workflow_reply = result.get("response", "The workflow returned no response.")
    updated_messages = result.get("messages")
    if isinstance(updated_messages, list):
        cl.user_session.set("llm_messages", updated_messages)

    history.append(workflow_reply)
    cl.user_session.set("message_history", history)

    timestamp = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
    response_lines = [f"Workflow response ({timestamp}):", workflow_reply]
    if attachment_note:
        response_lines.extend(["", attachment_note])
    if notice := result.get("notice"):
        response_lines.extend(["", notice])

    await cl.Message(content="\n".join(response_lines)).send()
