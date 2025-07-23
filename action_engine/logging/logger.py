import logging

# Module level logger for the action engine project
_logger = logging.getLogger("action_engine")

if not _logger.handlers:
    _handler = logging.StreamHandler()
    _formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    _handler.setFormatter(_formatter)
    _logger.addHandler(_handler)

_logger.setLevel(logging.INFO)


def get_logger() -> logging.Logger:
    """Return the configured logger for the action engine."""
    return _logger
