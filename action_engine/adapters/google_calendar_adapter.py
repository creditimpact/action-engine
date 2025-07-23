# google_calendar_adapter.py

from action_engine.logging.logger import get_logger

logger = get_logger()


async def create_event(payload):
    """
    יוצר אירוע ביומן Google (מימוש ראשוני, דמיוני).
    """
    # תיעוד / הדמיה
    logger.info("[GOOGLE_CALENDAR] create_event called with payload: %s", payload)

    # החזרה דמיונית
    return {
        "status": "success",
        "platform": "google_calendar",
        "message": "אירוע נוצר בהצלחה",
        "data": payload
    }
