import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from action_engine.logging.logger import get_logger

logger = get_logger(__name__)


async def perform_action(params):
    # כאן תבוא האינטגרציה האמיתית עם Gmail
    logger.info("Gmail perform_action invoked", extra={"params": params})
    return {"message": "בוצעה פעולה ב־Gmail", "params": params}


async def send_email(payload: dict) -> dict:
    """Send an email via Gmail.

    This function currently mocks the interaction with the Gmail API and
    simply echoes back the provided payload.
    """
    # Basic logging for action invocation
    logger.info("Gmail send_email", extra={"payload": payload})

    return {
        "status": "success",
        "platform": "gmail",
        "message": "Email sent successfully",
        "data": payload,
    }

