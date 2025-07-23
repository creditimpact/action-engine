from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
from router import route_action
from validator import ActionRequest

import sys
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from action_engine.logging.logger import get_logger
from auth import token_manager

app = FastAPI()
logger = get_logger(__name__)

API_KEY = os.getenv("API_KEY")


def verify_api_key(x_api_key: str | None) -> None:
    """Validate the provided ``X-API-Key`` header."""
    if API_KEY and x_api_key != API_KEY:
        logger.info("Invalid API key", extra={"provided": x_api_key})
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.post("/perform_action")
async def perform_action(request: ActionRequest, x_api_key: str = Header(None)):
    try:
        verify_api_key(x_api_key)
    except HTTPException as exc:
        return JSONResponse(content={"error": exc.detail}, status_code=exc.status_code)
    logger.info("Received action request")
    response = await route_action(request.dict())
    logger.info("Action request completed")
    return response


@app.post("/auth/token")
async def save_token(data: dict, x_api_key: str = Header(None)):
    """Store an access token for a user/platform."""
    try:
        verify_api_key(x_api_key)
    except HTTPException as exc:
        return JSONResponse(content={"error": exc.detail}, status_code=exc.status_code)
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
