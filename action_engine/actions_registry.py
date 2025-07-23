"""Registry of supported actions for each platform."""

from typing import Dict, List

ACTIONS_REGISTRY: Dict[str, List[str]] = {
    "gmail": ["perform_action"],
    "google_calendar": ["create_event"],
    "notion": ["create_task"],
    "zapier": ["perform_action"],
}
