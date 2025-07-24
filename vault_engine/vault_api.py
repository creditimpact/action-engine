from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
import time

from .auth_middleware import verify_engine
from .vault_storage import store_token, retrieve_token
from .token_refresher import refresh_if_needed
from .connection_checker import get_status
from .vault_logger import get_logger, RequestIdMiddleware, get_request_id

app = FastAPI()
app.add_middleware(RequestIdMiddleware)
logger = get_logger(__name__)


@app.post("/store_token")
async def store_token_endpoint(
    data: dict,
    x_engine_id: str = Header(None),
    x_engine_key: str = Header(None),
):
    verify_engine(x_engine_id, x_engine_key)
    user_id = data.get("user_id")
    platform = data.get("platform")

    token_payload = data.get("token", data)
    access_token = token_payload.get("access_token")
    refresh_token = token_payload.get("refresh_token")
    expires_at = token_payload.get("expires_at")
    expires_in = token_payload.get("expires_in")
    scopes = token_payload.get("scopes", [])

    if expires_at is None and expires_in is not None:
        try:
            expires_at = time.time() + float(expires_in)
        except Exception:
            expires_at = None

    if not all(isinstance(v, str) and v for v in (user_id, platform, access_token)):
        raise HTTPException(status_code=400, detail="Invalid token payload")

    token_data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_at": expires_at,
        "scopes": scopes,
    }
    await store_token(user_id, platform, token_data)
    logger.info(
        "Token stored",
        extra={"user_id": user_id, "platform": platform, "request_id": get_request_id()},
    )
    return JSONResponse({"status": "ok"})


@app.post("/get_token")
async def get_token_endpoint(
    user_id: str,
    platform: str,
    x_engine_id: str = Header(None),
    x_engine_key: str = Header(None),
):
    verify_engine(x_engine_id, x_engine_key)
    token = await refresh_if_needed(user_id, platform)
    if not token:
        return JSONResponse({"error": "Token not found"}, status_code=404)
    logger.info(
        "Token retrieved",
        extra={"user_id": user_id, "platform": platform, "request_id": get_request_id()},
    )
    return JSONResponse(token)


@app.post("/status")
async def status_endpoint(
    user_id: str,
    x_engine_id: str = Header(None),
    x_engine_key: str = Header(None),
):
    verify_engine(x_engine_id, x_engine_key)
    statuses = await get_status(user_id)
    logger.info(
        "Status retrieved",
        extra={"user_id": user_id, "request_id": get_request_id()},
    )
    connected_platforms = [
        {"platform": p, "status": s} for p, s in statuses.items()
    ]
    return JSONResponse({"connected_platforms": connected_platforms})
