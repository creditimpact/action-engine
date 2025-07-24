from typing import Dict, List
from .engine_registry import get_engine
from .platform_registry import get_platform_status


def is_action_allowed(engine_id: str, platform: str, action_type: str) -> Dict:
    """Return whether the action is permitted for the engine and platform."""
    engine = get_engine(engine_id)
    status = get_platform_status(platform)
    if not engine:
        return {"action_allowed": False, "required_scopes": [], "platform_status": status}
    if status != "active":
        return {"action_allowed": False, "required_scopes": [], "platform_status": status}
    permissions = engine.get("permissions", {})
    scopes: List[str] | None = None
    if platform in permissions:
        scopes = permissions[platform].get(action_type)
    allowed = scopes is not None
    return {
        "action_allowed": allowed,
        "required_scopes": scopes or [],
        "platform_status": status,
    }
