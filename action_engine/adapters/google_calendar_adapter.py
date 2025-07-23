# google_calendar_adapter.py
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from action_engine.logging.logger import get_logger

logger = get_logger(__name__)


async def create_event(payload):
    """
    יוצר אירוע ביומן Google (מימוש ראשוני, דמיוני).
    """
    # תיעוד / הדמיה
    logger.info("Google Calendar create_event", extra={"payload": payload})

    # Placeholder for Google Calendar API integration
    # Example: await google_calendar_client.create_event(payload)

    # החזרה דמיונית
    return {
        "status": "success",
        "platform": "google_calendar",
        "message": "אירוע נוצר בהצלחה",
        "data": payload
    }
