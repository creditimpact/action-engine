"""Token refresh utilities."""
import time
from typing import Optional, Dict, Any

from .vault_storage import retrieve_token, store_token


async def refresh_if_needed(user_id: str, platform: str) -> Optional[Dict[str, Any]]:
    token = await retrieve_token(user_id, platform)
    if not token:
        return None

    expires_at = token.get("expires_at")
    if expires_at is None or time.time() < float(expires_at):
        return token

    refresh_token = token.get("refresh_token")
    if not refresh_token:
        return token

    new_data = {
        "access_token": f"refreshed-{refresh_token}",
        "refresh_token": refresh_token,
        "expires_at": time.time() + 3600,
        "scopes": token.get("scopes", []),
    }
    await store_token(user_id, platform, new_data)
    return new_data
