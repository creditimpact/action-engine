from __future__ import annotations

import asyncio
import json
import urllib.error
import urllib.request

from fastapi import HTTPException

from action_engine.auth import token_manager
from action_engine.logging.logger import get_logger, get_request_id


class BaseAdapter:
    """Base class for platform adapters providing HTTP utilities."""

    platform: str = ""
    base_url: str = ""

    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)

    async def _get_token(self, user_id: str) -> str:
        token = await token_manager.get_token(user_id, self.platform)
        if not token:
            self.logger.info(
                "Token missing",
                extra={
                    "user_id": user_id,
                    "platform": self.platform,
                    "request_id": get_request_id(),
                },
            )
            raise HTTPException(status_code=401, detail=f"Missing token for {self.platform}")
        return token

    async def _request(
        self, method: str, url: str, token: str, data: dict | None = None
    ) -> dict:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        body = None
        if data is not None:
            body = json.dumps(data).encode()
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        loop = asyncio.get_event_loop()
        try:
            resp = await loop.run_in_executor(None, urllib.request.urlopen, req)
            resp_body = await loop.run_in_executor(None, resp.read)
            status = resp.getcode()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode()
            self.logger.info(
                "HTTP error",
                extra={
                    "status_code": exc.code,
                    "detail": detail,
                    "request_id": get_request_id(),
                },
            )
            raise HTTPException(status_code=exc.code, detail=detail)
        except Exception as exc:
            self.logger.info(
                "HTTP request failed",
                extra={"detail": str(exc), "request_id": get_request_id()},
            )
            raise HTTPException(status_code=502, detail=str(exc))

        if status >= 400:
            detail = resp_body.decode()
            self.logger.info(
                "HTTP error",
                extra={"status_code": status, "detail": detail, "request_id": get_request_id()},
            )
            raise HTTPException(status_code=status, detail=detail)

        if resp_body:
            try:
                return json.loads(resp_body.decode())
            except Exception:
                return {"raw": resp_body.decode()}
        return {}


from . import gmail_adapter, google_calendar_adapter, notion_adapter, zapier_adapter

__all__ = [
    "BaseAdapter",
    "gmail_adapter",
    "google_calendar_adapter",
    "notion_adapter",
    "zapier_adapter",
]
