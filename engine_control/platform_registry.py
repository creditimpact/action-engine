from typing import Dict

_PLATFORM_STATUS: Dict[str, str] = {}


VALID_STATUSES = {"active", "maintenance", "deprecated"}


def set_platform_status(platform_name: str, status: str) -> None:
    """Set operational status for a platform."""
    if status not in VALID_STATUSES:
        raise ValueError("Invalid status")
    _PLATFORM_STATUS[platform_name] = status


def get_platform_status(platform_name: str) -> str:
    """Return status for platform, defaulting to 'active'."""
    return _PLATFORM_STATUS.get(platform_name, "active")


def clear_platforms() -> None:
    """Remove all platform statuses (mainly for tests)."""
    _PLATFORM_STATUS.clear()
