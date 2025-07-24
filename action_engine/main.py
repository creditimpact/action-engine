from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
import json
from action_engine.router import route_action
from action_engine.validator import ActionRequest
from action_engine.auth.jwt_manager import create_token, verify_token

from action_engine.logging.logger import (
    get_logger,
    get_request_id,
    RequestIdMiddleware,
)
from action_engine.auth import token_manager
from action_engine.auth.oauth_client import OAuthClient
from action_engine import config

app = FastAPI()
app.add_middleware(RequestIdMiddleware)
logger = get_logger(__name__)


@app.post("/login")
async def login(data: dict):
    """Issue a token for ``user_id``."""
    user_id = data.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        return JSONResponse({"error": "Invalid user_id"}, status_code=400)
    token = create_token(user_id)
    return JSONResponse({"token": token})


def _get_user_id(authorization: str | None) -> str | None:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ", 1)[1]
    return verify_token(token)


def build_oauth_client(platform: str) -> OAuthClient:
    """Construct :class:`OAuthClient` based on configuration for ``platform``."""
    cfg = config.get_oauth_config(platform)
    if not all(cfg.get(k) for k in ("client_id", "client_secret", "redirect_uri")):
        raise HTTPException(status_code=500, detail="OAuth configuration missing")
    return OAuthClient(cfg["client_id"], cfg["client_secret"], cfg["redirect_uri"])


@app.post("/perform_action")
async def perform_action(
    request: ActionRequest, authorization: str = Header(None)
):
    user_id = _get_user_id(authorization)
    if user_id != request.user_id:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    request_id = get_request_id()
    logger.info("Received action request", extra={"request_id": request_id})
    response = await route_action(request.dict())
    logger.info("Action request completed", extra={"request_id": request_id})
    return response


@app.post("/auth/token")
async def save_token(data: dict, authorization: str = Header(None)):
    user_id_header = _get_user_id(authorization)
    if user_id_header != data.get("user_id"):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    """Store an access token for a user/platform."""
    user_id = data.get("user_id")
    platform = data.get("platform")
    access_token = data.get("access_token")

    if not all(isinstance(v, str) for v in (user_id, platform, access_token)):
        detail = "Invalid token payload: 'user_id', 'platform' and 'access_token' are required"
        logger.info(
            "Token validation error",
            extra={"user_id": user_id, "platform": platform, "request_id": get_request_id()},
        )
        return JSONResponse(content={"error": detail}, status_code=400)

    await token_manager.set_token(user_id, platform, {"access_token": access_token})
    logger.info(
        "Token stored",
        extra={"user_id": user_id, "platform": platform, "request_id": get_request_id()},
    )
    return JSONResponse(content={"status": "ok"})


@app.post("/auth/start")
async def start_oauth(data: dict, authorization: str = Header(None)):
    """Initiate an OAuth authorization flow for a platform."""
    user_id_header = _get_user_id(authorization)
    if user_id_header != data.get("user_id"):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    user_id = data.get("user_id")
    platform = data.get("platform")
    if not all(isinstance(v, str) and v for v in (user_id, platform)):
        detail = "Invalid OAuth request: 'user_id' and 'platform' are required"
        logger.info(
            "OAuth initiation validation error",
            extra={"user_id": user_id, "platform": platform, "request_id": get_request_id()},
        )
        return JSONResponse(content={"error": detail}, status_code=400)

    try:
        oauth_client = build_oauth_client(platform)
    except HTTPException as exc:
        return JSONResponse({"error": exc.detail}, status_code=exc.status_code)

    scope = config.get_oauth_config(platform).get("scope", "")
    auth_url = await oauth_client.initiate_authorization(scope)
    logger.info(
        "OAuth flow started",
        extra={"user_id": user_id, "platform": platform, "request_id": get_request_id()},
    )
    return JSONResponse(content={"authorization_url": auth_url})


@app.post("/auth/callback")
async def oauth_callback(data: dict, authorization: str = Header(None)):
    """Handle OAuth callback and store tokens."""
    user_id_header = _get_user_id(authorization)
    if user_id_header != data.get("user_id"):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    user_id = data.get("user_id")
    platform = data.get("platform")
    authorization_response = data.get("authorization_response")
    client_id = data.get("client_id")
    client_secret = data.get("client_secret")
    redirect_uri = data.get("redirect_uri")

    if not all(
        isinstance(v, str) and v
        for v in (
            user_id,
            platform,
            authorization_response,
            client_id,
            client_secret,
            redirect_uri,
        )
    ):
        detail = (
            "Invalid callback payload: 'user_id', 'platform', 'authorization_response', "
            "'client_id', 'client_secret' and 'redirect_uri' are required"
        )
        logger.info(
            "OAuth callback validation error",
            extra={"user_id": user_id, "platform": platform, "request_id": get_request_id()},
        )
        return JSONResponse(content={"error": detail}, status_code=400)

    oauth_client = OAuthClient(client_id, client_secret, redirect_uri)
    token_data = await oauth_client.fetch_token(authorization_response)

    await token_manager.set_token(
        user_id,
        platform,
        {
            "access_token": token_data.get("access_token"),
            "refresh_token": token_data.get("refresh_token"),
            "expires_in": token_data.get("expires_in"),
        },
    )
    logger.info(
        "OAuth token stored",
        extra={"user_id": user_id, "platform": platform, "request_id": get_request_id()},
    )
    return JSONResponse(content={"status": "ok"})
