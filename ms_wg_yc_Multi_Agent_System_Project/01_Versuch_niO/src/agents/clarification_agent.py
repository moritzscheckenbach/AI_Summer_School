"""Clarification agent placeholder.

Students should implement logic that inspects user requests and produces
clarifying questions when details are missing.
"""

from __future__ import annotations

from typing import Any, Dict

from src.workflows.state import WorkflowState


class ClarificationAgent:
    """Analyze an incoming feature request and surface clarification prompts."""

    async def run(self, state: WorkflowState) -> Dict[str, Any]:
        """Return clarifying questions for the given input.

        Args:
            user_input: Raw text supplied by the user to the chat interface.
            context: Optional shared workflow information.
        """
        raise NotImplementedError("Students implement the clarification workflow")
