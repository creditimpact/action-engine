"""In-memory store and helpers for registered engines."""

from __future__ import annotations

import secrets
from typing import Dict, List, Optional

_engine_store: Dict[str, Dict] = {}


def register_engine(
    engine_id: str, permissions: Dict, depends_on: Optional[List[str]] = None
) -> str:
    """Register an engine and return its generated secret token."""

    token = secrets.token_hex(16)
    _engine_store[engine_id] = {
        "token": token,
        "permissions": permissions or {},
        "depends_on": depends_on or [],
    }
    return token


def get_engine(engine_id: str) -> Optional[Dict]:
    """Return engine information if registered."""

    return _engine_store.get(engine_id)


def validate_engine(engine_id: str, token: str) -> bool:
    """Return ``True`` if ``token`` matches the stored engine token."""

    engine = _engine_store.get(engine_id)
    return bool(engine and engine.get("token") == token)


def list_engines() -> Dict[str, Dict]:
    """Return a copy of the registered engines."""

    return _engine_store.copy()


def clear_engines() -> None:
    """Remove all registered engines (mainly for tests)."""

    _engine_store.clear()
