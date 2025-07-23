import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from action_engine.logging.logger import get_logger

logger = get_logger(__name__)


async def perform_action(params):
    # כאן תבוא האינטגרציה עם Zapier Webhook / Trigger
    logger.info("Zapier perform_action", extra={"params": params})
    return {"message": "בוצעה פעולה דרך Zapier", "params": params}


async def trigger_zap(payload: dict) -> dict:
    """Trigger a Zap via webhook (mocked)."""
    logger.info("Zapier trigger_zap", extra={"payload": payload})

    # Placeholder for actual webhook call
    # Example: await zapier_client.trigger(payload)

    return {
        "status": "success",
        "platform": "zapier",
        "message": "Zap triggered successfully",
        "data": payload,
    }
