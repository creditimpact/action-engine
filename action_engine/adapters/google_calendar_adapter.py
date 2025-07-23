# google_calendar_adapter.py
from action_engine.logging.logger import get_logger
from action_engine.auth.token_manager import get_token

logger = get_logger(__name__)


async def create_event(user_id: str, payload: dict):
    """
    יוצר אירוע ביומן Google (מימוש ראשוני, דמיוני).
    """
    # תיעוד / הדמיה
    token = get_token(user_id, "google_calendar")
    if not token:
        logger.info(
            "Google Calendar token missing",
            extra={"user_id": user_id, "platform": "google_calendar"},
        )
        return {"status": "error", "message": "Missing token for google_calendar"}

    logger.info(
        "Google Calendar create_event",
        extra={"payload": payload, "user_id": user_id},
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
