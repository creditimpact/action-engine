"""Simple in-memory token storage utilities.

Tokens are stored per ``user_id`` and ``platform`` so multiple users can be
served concurrently.  This implementation is intentionally minimal and
non-persistent – a real deployment would use a database or external storage.
"""

from typing import Dict, Optional

# In-memory storage: ``{user_id: {platform: token}}``
_token_store: Dict[str, Dict[str, str]] = {}


def get_token(user_id: str, platform: str) -> Optional[str]:
    """Retrieve a stored token for ``user_id``/``platform``."""
    return _token_store.get(user_id, {}).get(platform)


def set_token(user_id: str, platform: str, token: str) -> None:
    """Store the access token for ``user_id``/``platform``."""
    _token_store.setdefault(user_id, {})[platform] = token

