from fastapi import FastAPI
from fastapi.responses import JSONResponse
from action_engine.router import route_action
from action_engine.validator import ActionRequest

from action_engine.logging.logger import get_logger
from action_engine.auth import token_manager

app = FastAPI()
logger = get_logger(__name__)


@app.post("/perform_action")
async def perform_action(request: ActionRequest):
    logger.info("Received action request")
    response = await route_action(request.dict())
    logger.info("Action request completed")
    return response


@app.post("/auth/token")
async def save_token(data: dict):
    """Store an access token for a user/platform."""
    user_id = data.get("user_id")
    platform = data.get("platform")
    access_token = data.get("access_token")

    if not all(isinstance(v, str) for v in (user_id, platform, access_token)):
        detail = "Invalid token payload: 'user_id', 'platform' and 'access_token' are required"
        logger.info("Token validation error", extra={"user_id": user_id, "platform": platform})
        return JSONResponse(content={"error": detail}, status_code=400)

    token_manager.set_token(user_id, platform, access_token)
    logger.info("Token stored", extra={"user_id": user_id, "platform": platform})
    return JSONResponse(content={"status": "ok"})
