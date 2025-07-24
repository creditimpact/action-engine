# google_calendar_adapter.py
from action_engine.logging.logger import get_logger, get_request_id
from action_engine.auth import token_manager
from fastapi import HTTPException
from pydantic import BaseModel

logger = get_logger(__name__)


class CreateEventPayload(BaseModel):
    title: str


def _validate(payload: dict, model: type[BaseModel]) -> BaseModel:
    obj = model(**payload)
    for field in model.__annotations__:
        if getattr(obj, field, None) is None:
            raise HTTPException(status_code=422, detail=f"Missing field: {field}")
    return obj


async def create_event(user_id: str, payload: dict):
    """
    יוצר אירוע ביומן Google (מימוש ראשוני, דמיוני).
    """
    # תיעוד / הדמיה
    _validate(payload, CreateEventPayload)
    token = await token_manager.get_token(user_id, "google_calendar")
    if not token:
        logger.info(
            "Google Calendar token missing",
            extra={"user_id": user_id, "platform": "google_calendar", "request_id": get_request_id()},
        )
        return {"status": "error", "message": "Missing token for google_calendar"}

    logger.info(
        "Google Calendar create_event",
        extra={"payload": payload, "user_id": user_id, "request_id": get_request_id()},
    )

    # Placeholder for Google Calendar API integration
    # Example: await google_calendar_client.create_event(payload)

    # החזרה דמיונית
    return {
        "status": "success",
        "platform": "google_calendar",
        "message": "אירוע נוצר בהצלחה",
        "data": payload
    }
