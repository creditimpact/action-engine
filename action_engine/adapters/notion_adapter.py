from action_engine.logging.logger import get_logger
from action_engine.auth.token_manager import get_token

logger = get_logger(__name__)


async def create_task(user_id: str, payload: dict):
    """Create a task in Notion (mocked)."""
    # Simulate interaction with Notion API
    token = get_token(user_id, "notion")
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
