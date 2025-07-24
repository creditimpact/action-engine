from action_engine.logging.logger import get_logger, get_request_id
from action_engine.auth import token_manager
from fastapi import HTTPException
from pydantic import BaseModel

logger = get_logger(__name__)


class PerformActionPayload(BaseModel):
    x: int


def _validate(payload: dict, model: type[BaseModel]) -> BaseModel:
    obj = model(**payload)
    for field in model.__annotations__:
        if getattr(obj, field, None) is None:
            raise HTTPException(status_code=422, detail=f"Missing field: {field}")
    return obj


async def perform_action(user_id: str, params: dict):
    """Mock integration with Zapier Webhook / Trigger."""
    _validate(params, PerformActionPayload)
    token = await token_manager.get_access_token(user_id, "zapier")
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
    _validate(payload, PerformActionPayload)
    token = await token_manager.get_access_token(user_id, "zapier")
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
