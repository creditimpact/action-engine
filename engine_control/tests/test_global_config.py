import importlib
import pytest

main = importlib.import_module("engine_control.engine_api")
from engine_control import config

@pytest.mark.asyncio
async def test_global_config_endpoint():
    config.clear_global_config()
    config.set_global_config({"feature_flags": {"x": True}})
    resp = await main.global_config_endpoint(x_engine_id="local", x_engine_key="local-key")
    assert resp.status_code == 200
    assert resp.content["feature_flags"] == {"x": True}

