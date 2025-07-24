"""Async token storage using Redis with encryption."""
import json
import os
from typing import Optional, Dict, Any, List

try:
    import redis.asyncio as redis  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    redis = None  # type: ignore

_redis_client: Optional["redis.Redis"] = None

from .token_encryptor import encrypt, decrypt

REDIS_URL = os.getenv("VAULT_REDIS_URL", "redis://localhost:6379")


async def init_redis(client: "redis.Redis") -> None:
    global _redis_client
    _redis_client = client


async def _get_redis() -> "redis.Redis":
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    if not redis:
        raise RuntimeError("Redis package is not installed")
    try:  # pragma: no cover - network connection in real usage
        _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        await _redis_client.ping()
        return _redis_client
    except Exception as exc:  # pragma: no cover - outside tests
        _redis_client = None
        raise RuntimeError("Redis unavailable") from exc


async def store_token(user_id: str, platform: str, data: Dict[str, Any]) -> None:
    client = await _get_redis()
    encoded = encrypt(json.dumps(data))
    await client.set(f"{user_id}:{platform}", encoded)


async def retrieve_token(user_id: str, platform: str) -> Optional[Dict[str, Any]]:
    client = await _get_redis()
    raw = await client.get(f"{user_id}:{platform}")
    if raw is None:
        return None
    try:
        decrypted = decrypt(raw)
        return json.loads(decrypted)
    except Exception:  # pragma: no cover - bad data
        return None


async def list_platforms() -> List[str]:
    from pathlib import Path

    profiles = Path(__file__).resolve().parent / "platform_profiles"
    return [p.stem for p in profiles.glob("*.yaml")]
