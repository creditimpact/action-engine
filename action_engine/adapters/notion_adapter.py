import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from action_engine.logging.logger import get_logger

logger = get_logger(__name__)


async def create_task(payload):
    """Create a task in Notion (mocked)."""
    # Simulate interaction with Notion API
    logger.info("Notion create_task", extra={"payload": payload})

    # Placeholder for Notion API integration
    # Example: await notion_client.create_task(payload)
    return {
        "status": "success",
        "platform": "notion",
        "message": "משימה נוצרה בהצלחה",
        "data": payload,
    }
