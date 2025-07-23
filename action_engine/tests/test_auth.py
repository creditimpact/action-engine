import importlib
import os
import pytest

from auth import token_manager


# Import main after setting API_KEY and FastAPI stubs
os.environ["API_KEY"] = "test-key"
main = importlib.import_module("main")


@pytest.mark.asyncio
async def test_save_token_success():
    payload = {"user_id": "u1", "platform": "gmail", "access_token": "tok"}
    response = await main.save_token(payload, x_api_key="test-key")
    assert response.status_code == 200
    assert response.content == {"status": "ok"}
    assert token_manager.get_token("u1", "gmail") == "tok"


@pytest.mark.asyncio
async def test_save_token_validation_error():
    payload = {"user_id": "u1", "platform": "gmail"}  # missing access_token
    response = await main.save_token(payload, x_api_key="test-key")
    assert response.status_code == 400
    assert "Invalid token payload" in response.content["error"]


@pytest.mark.asyncio
async def test_save_token_missing_key():
    payload = {"user_id": "u1", "platform": "gmail", "access_token": "tok"}
    response = await main.save_token(payload)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_save_token_invalid_key():
    payload = {"user_id": "u1", "platform": "gmail", "access_token": "tok"}
    response = await main.save_token(payload, x_api_key="bad")
    assert response.status_code == 401
