from typing import Dict, List, Optional

_engine_store: Dict[str, Dict] = {}


def register_engine(engine_id: str, permissions: Dict, depends_on: Optional[List[str]] = None) -> None:
    """Register an engine with its permissions and dependencies."""
    _engine_store[engine_id] = {
        "permissions": permissions or {},
        "depends_on": depends_on or [],
    }


def get_engine(engine_id: str) -> Optional[Dict]:
    """Return engine information if registered."""
    return _engine_store.get(engine_id)


def clear_engines() -> None:
    """Remove all registered engines (mainly for tests)."""
    _engine_store.clear()
