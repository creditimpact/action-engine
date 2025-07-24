from fastapi import HTTPException
from pydantic import BaseModel

from action_engine.logging.logger import get_logger, get_request_id
from action_engine.adapters import BaseAdapter

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


class GmailAdapter(BaseAdapter):
    """Adapter for Gmail actions using the Gmail API."""

    SEND_API_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"

    def __init__(self) -> None:
        super().__init__("gmail")

    async def perform_action(self, user_id: str, params: dict):
        _validate(params, GmailPerformActionPayload)
        await self._get_token(user_id)
        logger.info(
            "Gmail perform_action invoked",
            extra={"params": params, "user_id": user_id, "request_id": get_request_id()},
        )
        return {"message": "בוצעה פעולה ב־Gmail", "params": params}

    async def send_email(self, user_id: str, payload: dict) -> dict:
        _validate(payload, GmailSendEmailPayload)
        token = await self._get_token(user_id)
        logger.info(
            "Gmail send_email",
            extra={"payload": payload, "user_id": user_id, "request_id": get_request_id()},
        )
        await self.post(
            self.SEND_API_URL,
            headers={"Authorization": f"Bearer {token}"},
            data=payload,
        )
        return {
            "status": "success",
            "platform": "gmail",
            "message": "Email sent successfully",
            "data": payload,
        }


adapter = GmailAdapter()

async def perform_action(user_id: str, params: dict):
    return await adapter.perform_action(user_id, params)

async def send_email(user_id: str, payload: dict) -> dict:
    return await adapter.send_email(user_id, payload)
