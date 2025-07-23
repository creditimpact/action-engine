import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from action_engine.logging.logger import get_logger
from auth.token_manager import get_token

logger = get_logger(__name__)


async def create_task(user_id: str, payload: dict):
    """Create a task in Notion (mocked)."""
    # Simulate interaction with Notion API
    token = await get_token(user_id, "notion")
    if not token:
        logger.info(
            "Notion token missing",
            extra={"user_id": user_id, "platform": "notion"},
        )
        return {"status": "error", "message": "Missing token for notion"}

    logger.info(
        "Notion create_task",
        extra={"payload": payload, "user_id": user_id},
    )

    # Placeholder for Notion API integration
    # Example: await notion_client.create_task(payload)
    return {
        "status": "success",
        "platform": "notion",
        "message": "משימה נוצרה בהצלחה",
        "data": payload,
    }
