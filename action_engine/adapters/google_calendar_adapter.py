# google_calendar_adapter.py
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from action_engine.logging.logger import get_logger, get_request_id
from auth.token_manager import get_token

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
