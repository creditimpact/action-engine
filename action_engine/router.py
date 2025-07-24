from fastapi.responses import JSONResponse
from fastapi import HTTPException

from action_engine.logging.logger import get_logger, get_request_id

from action_engine.validator import validate_request
from action_engine.action_parser import parse_request

# ייבוא אדפטרים
from action_engine.actions_registry import (
    get_action_function,
    supported_actions,
)

logger = get_logger(__name__)


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

    if not platform or not list(supported_actions(platform)):
        logger.info("Unsupported platform", extra={"platform": platform, "request_id": request_id})
        return JSONResponse(
            content={"error": f"פלטפורמה לא תקינה או לא נתמכת: '{platform}'"},
            status_code=400
        )

    # מנסה למצוא את הפונקציה המתאימה לפעולה
    action_func = get_action_function(platform, action_type)

    if not action_func:
        logger.info(
            "Unknown action",
            extra={"action_type": action_type, "platform": platform, "request_id": request_id},
        )
        return JSONResponse(
            content={"error": f"הפעולה '{action_type}' לא קיימת באדפטר '{platform}'"},
            status_code=400
        )

    if action_type not in supported_actions(platform):
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
