from __future__ import annotations

import asyncio
import json
from typing import Any, Optional
from urllib import request, error

from fastapi import HTTPException

from action_engine.logging.logger import get_logger, get_request_id
from action_engine.auth import token_manager


class BaseAdapter:
    """Base adapter providing token handling and HTTP helpers."""

    def __init__(self, platform: str) -> None:
        self.platform = platform
        self.logger = get_logger(__name__)

    async def _get_token(self, user_id: str) -> str:
        token = await token_manager.get_access_token(user_id, self.platform)
        if not token:
            self.logger.info(
                f"{self.platform} token missing",
                extra={"user_id": user_id, "platform": self.platform, "request_id": get_request_id()},
            )
            raise HTTPException(status_code=400, detail=f"Missing token for {self.platform}")
        return token

    async def send_http_request(
        self,
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        data: Optional[Any] = None,
    ) -> Any:
        """Send an HTTP request asynchronously using urllib."""

        async def _do_request() -> Any:
            _headers = dict(headers or {})
            body = None
            if data is not None:
                if isinstance(data, (dict, list)):
                    body = json.dumps(data).encode()
                    _headers.setdefault("Content-Type", "application/json")
                elif isinstance(data, str):
                    body = data.encode()
                else:
                    body = data
            req = request.Request(url, data=body, headers=_headers, method=method)
            try:
                with request.urlopen(req) as resp:
                    resp_body = resp.read()
                    try:
                        return json.loads(resp_body)
                    except Exception:  # pragma: no cover - non JSON response
                        return resp_body.decode()
            except error.HTTPError as exc:
                raise HTTPException(status_code=exc.code, detail=exc.reason)
            except Exception as exc:  # pragma: no cover - network failure
                raise HTTPException(status_code=500, detail=str(exc))

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _do_request)

    async def post(
        self, url: str, headers: Optional[dict[str, str]] = None, data: Optional[Any] = None
    ) -> Any:
        return await self.send_http_request("POST", url, headers=headers, data=data)

__all__ = ["BaseAdapter"]
