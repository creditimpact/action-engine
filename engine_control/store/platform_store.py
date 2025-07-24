"""In-memory store for platform status information."""

from __future__ import annotations

from typing import Dict

PLATFORMS: Dict[str, str] = {}


def clear() -> None:
    """Remove all stored platform information."""

    PLATFORMS.clear()
