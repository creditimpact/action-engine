"""Global configuration utilities for Engine Control."""

from __future__ import annotations

from typing import Any, Dict

_GLOBAL_CONFIG: Dict[str, Any] = {
    "api_version": "1.0",
    "feature_flags": {},
}


def get_global_config() -> Dict[str, Any]:
    """Return a copy of the global configuration."""

    return dict(_GLOBAL_CONFIG)


def set_global_config(data: Dict[str, Any]) -> None:
    """Merge ``data`` into the current global configuration."""

    _GLOBAL_CONFIG.update(data)


def clear_global_config() -> None:
    """Reset the global configuration to defaults."""

    _GLOBAL_CONFIG.clear()
    _GLOBAL_CONFIG.update({"api_version": "1.0", "feature_flags": {}})
