from action_engine.logging.logger import get_logger

logger = get_logger()


async def create_task(payload):
    """Create a task in Notion (mocked)."""
    # Simulate interaction with Notion API
    logger.info("[NOTION] create_task called with payload: %s", payload)
    return {
        "status": "success",
        "platform": "notion",
        "message": "משימה נוצרה בהצלחה",
        "data": payload,
    }
