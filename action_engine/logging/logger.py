import json
import logging
from typing import Any


class JsonFormatter(logging.Formatter):
    """Formatter that outputs logs as JSON strings."""

    def format(self, record: logging.LogRecord) -> str:  # pragma: no cover - simple formatting
        log_record = {
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
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
