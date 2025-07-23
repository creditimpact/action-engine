import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from action_engine.logging.logger import get_logger, get_request_id
from auth.token_manager import get_token

logger = get_logger(__name__)


async def perform_action(user_id: str, params: dict):
    """Mock integration with Zapier Webhook / Trigger."""
    token = get_token(user_id, "zapier")
    if not token:
        logger.info(
            "Zapier token missing",
            extra={"user_id": user_id, "platform": "zapier", "request_id": get_request_id()},
        )
        return {"status": "error", "message": "Missing token for zapier"}

    logger.info(
        "Zapier perform_action",
        extra={"params": params, "user_id": user_id, "request_id": get_request_id()},
    )
    return {"message": "בוצעה פעולה דרך Zapier", "params": params}


async def trigger_zap(user_id: str, payload: dict) -> dict:
    """Trigger a Zap via webhook (mocked)."""
    token = get_token(user_id, "zapier")
    if not token:
        logger.info(
            "Zapier token missing",
            extra={"user_id": user_id, "platform": "zapier", "request_id": get_request_id()},
        )
        return {"status": "error", "message": "Missing token for zapier"}

    logger.info(
        "Zapier trigger_zap",
        extra={"payload": payload, "user_id": user_id, "request_id": get_request_id()},
    )

    # Placeholder for actual webhook call
    # Example: await zapier_client.trigger(payload)

    return {
        "status": "success",
        "platform": "zapier",
        "message": "Zap triggered successfully",
        "data": payload,
    }
