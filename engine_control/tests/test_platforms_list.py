import importlib
import pytest

main = importlib.import_module("engine_control.engine_api")
from engine_control import platform_registry

@pytest.mark.asyncio
async def test_platforms_list_endpoint():
    platform_registry.clear_platforms()
    platform_registry.set_platform_status("gmail", "active")
    platform_registry.set_platform_status("slack", "maintenance")
    resp = await main.platforms_list_endpoint(x_engine_id="local", x_engine_key="local-key")
    assert resp.status_code == 200
    assert resp.content == {"platforms": {"gmail": "active", "slack": "maintenance"}}

