"""Simple Redis based token storage utilities.

Tokens are stored per ``user_id`` and ``platform`` so multiple users can be
served concurrently. The storage backend is configured via the ``REDIS_URL``
environment variable and defaults to ``redis://localhost:6379/0``.
"""

from typing import Optional
import os

try:  # pragma: no cover - real redis is optional in tests
    import redis.asyncio as redis  # type: ignore
except Exception:  # pragma: no cover - fall back to in-memory stub
    class _StubRedis:
        def __init__(self):
            self.store = {}

        async def hget(self, key: str, field: str):
            return self.store.get(key, {}).get(field)

        async def hset(self, key: str, mapping):
            self.store.setdefault(key, {}).update(mapping)

    class _RedisModule:
        def from_url(self, url, decode_responses=True):
            return _StubRedis()

    redis = _RedisModule()  # type: ignore


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)


async def get_token(user_id: str, platform: str) -> Optional[str]:
    """Retrieve a stored token for ``user_id``/``platform`` from Redis."""
    key = f"tokens:{user_id}"
    return await redis_client.hget(key, platform)


async def set_token(user_id: str, platform: str, token: str) -> None:
    """Store the access token for ``user_id``/``platform`` in Redis."""
    key = f"tokens:{user_id}"
    await redis_client.hset(key, {platform: token})

