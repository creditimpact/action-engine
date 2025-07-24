"""Registry mapping platforms and actions to adapter callables."""

from __future__ import annotations

from typing import Callable, Dict, Iterable

from .adapters import (
    gmail_adapter,
    google_calendar_adapter,
    notion_adapter,
    zapier_adapter,
)


#: Nested mapping of ``platform -> action_type -> callable`` used by the router
ACTION_FUNCTIONS: Dict[str, Dict[str, Callable[..., object]]] = {
    "gmail": {
        "perform_action": gmail_adapter.perform_action,
        "send_email": gmail_adapter.send_email,
    },
    "google_calendar": {"create_event": google_calendar_adapter.create_event},
    "notion": {"create_task": notion_adapter.create_task},
    "zapier": {
        "perform_action": zapier_adapter.perform_action,
        "trigger_zap": zapier_adapter.trigger_zap,
    },
}


def get_action_function(platform: str, action_type: str) -> Callable[..., object] | None:
    """Return the adapter callable for ``platform``/``action_type`` if registered."""

    return ACTION_FUNCTIONS.get(platform, {}).get(action_type)


def supported_actions(platform: str) -> Iterable[str]:
    """Return an iterable of supported action types for ``platform``."""

    return ACTION_FUNCTIONS.get(platform, {}).keys()

