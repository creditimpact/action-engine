import importlib
import pytest
from action_engine.tests.conftest import DummyRedis
from vault_engine import vault_storage

vault_api = importlib.import_module("vault_engine.vault_api")


@pytest.mark.asyncio
async def test_refresh_expired_token():
    await vault_storage.init_redis(DummyRedis())
    data = {
        "user_id": "u2",
        "platform": "google",
        "access_token": "old",
        "refresh_token": "ref",
        "expires_at": 0,
        "scopes": [],
    }
    await vault_api.store_token_endpoint(data, x_engine_id="local", x_engine_key="local-key")
    resp = await vault_api.get_token_endpoint("u2", "google", x_engine_id="local", x_engine_key="local-key")
    assert resp.status_code == 200
    assert resp.content["access_token"].startswith("refreshed-")
