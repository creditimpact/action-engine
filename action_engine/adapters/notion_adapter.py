from action_engine.logging.logger import get_logger, get_request_id
from action_engine.auth import token_manager
from fastapi import HTTPException
from pydantic import BaseModel

logger = get_logger(__name__)


class CreateTaskPayload(BaseModel):
    title: str


def _validate(payload: dict, model: type[BaseModel]) -> BaseModel:
    obj = model(**payload)
    for field in model.__annotations__:
        if getattr(obj, field, None) is None:
            raise HTTPException(status_code=422, detail=f"Missing field: {field}")
    return obj


async def create_task(user_id: str, payload: dict):
    """Create a task in Notion (mocked)."""
    # Simulate interaction with Notion API
    _validate(payload, CreateTaskPayload)
    token = await token_manager.get_token(user_id, "notion")
    if not token:
        logger.info(
            "Notion token missing",
            extra={"user_id": user_id, "platform": "notion", "request_id": get_request_id()},
        )
        return {"status": "error", "message": "Missing token for notion"}

    logger.info(
        "Notion create_task",
        extra={"payload": payload, "user_id": user_id, "request_id": get_request_id()},
    )

    # Placeholder for Notion API integration
    # Example: await notion_client.create_task(payload)
    return {
        "status": "success",
        "platform": "notion",
        "message": "משימה נוצרה בהצלחה",
        "data": payload,
    }
