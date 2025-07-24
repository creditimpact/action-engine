import importlib
import pytest

main = importlib.import_module("engine_control.engine_api")
from engine_control import engine_registry, platform_registry

@pytest.mark.asyncio
async def test_action_check_denied_when_platform_down():
    engine_registry.clear_engines()
    platform_registry.clear_platforms()
    token_resp = await main.register_engine_endpoint({"engine_id": "e2", "permissions": {"gmail": {"send": []}}}, x_engine_id="local", x_engine_key="local-key")
    token = token_resp.content["engine_key"]
    platform_registry.set_platform_status("gmail", "maintenance")
    result = await main.actions_check_endpoint({"engine_id": "e2", "platform": "gmail", "action_type": "send"}, x_engine_id="e2", x_engine_key=token)
    assert result.status_code == 200
    assert result.content["allowed"] is False
    assert result.content["platform_status"] == "maintenance"

