"""HTTP route handlers for Engine Control."""

from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse

from .auth_middleware import verify_engine
from .engine_registry import register_engine, validate_engine, get_engine
from .permission_checker import is_action_allowed
from .platform_registry import list_platforms
from .config import get_global_config
from .engine_logger import get_logger, get_request_id

router = APIRouter()
logger = get_logger(__name__)


@router.post("/engines/register")
async def register_engine_endpoint(
    data: dict,
    x_engine_id: str = Header(None),
    x_engine_key: str = Header(None),
):
    """Register a new engine and return its secret token."""

    verify_engine(x_engine_id, x_engine_key)
    engine_id = data.get("engine_id")
    permissions = data.get("permissions", {})
    depends_on = data.get("depends_on", [])
    if not isinstance(engine_id, str) or not engine_id:
        raise HTTPException(status_code=400, detail="Invalid engine_id")

    token = register_engine(engine_id, permissions, depends_on)
    logger.info(
        "Engine registered",
        extra={"engine_id": engine_id, "request_id": get_request_id()},
    )
    return JSONResponse({"engine_id": engine_id, "engine_key": token})


@router.post("/engines/validate")
async def validate_engine_endpoint(
    data: dict | None = None,
    x_engine_id: str = Header(None),
    x_engine_key: str = Header(None),
):
    """Validate provided engine credentials."""

    valid = validate_engine(x_engine_id or "", x_engine_key or "")
    if not valid:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    return JSONResponse({"valid": True})


@router.post("/actions/check")
async def actions_check_endpoint(
    data: dict,
    x_engine_id: str = Header(None),
    x_engine_key: str = Header(None),
):
    """Return whether an action is allowed for the engine."""

    verify_engine(x_engine_id, x_engine_key)
    engine_id = data.get("engine_id")
    platform = data.get("platform")
    action_type = data.get("action_type")
    if not all(isinstance(v, str) and v for v in (engine_id, platform, action_type)):
        raise HTTPException(status_code=400, detail="Invalid payload")

    result = is_action_allowed(engine_id, platform, action_type)
    logger.info(
        "Permission check",
        extra={
            "engine_id": engine_id,
            "platform": platform,
            "action_type": action_type,
            "request_id": get_request_id(),
        },
    )
    return JSONResponse(result)


@router.get("/platforms/list")
async def platforms_list_endpoint(
    x_engine_id: str = Header(None),
    x_engine_key: str = Header(None),
):
    """Return known platforms and their statuses."""

    verify_engine(x_engine_id, x_engine_key)
    return JSONResponse({"platforms": list_platforms()})


@router.get("/config/global")
async def global_config_endpoint(
    x_engine_id: str = Header(None),
    x_engine_key: str = Header(None),
):
    """Return global configuration information."""

    verify_engine(x_engine_id, x_engine_key)
    return JSONResponse(get_global_config())


@router.post("/log/engine_event")
async def log_engine_event_endpoint(
    data: dict,
    x_engine_id: str = Header(None),
    x_engine_key: str = Header(None),
):
    """Log an arbitrary engine event."""

    verify_engine(x_engine_id, x_engine_key)
    logger.info("Engine event", extra={"data": data, "request_id": get_request_id()})
    return JSONResponse({"status": "logged"})
