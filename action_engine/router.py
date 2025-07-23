from fastapi.responses import JSONResponse

# ייבוא אדפטרים
from adapters import (
    gmail_adapter,
    google_calendar_adapter,
    notion_adapter,
    zapier_adapter,
)
from actions_registry import ACTIONS_REGISTRY

# מילון שמתאים בין פלטפורמות למודולים
adapter_registry = {
    "gmail": gmail_adapter,
    "google_calendar": google_calendar_adapter,
    "notion": notion_adapter,
    "zapier": zapier_adapter,
}

async def route_action(data):
    platform = data.get("platform")
    action_type = data.get("action_type")
    payload = data.get("payload", {})

    if platform == "test":
        return JSONResponse(content={"message": "המערכת עובדת 🎯"})

    if not platform or platform not in adapter_registry:
        return JSONResponse(
            content={"error": f"פלטפורמה לא תקינה או לא נתמכת: '{platform}'"},
            status_code=400
        )

    if action_type not in ACTIONS_REGISTRY.get(platform, []):
        return JSONResponse(
            content={"error": f"הפעולה '{action_type}' אינה נתמכת עבור הפלטפורמה '{platform}'"},
            status_code=400,
        )

    adapter_module = adapter_registry[platform]

    # מנסה למצוא את הפונקציה המתאימה לפעולה
    action_func = getattr(adapter_module, action_type, None)

    if not action_func:
        return JSONResponse(
            content={"error": f"הפעולה '{action_type}' לא קיימת באדפטר '{platform}'"},
            status_code=400
        )

    try:
        result = await action_func(payload)
        return JSONResponse(content={"status": "success", "result": result})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
