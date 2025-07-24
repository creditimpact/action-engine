import importlib
import pytest

main = importlib.import_module("engine_control.engine_api")
from engine_control import engine_registry

@pytest.mark.asyncio
async def test_register_and_validate_engine():
    engine_registry.clear_engines()
    resp = await main.register_engine_endpoint({"engine_id": "e1", "permissions": {}}, x_engine_id="local", x_engine_key="local-key")
    assert resp.status_code == 200
    token = resp.content["engine_key"]

    valid = await main.validate_engine_endpoint(None, x_engine_id="e1", x_engine_key=token)
    assert valid.status_code == 200
    assert valid.content == {"valid": True}

