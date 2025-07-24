import importlib
import pytest

from action_engine.auth import token_manager
from action_engine.tests.conftest import DummyRedis


# Import main after FastAPI stubs are set up in conftest
main = importlib.import_module("action_engine.main")


async def _token(user_id: str) -> str:
    resp = await main.login({"user_id": user_id})
    return resp.content["token"]


@pytest.mark.asyncio
async def test_save_token_success():
    await token_manager.init_redis(DummyRedis())
    payload = {"user_id": "u1", "platform": "gmail", "access_token": "tok"}
    token = await _token("u1")
    response = await main.save_token(payload, authorization=f"Bearer {token}")
    assert response.status_code == 200
    assert response.content == {"status": "ok"}
    assert await token_manager.get_token("u1", "gmail") == {"access_token": "tok"}


@pytest.mark.asyncio
async def test_save_token_validation_error():
    await token_manager.init_redis(DummyRedis())
    payload = {"user_id": "u1", "platform": "gmail"}  # missing access_token
    token = await _token("u1")
    response = await main.save_token(payload, authorization=f"Bearer {token}")
    assert response.status_code == 400
    assert "Invalid token payload" in response.content["error"]


@pytest.mark.asyncio
async def test_save_token_unauthorized():
    await token_manager.init_redis(DummyRedis())
    payload = {"user_id": "u1", "platform": "gmail", "access_token": "tok"}
    response = await main.save_token(payload, authorization="Bearer bad")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_perform_action_requires_token():
    await token_manager.init_redis(DummyRedis())
    request = main.ActionRequest(
        action_type="perform_action",
        platform="test",
        user_id="u1",
        payload={}
    )
    response = await main.perform_action(request, authorization="Bearer bad")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_perform_action_success_with_token():
    await token_manager.init_redis(DummyRedis())
    request = main.ActionRequest(
        action_type="perform_action",
        platform="test",
        user_id="u1",
        payload={}
    )
    token = await _token("u1")
    response = await main.perform_action(request, authorization=f"Bearer {token}")
    assert response.status_code == 200
