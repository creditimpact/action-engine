"""Return connection status for platforms."""
import time
from typing import Dict

from .vault_storage import retrieve_token, list_platforms


async def get_status(user_id: str) -> Dict[str, str]:
    statuses: Dict[str, str] = {}
    platforms = await list_platforms()
    for platform in platforms:
        token = await retrieve_token(user_id, platform)
        if not token:
            statuses[platform] = "not_connected"
            continue
        expires_at = token.get("expires_at")
        if expires_at and time.time() >= float(expires_at):
            statuses[platform] = "token_expired"
        else:
            statuses[platform] = "active"
    return statuses
