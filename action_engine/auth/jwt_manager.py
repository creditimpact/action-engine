import time
import json
import base64
import hmac
import hashlib
from typing import Optional
from action_engine.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_SECONDS


def create_token(user_id: str) -> str:
    """Return a signed token for ``user_id``."""
    payload = {"user_id": user_id, "exp": int(time.time()) + ACCESS_TOKEN_EXPIRE_SECONDS}
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode()
    signature = hmac.new(SECRET_KEY.encode(), payload_bytes, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(payload_bytes + b"." + signature).decode()


def verify_token(token: str) -> Optional[str]:
    """Return the ``user_id`` if the token is valid and not expired."""
    try:
        decoded = base64.urlsafe_b64decode(token.encode())
        payload_bytes, signature = decoded.rsplit(b".", 1)
        expected = hmac.new(SECRET_KEY.encode(), payload_bytes, hashlib.sha256).digest()
        if not hmac.compare_digest(signature, expected):
            return None
        payload = json.loads(payload_bytes.decode())
        if payload.get("exp", 0) < time.time():
            return None
        return payload.get("user_id")
    except Exception:
        return None
