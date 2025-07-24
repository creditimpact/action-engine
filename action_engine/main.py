from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
import json
from action_engine.router import route_action
from action_engine.validator import ActionRequest
from action_engine.config import API_KEY

from action_engine.logging.logger import (
    get_logger,
    get_request_id,
    RequestIdMiddleware,
)
from action_engine.auth import token_manager
from action_engine.auth.oauth_client import OAuthClient

app = FastAPI()
app.add_middleware(RequestIdMiddleware)
logger = get_logger(__name__)


@app.post("/perform_action")
async def perform_action(request: ActionRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    request_id = get_request_id()
    logger.info("Received action request", extra={"request_id": request_id})
    response = await route_action(request.dict())
    logger.info("Action request completed", extra={"request_id": request_id})
    return response


@app.post("/auth/token")
async def save_token(data: dict, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
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

    await token_manager.set_token(user_id, platform, access_token)
    logger.info(
        "Token stored",
        extra={"user_id": user_id, "platform": platform, "request_id": get_request_id()},
    )
    return JSONResponse(content={"status": "ok"})


@app.post("/auth/start")
async def start_oauth(data: dict, x_api_key: str = Header(None)):
    """Initiate an OAuth authorization flow for a platform."""
    if x_api_key != API_KEY:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    user_id = data.get("user_id")
    platform = data.get("platform")
    client_id = data.get("client_id")
    client_secret = data.get("client_secret")
    redirect_uri = data.get("redirect_uri")
    scope = data.get("scope", "")

    if not all(
        isinstance(v, str) and v
        for v in (user_id, platform, client_id, client_secret, redirect_uri)
    ):
        detail = (
            "Invalid OAuth request: 'user_id', 'platform', 'client_id', "
            "'client_secret' and 'redirect_uri' are required"
        )
        logger.info(
            "OAuth initiation validation error",
            extra={"user_id": user_id, "platform": platform, "request_id": get_request_id()},
        )
        return JSONResponse(content={"error": detail}, status_code=400)

    oauth_client = OAuthClient(client_id, client_secret, redirect_uri)
    auth_url = await oauth_client.initiate_authorization(scope)
    logger.info(
        "OAuth flow started",
        extra={"user_id": user_id, "platform": platform, "request_id": get_request_id()},
    )
    return JSONResponse(content={"authorization_url": auth_url})


@app.post("/auth/callback")
async def oauth_callback(data: dict, x_api_key: str = Header(None)):
    """Handle OAuth callback and store tokens."""
    if x_api_key != API_KEY:
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
        json.dumps(
            {
                "access_token": token_data.get("access_token"),
                "refresh_token": token_data.get("refresh_token"),
                "expires_in": token_data.get("expires_in"),
            }
        ),
    )
    logger.info(
        "OAuth token stored",
        extra={"user_id": user_id, "platform": platform, "request_id": get_request_id()},
    )
    return JSONResponse(content={"status": "ok"})
