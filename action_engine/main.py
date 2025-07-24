from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
from action_engine.router import route_action
from action_engine.validator import ActionRequest
from action_engine.config import API_KEY

from action_engine.logging.logger import (
    get_logger,
    get_request_id,
    RequestIdMiddleware,
)
from action_engine.auth import token_manager

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
