from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse

from .auth_middleware import verify_engine
from .engine_registry import register_engine
from .platform_registry import set_platform_status
from .permission_checker import is_action_allowed as check_action
from .engine_config import get_engine_config as fetch_config, set_engine_config
from .engine_logger import get_logger, RequestIdMiddleware, get_request_id

app = FastAPI()
app.add_middleware(RequestIdMiddleware)
logger = get_logger(__name__)


@app.post("/register_engine")
async def register_engine_endpoint(
    data: dict,
    x_engine_id: str = Header(None),
    x_engine_key: str = Header(None),
):
    verify_engine(x_engine_id, x_engine_key)
    engine_id = data.get("engine_id")
    permissions = data.get("permissions", {})
    depends_on = data.get("depends_on", [])
    if not isinstance(engine_id, str) or not engine_id:
        raise HTTPException(status_code=400, detail="Invalid engine_id")
    register_engine(engine_id, permissions, depends_on)
    logger.info(
        "Engine registered",
        extra={"engine_id": engine_id, "request_id": get_request_id()},
    )
    return JSONResponse({"status": "ok"})


@app.post("/set_platform_status")
async def set_platform_status_endpoint(
    data: dict,
    x_engine_id: str = Header(None),
    x_engine_key: str = Header(None),
):
    verify_engine(x_engine_id, x_engine_key)
    platform = data.get("platform")
    status = data.get("status")
    if not isinstance(platform, str) or status not in {"active", "maintenance", "deprecated"}:
        raise HTTPException(status_code=400, detail="Invalid platform status")
    set_platform_status(platform, status)
    logger.info(
        "Platform status updated",
        extra={"platform": platform, "status": status, "request_id": get_request_id()},
    )
    return JSONResponse({"status": "ok"})


@app.post("/set_engine_config")
async def set_engine_config_endpoint(
    data: dict,
    x_engine_id: str = Header(None),
    x_engine_key: str = Header(None),
):
    verify_engine(x_engine_id, x_engine_key)
    engine_id = data.get("engine_id")
    config = data.get("config", {})
    if not isinstance(engine_id, str) or not engine_id:
        raise HTTPException(status_code=400, detail="Invalid engine_id")
    set_engine_config(engine_id, config)
    return JSONResponse({"status": "ok"})


@app.get("/engine_config/{engine_id}")
async def engine_config_endpoint(
    engine_id: str,
    x_engine_id: str = Header(None),
    x_engine_key: str = Header(None),
):
    verify_engine(x_engine_id, x_engine_key)
    config = fetch_config(engine_id)
    return JSONResponse(config)


@app.post("/is_action_allowed")
async def is_action_allowed_endpoint(
    data: dict,
    x_engine_id: str = Header(None),
    x_engine_key: str = Header(None),
):
    verify_engine(x_engine_id, x_engine_key)
    engine_id = data.get("engine_id")
    platform = data.get("platform")
    action_type = data.get("action_type")
    if not all(isinstance(v, str) and v for v in (engine_id, platform, action_type)):
        raise HTTPException(status_code=400, detail="Invalid request")
    result = check_action(engine_id, platform, action_type)
    logger.info(
        "Authorization checked",
        extra={
            "engine_id": engine_id,
            "platform": platform,
            "request_id": get_request_id(),
        },
    )
    return JSONResponse(result)
