import importlib
import pytest
from action_engine.tests.conftest import DummyRedis
from vault_engine import vault_storage

vault_api = importlib.import_module("vault_engine.vault_api")


@pytest.mark.asyncio
async def test_store_and_retrieve_token():
    await vault_storage.init_redis(DummyRedis())
    data = {
        "user_id": "u1",
        "platform": "google",
        "access_token": "tok",
        "refresh_token": "ref",
        "expires_at": None,
        "scopes": ["email"],
    }
    resp = await vault_api.store_token_endpoint(data, x_engine_id="local", x_engine_key="local-key")
    assert resp.status_code == 200
    resp2 = await vault_api.get_token_endpoint("u1", "google", x_engine_id="local", x_engine_key="local-key")
    assert resp2.status_code == 200
    assert resp2.content["access_token"] == "tok"
    assert resp2.content["refresh_token"] == "ref"
