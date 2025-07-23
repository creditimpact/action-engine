from action_engine.logging.logger import get_logger
from action_engine.auth.token_manager import get_token

logger = get_logger(__name__)


async def perform_action(user_id: str, params: dict):
    """Mock action execution for Gmail."""
    token = get_token(user_id, "gmail")
    if not token:
        logger.info(
            "Gmail token missing",
            extra={"user_id": user_id, "platform": "gmail"},
        )
        return {"status": "error", "message": "Missing token for gmail"}

    logger.info(
        "Gmail perform_action invoked",
        extra={"params": params, "user_id": user_id},
    )
    return {"message": "בוצעה פעולה ב־Gmail", "params": params}


async def send_email(user_id: str, payload: dict) -> dict:
    """Send an email via Gmail.

    This function currently mocks the interaction with the Gmail API and
    simply echoes back the provided payload.
    """
    # Basic logging for action invocation
    token = get_token(user_id, "gmail")
    if not token:
        logger.info(
            "Gmail token missing",
            extra={"user_id": user_id, "platform": "gmail"},
        )
        return {"status": "error", "message": "Missing token for gmail"}

    logger.info(
        "Gmail send_email",
        extra={"payload": payload, "user_id": user_id},
    )

    return {
        "status": "success",
        "platform": "gmail",
        "message": "Email sent successfully",
        "data": payload,
    }

