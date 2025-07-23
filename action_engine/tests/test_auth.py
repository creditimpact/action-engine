import importlib
import pytest

from action_engine.auth import token_manager


# Import main after FastAPI stubs are set up in conftest
main = importlib.import_module("action_engine.main")


@pytest.mark.asyncio
async def test_save_token_success():
    payload = {"user_id": "u1", "platform": "gmail", "access_token": "tok"}
    response = await main.save_token(payload)
    assert response.status_code == 200
    assert response.content == {"status": "ok"}
    assert token_manager.get_token("u1", "gmail") == "tok"


@pytest.mark.asyncio
async def test_save_token_validation_error():
    payload = {"user_id": "u1", "platform": "gmail"}  # missing access_token
    response = await main.save_token(payload)
    assert response.status_code == 400
    assert "Invalid token payload" in response.content["error"]
