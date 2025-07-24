from action_engine.logging.logger import get_logger, get_request_id
from action_engine.auth import token_manager
from fastapi import HTTPException
from pydantic import BaseModel

logger = get_logger(__name__)


class GmailPerformActionPayload(BaseModel):
    key: str


class GmailSendEmailPayload(BaseModel):
    to: str


def _validate(payload: dict, model: type[BaseModel]) -> BaseModel:
    try:
        obj = model(**payload)
    except Exception as exc:  # pragma: no cover - simple validation
        raise HTTPException(status_code=422, detail=str(exc))
    for field in model.__annotations__:
        if getattr(obj, field, None) is None:
            raise HTTPException(status_code=422, detail=f"Missing field: {field}")
    return obj


async def perform_action(user_id: str, params: dict):
    """Mock action execution for Gmail."""
    _validate(params, GmailPerformActionPayload)
    token = await token_manager.get_access_token(user_id, "gmail")
    if not token:
        logger.info(
            "Gmail token missing",
            extra={"user_id": user_id, "platform": "gmail", "request_id": get_request_id()},
        )
        return {"status": "error", "message": "Missing token for gmail"}

    logger.info(
        "Gmail perform_action invoked",
        extra={"params": params, "user_id": user_id, "request_id": get_request_id()},
    )
    return {"message": "בוצעה פעולה ב־Gmail", "params": params}


async def send_email(user_id: str, payload: dict) -> dict:
    """Send an email via Gmail.

    This function currently mocks the interaction with the Gmail API and
    simply echoes back the provided payload.
    """
    _validate(payload, GmailSendEmailPayload)
    # Basic logging for action invocation
    token = await token_manager.get_access_token(user_id, "gmail")
    if not token:
        logger.info(
            "Gmail token missing",
            extra={"user_id": user_id, "platform": "gmail", "request_id": get_request_id()},
        )
        return {"status": "error", "message": "Missing token for gmail"}

    logger.info(
        "Gmail send_email",
        extra={"payload": payload, "user_id": user_id, "request_id": get_request_id()},
    )

    return {
        "status": "success",
        "platform": "gmail",
        "message": "Email sent successfully",
        "data": payload,
    }

