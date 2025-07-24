from fastapi.responses import JSONResponse
from fastapi import HTTPException

from action_engine.logging.logger import get_logger, get_request_id

from action_engine.validator import validate_request
from action_engine.action_parser import parse_request

# ייבוא אדפטרים
from action_engine.adapters import (
    gmail_adapter,
    google_calendar_adapter,
    notion_adapter,
    zapier_adapter,
)
from action_engine.actions_registry import ACTIONS_REGISTRY

logger = get_logger(__name__)

# מילון שמתאים בין פלטפורמות למודולים
adapter_registry = {
    "gmail": gmail_adapter,
    "google_calendar": google_calendar_adapter,
    "notion": notion_adapter,
    "zapier": zapier_adapter,
}

async def route_action(data):
    request_id = get_request_id()
    logger.info("Routing action", extra={"payload": data, "request_id": request_id})
    try:
        request_model = validate_request(data)
    except HTTPException as exc:
        logger.info("Validation error", extra={"error": exc.detail, "request_id": request_id})
        return JSONResponse(content={"error": exc.detail}, status_code=exc.status_code)

    action = parse_request(request_model)
    platform = action.platform
    action_type = action.action_type
    user_id = action.user_id
    payload = action.payload

    if platform == "test":
        return JSONResponse(content={"message": "המערכת עובדת 🎯"})

    if not platform or platform not in adapter_registry:
        logger.info("Unsupported platform", extra={"platform": platform, "request_id": request_id})
        return JSONResponse(
            content={"error": f"פלטפורמה לא תקינה או לא נתמכת: '{platform}'"},
            status_code=400
        )

    adapter_module = adapter_registry[platform]

    # מנסה למצוא את הפונקציה המתאימה לפעולה
    action_func = getattr(adapter_module, action_type, None)

    if not action_func:
        logger.info(
            "Unknown action",
            extra={"action_type": action_type, "platform": platform, "request_id": request_id},
        )
        return JSONResponse(
            content={"error": f"הפעולה '{action_type}' לא קיימת באדפטר '{platform}'"},
            status_code=400
        )

    if action_type not in ACTIONS_REGISTRY.get(platform, []):
        logger.info(
            "Action not supported",
            extra={"action_type": action_type, "platform": platform, "request_id": request_id},
        )
        return JSONResponse(
            content={"error": f"הפעולה '{action_type}' אינה נתמכת עבור הפלטפורמה '{platform}'"},
            status_code=400,
        )

    try:
        result = await action_func(user_id, payload)
        logger.info(
            "Adapter executed",
            extra={"platform": platform, "action_type": action_type, "request_id": request_id},
        )
        return JSONResponse(content={"status": "success", "result": result})
    except HTTPException as exc:
        logger.info("Execution error", extra={"error": exc.detail, "request_id": request_id})
        return JSONResponse(content={"error": exc.detail}, status_code=exc.status_code)
    except Exception as e:
        logger.info("Execution error", extra={"error": str(e), "request_id": request_id})
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
