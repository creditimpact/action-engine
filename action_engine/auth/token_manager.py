"""Asynchronous token storage utilities with Redis fallback."""

from typing import Dict, Optional

try:
    import redis.asyncio as redis  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    redis = None  # type: ignore

_redis_client: Optional["redis.Redis"] = None
_memory_store: Dict[str, Dict[str, str]] = {}


async def init_redis(client: "redis.Redis") -> None:
    """Inject a Redis client instance (used in tests)."""
    global _redis_client
    _redis_client = client


async def _get_redis() -> Optional["redis.Redis"]:
    """Return a Redis client if available and reachable."""
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    if not redis:
        return None
    try:  # pragma: no cover - actual connection may not exist in tests
        _redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
        await _redis_client.ping()
        return _redis_client
    except Exception:
        _redis_client = None
        return None


async def get_token(user_id: str, platform: str) -> Optional[str]:
    """Retrieve a stored token for ``user_id``/``platform``."""
    client = await _get_redis()
    if client:
        return await client.get(f"{user_id}:{platform}")
    return _memory_store.get(user_id, {}).get(platform)


async def set_token(user_id: str, platform: str, token: str) -> None:
    """Store the access token for ``user_id``/``platform``."""
    client = await _get_redis()
    if client:
        await client.set(f"{user_id}:{platform}", token)
    else:
        _memory_store.setdefault(user_id, {})[platform] = token
