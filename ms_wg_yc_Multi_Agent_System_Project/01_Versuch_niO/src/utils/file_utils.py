"""Utility helpers for working with the template's output files."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

OUTPUT_ROOT = Path("outputs")
SESSIONS_DIR = OUTPUT_ROOT / "sessions"
DOCUMENTS_DIR = OUTPUT_ROOT / "documents"


def ensure_directories() -> None:
    """Ensure the base output directories exist."""
    for path in (OUTPUT_ROOT, SESSIONS_DIR, DOCUMENTS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def get_session_dir(session_id: str) -> Path:
    """Return a directory for the given session, creating it if needed."""
    ensure_directories()
    safe_id = session_id.replace("/", "-") or "anonymous"
    session_path = SESSIONS_DIR / safe_id
    session_path.mkdir(parents=True, exist_ok=True)
    return session_path


def save_text(session_id: str, filename: str, content: str) -> Path:
    """Persist text content inside the session directory and return the path."""
    target_dir = get_session_dir(session_id)
    target_path = target_dir / filename
    target_path.write_text(content, encoding="utf-8")
    return target_path


def list_session_files(session_id: str) -> Iterable[Path]:
    """Yield all files previously stored for the session."""
    session_path = get_session_dir(session_id)
    return session_path.iterdir()
