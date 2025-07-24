"""Asynchronous token storage utilities requiring Redis."""

from typing import Optional, Dict, Any
import json
import time
import base64

from action_engine.config import REDIS_URL, ENCRYPTION_KEY

try:
    import redis.asyncio as redis  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    redis = None  # type: ignore

_redis_client: Optional["redis.Redis"] = None


def _xor(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def _encrypt(text: str) -> str:
    data = text.encode()
    key = ENCRYPTION_KEY.encode()
    return base64.urlsafe_b64encode(_xor(data, key)).decode()


def _decrypt(token: str) -> str:
    data = base64.urlsafe_b64decode(token.encode())
    key = ENCRYPTION_KEY.encode()
    return _xor(data, key).decode()


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


async def get_token(user_id: str, platform: str) -> Optional[Dict[str, Any]]:
    """Retrieve a stored token dictionary for ``user_id``/``platform``."""
    client = await _get_redis()
    raw = await client.get(f"{user_id}:{platform}")
    if raw is None:
        return None
    try:
        decrypted = _decrypt(raw)
        return json.loads(decrypted)
    except Exception:  # pragma: no cover - invalid json
        return None


async def set_token(user_id: str, platform: str, token_data: Dict[str, Any]) -> None:
    """Store token information for ``user_id``/``platform``."""
    client = await _get_redis()
    encoded = _encrypt(json.dumps(token_data))
    await client.set(f"{user_id}:{platform}", encoded)


def is_expired(token_data: Dict[str, Any]) -> bool:
    """Return ``True`` if the token has expired."""
    expires_at = token_data.get("expires_at")
    if expires_at is None:
        return False
    return time.time() >= float(expires_at)


async def refresh_if_needed(user_id: str, platform: str) -> Optional[Dict[str, Any]]:
    """Refresh the stored token using its ``refresh_token`` if expired."""
    token_data = await get_token(user_id, platform)
    if not token_data:
        return None
    if not is_expired(token_data):
        return token_data

    refresh_token_value = token_data.get("refresh_token")
    if not refresh_token_value:
        return token_data

    # Simulate token refresh. Real implementation would call provider API.
    new_data = {
        "access_token": f"refreshed-{refresh_token_value}",
        "refresh_token": refresh_token_value,
        "expires_at": time.time() + 3600,
    }
    await set_token(user_id, platform, new_data)
    return new_data


async def get_access_token(user_id: str, platform: str) -> Optional[str]:
    """Return a valid access token, refreshing if necessary."""
    token_data = await refresh_if_needed(user_id, platform)
    if not token_data:
        return None
    return token_data.get("access_token")
