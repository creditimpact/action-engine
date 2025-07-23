from fastapi import FastAPI
from router import route_action
from validator import ActionRequest

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from action_engine.logging.logger import get_logger

app = FastAPI()
logger = get_logger(__name__)


@app.post("/perform_action")
async def perform_action(request: ActionRequest):
    logger.info("Received action request")
    response = await route_action(request.dict())
    logger.info("Action request completed")
    return response
