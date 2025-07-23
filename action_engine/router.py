from fastapi.responses import JSONResponse

from action_engine.logging.logger import get_logger

# ייבוא אדפטרים
from adapters import (
    gmail_adapter,
    google_calendar_adapter,
    notion_adapter,
    zapier_adapter,
)

# מילון שמתאים בין פלטפורמות למודולים
adapter_registry = {
    "gmail": gmail_adapter,
    "google_calendar": google_calendar_adapter,
    "notion": notion_adapter,
    "zapier": zapier_adapter,
}

logger = get_logger()


async def route_action(data):
    platform = data.get("platform")
    action_type = data.get("action_type")
    payload = data.get("payload", {})

    if platform == "test":
        logger.info("Health check action received")
        return JSONResponse(content={"message": "המערכת עובדת 🎯"})

    if not platform or platform not in adapter_registry:
        return JSONResponse(
            content={"error": f"פלטפורמה לא תקינה או לא נתמכת: '{platform}'"},
            status_code=400
        )

    logger.info("Routing action '%s' for platform '%s'", action_type, platform)
    adapter_module = adapter_registry[platform]

    # מנסה למצוא את הפונקציה המתאימה לפעולה
    action_func = getattr(adapter_module, action_type, None)

    if not action_func:
        logger.warning("Action '%s' not found in adapter '%s'", action_type, platform)
        return JSONResponse(
            content={"error": f"הפעולה '{action_type}' לא קיימת באדפטר '{platform}'"},
            status_code=400
        )

    try:
        logger.info("Executing action '%s' on platform '%s'", action_type, platform)
        result = await action_func(payload)
        logger.info("Action '%s' on platform '%s' completed", action_type, platform)
        return JSONResponse(content={"status": "success", "result": result})
    except Exception as e:
        logger.exception("Error executing action '%s' on platform '%s'", action_type, platform)
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
