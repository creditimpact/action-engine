import importlib
import json
import pytest
from action_engine.auth import token_manager
from action_engine.tests.conftest import DummyRedis

# Import main after FastAPI stubs are set up in conftest
main = importlib.import_module("action_engine.main")

async def _token(user_id: str) -> str:
    resp = await main.login({"user_id": user_id})
    return resp.content["token"]

@pytest.mark.asyncio
async def test_start_oauth_returns_url():
    await token_manager.init_redis(DummyRedis())
    data = {
        "user_id": "u1",
        "platform": "gmail",
        "client_id": "id",
        "client_secret": "secret",
        "redirect_uri": "https://app/cb",
        "scope": "email",
    }
    token = await _token("u1")
    response = await main.start_oauth(data, authorization=f"Bearer {token}")
    assert response.status_code == 200
    assert response.content["authorization_url"].startswith("https://auth.example.com")

@pytest.mark.asyncio
async def test_oauth_callback_stores_token():
    await token_manager.init_redis(DummyRedis())
    data = {
        "user_id": "u1",
        "platform": "gmail",
        "client_id": "id",
        "client_secret": "secret",
        "redirect_uri": "https://app/cb",
        "authorization_response": "https://app/cb?code=1",
    }
    token = await _token("u1")
    response = await main.oauth_callback(data, authorization=f"Bearer {token}")
    assert response.status_code == 200
    stored = await token_manager.get_token("u1", "gmail")
    assert stored["access_token"] == "dummy-access-token"
