import importlib
import pytest
from fastapi import HTTPException

# Import main after FastAPI stubs are loaded via conftest
main = importlib.import_module("engine_control.main")

from engine_control import engine_registry, platform_registry, engine_config


@pytest.mark.asyncio
async def test_register_engine_and_allowed_action():
    engine_registry.clear_engines()
    platform_registry.clear_platforms()
    engine_config.clear_engine_configs()

    data = {
        "engine_id": "action",
        "permissions": {
            "gmail": {"send_mail": ["mail.send"]}
        },
    }
    resp = await main.register_engine_endpoint(data, x_engine_id="local", x_engine_key="local-key")
    assert resp.status_code == 200

    await main.set_platform_status_endpoint({"platform": "gmail", "status": "active"}, x_engine_id="local", x_engine_key="local-key")

    result = await main.is_action_allowed_endpoint(
        {"engine_id": "action", "platform": "gmail", "action_type": "send_mail"},
        x_engine_id="local",
        x_engine_key="local-key",
    )
    assert result.status_code == 200
    assert result.content == {
        "action_allowed": True,
        "required_scopes": ["mail.send"],
        "platform_status": "active",
    }


@pytest.mark.asyncio
async def test_action_denied_for_unregistered_engine():
    engine_registry.clear_engines()
    platform_registry.clear_platforms()
    result = await main.is_action_allowed_endpoint(
        {"engine_id": "missing", "platform": "gmail", "action_type": "send"},
        x_engine_id="local",
        x_engine_key="local-key",
    )
    assert result.status_code == 200
    assert result.content["action_allowed"] is False


@pytest.mark.asyncio
async def test_platform_maintenance_rejects_action():
    engine_registry.clear_engines()
    platform_registry.clear_platforms()
    await main.register_engine_endpoint({"engine_id": "a", "permissions": {"gmail": {"send": []}}}, x_engine_id="local", x_engine_key="local-key")
    await main.set_platform_status_endpoint({"platform": "gmail", "status": "maintenance"}, x_engine_id="local", x_engine_key="local-key")
    result = await main.is_action_allowed_endpoint(
        {"engine_id": "a", "platform": "gmail", "action_type": "send"},
        x_engine_id="local",
        x_engine_key="local-key",
    )
    assert result.content["action_allowed"] is False
    assert result.content["platform_status"] == "maintenance"


@pytest.mark.asyncio
async def test_missing_headers_return_403():
    with pytest.raises(HTTPException) as exc:
        await main.is_action_allowed_endpoint({"engine_id": "a", "platform": "gmail", "action_type": "send"}, x_engine_id=None, x_engine_key=None)
    assert exc.value.status_code == 403

@pytest.mark.asyncio
async def test_invalid_headers_return_403():
    with pytest.raises(HTTPException) as exc:
        await main.is_action_allowed_endpoint(
            {"engine_id": "a", "platform": "gmail", "action_type": "send"},
            x_engine_id="bad",
            x_engine_key="bad",
        )
    assert exc.value.status_code == 403

