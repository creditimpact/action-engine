import json
import logging
from typing import Any
from datetime import datetime
import contextvars
import uuid

# Context variable storing the current request ID
request_id_ctx_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_id",
    default=None,
)


def get_request_id() -> str | None:
    """Return the request ID for the current context if available."""
    return request_id_ctx_var.get()


class JsonFormatter(logging.Formatter):
    """Formatter that outputs logs as JSON strings."""

    def format(self, record: logging.LogRecord) -> str:  # pragma: no cover - simple formatting
        log_record = {
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "time": datetime.utcnow().isoformat(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "request_id") and record.request_id is not None:
            log_record["request_id"] = record.request_id
        return json.dumps(log_record)


def get_logger(name: str) -> logging.Logger:
    """Return a logger configured with :class:`JsonFormatter`."""

    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger


class RequestIdMiddleware:
    """Simple ASGI middleware that assigns a UUID request ID for each request."""

    def __init__(self, app: Any):
        self.app = app

    async def __call__(self, scope, receive, send):  # pragma: no cover - simple middleware
        if scope.get("type") == "http":
            token = request_id_ctx_var.set(str(uuid.uuid4()))
            try:
                await self.app(scope, receive, send)
            finally:
                request_id_ctx_var.reset(token)
        else:
            await self.app(scope, receive, send)
