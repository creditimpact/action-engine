"""Utilities for converting validated requests into internal models."""

from dataclasses import dataclass
from typing import Any, Dict

from validator import ActionRequest


@dataclass
class ActionModel:
    """Internal representation of an action to execute."""

    action_type: str
    platform: str
    user_id: str
    payload: Dict[str, Any]


def parse_request(request: ActionRequest) -> ActionModel:
    """Convert a validated ActionRequest into an ActionModel."""

    return ActionModel(
        action_type=request.action_type,
        platform=request.platform,
        user_id=request.user_id,
        payload=request.payload,
    )

