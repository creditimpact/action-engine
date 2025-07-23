import importlib
import os
import pytest

from validator import ActionRequest

# Set API key before importing main
os.environ["API_KEY"] = "test-key"
main = importlib.import_module("main")


@pytest.mark.asyncio
async def test_perform_action_missing_key():
    req = ActionRequest(action_type="perform_action", platform="test", user_id="u1", payload={})
    response = await main.perform_action(req)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_perform_action_invalid_key():
    req = ActionRequest(action_type="perform_action", platform="test", user_id="u1", payload={})
    response = await main.perform_action(req, x_api_key="bad")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_perform_action_success_with_key():
    req = ActionRequest(action_type="perform_action", platform="test", user_id="u1", payload={})
    response = await main.perform_action(req, x_api_key="test-key")
    assert response.status_code == 200
    assert response.content == {"message": "המערכת עובדת 🎯"}
