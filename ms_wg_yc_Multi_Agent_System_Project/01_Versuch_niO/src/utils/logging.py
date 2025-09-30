"""Centralised logging configuration for the template."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

LOG_DIR = Path("outputs/logs")
LOG_FILE = LOG_DIR / "app.log"
_CONFIGURED = False


def configure_logging(level: int = logging.INFO) -> None:
    """Initialise root logging handlers exactly once."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    handlers = [logging.StreamHandler(), logging.FileHandler(LOG_FILE, encoding="utf-8")]
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=handlers,
    )
    _CONFIGURED = True


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a module-specific logger after ensuring configuration."""
    configure_logging()
    return logging.getLogger(name)
