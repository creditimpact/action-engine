"""Asynchronous token storage utilities requiring Redis."""

from typing import Optional

from action_engine.config import REDIS_URL

try:
    import redis.asyncio as redis  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    redis = None  # type: ignore

_redis_client: Optional["redis.Redis"] = None


async def init_redis(client: "redis.Redis") -> None:
    """Inject a Redis client instance (used in tests)."""
    global _redis_client
    _redis_client = client


async def _get_redis() -> Optional["redis.Redis"]:
    """Return a Redis client or raise if unavailable."""
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    if not redis:
        raise RuntimeError("Redis package is not installed")
    try:  # pragma: no cover - actual connection may not exist in tests
        _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        await _redis_client.ping()
        return _redis_client
    except Exception as exc:
        _redis_client = None
        raise RuntimeError("Redis server unavailable") from exc


async def get_token(user_id: str, platform: str) -> Optional[str]:
    """Retrieve a stored token for ``user_id``/``platform``."""
    client = await _get_redis()
    return await client.get(f"{user_id}:{platform}")


async def set_token(user_id: str, platform: str, token: str) -> None:
    """Store the access token for ``user_id``/``platform``."""
    client = await _get_redis()
    await client.set(f"{user_id}:{platform}", token)
