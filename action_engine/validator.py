"""Request validation utilities."""

from typing import Any, Dict

from fastapi import HTTPException
from pydantic import BaseModel, ValidationError


class ActionRequest(BaseModel):
    """Incoming request model from the API layer."""

    action_type: str
    platform: str
    payload: Dict[str, Any]


def validate_request(data: Dict[str, Any]) -> ActionRequest:
    """Validate that the incoming data contains the required fields.

    Parameters
    ----------
    data: Dict[str, Any]
        Raw request data.

    Returns
    -------
    ActionRequest
        Parsed request model.

    Raises
    ------
    HTTPException
        If required fields are missing or parsing fails.
    """

    required_fields = ["action_type", "platform", "payload"]
    for field in required_fields:
        if field not in data or data[field] is None:
            raise HTTPException(status_code=422, detail=f"Missing required field: '{field}'")

    try:
        return ActionRequest(**data)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

