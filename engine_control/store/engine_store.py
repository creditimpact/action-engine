"""Lightweight in-memory store used by :mod:`engine_registry`."""

from __future__ import annotations

from typing import Dict

ENGINES: Dict[str, Dict] = {}


def clear() -> None:
    """Remove all stored engines (mainly for tests)."""

    ENGINES.clear()
