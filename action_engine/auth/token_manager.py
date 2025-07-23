"""Simple in-memory token storage utilities."""

from typing import Dict

# In-memory storage for tokens keyed by platform name
_token_store: Dict[str, str] = {}


def get_token(platform: str) -> str | None:
    """Retrieve a stored token for the given platform."""
    return _token_store.get(platform)


def set_token(platform: str, token: str) -> None:
    """Store the access token for the given platform."""
    _token_store[platform] = token

