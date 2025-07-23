import importlib
import pytest
from action_engine.auth import token_manager

# Import router after fastapi stub is set up in conftest
router = importlib.import_module("action_engine.router")

def make_payload():
    return {"key": "value"}

@pytest.mark.asyncio
async def test_route_gmail_success():
    payload = make_payload()
    token_manager.set_token("u1", "gmail", "t")
    response = await router.route_action({
        "platform": "gmail",
        "action_type": "perform_action",
        "user_id": "u1",
        "payload": payload,
    })
    assert response.status_code == 200
    assert response.content == {
        "status": "success",
        "result": {
            "message": "בוצעה פעולה ב־Gmail",
            "params": payload,
        },
    }

@pytest.mark.asyncio
async def test_route_google_calendar_success():
    payload = make_payload()
    token_manager.set_token("u1", "google_calendar", "t")
    response = await router.route_action({
        "platform": "google_calendar",
        "action_type": "create_event",
        "user_id": "u1",
        "payload": payload,
    })
    assert response.status_code == 200
    assert response.content == {
        "status": "success",
        "result": {
            "status": "success",
            "platform": "google_calendar",
            "message": "אירוע נוצר בהצלחה",
            "data": payload,
        },
    }

@pytest.mark.asyncio
async def test_route_notion_success():
    payload = make_payload()
    token_manager.set_token("u1", "notion", "t")
    response = await router.route_action({
        "platform": "notion",
        "action_type": "create_task",
        "user_id": "u1",
        "payload": payload,
    })
    assert response.status_code == 200
    assert response.content == {
        "status": "success",
        "result": {
            "status": "success",
            "platform": "notion",
            "message": "משימה נוצרה בהצלחה",
            "data": payload,
        },
    }

@pytest.mark.asyncio
async def test_route_zapier_success():
    payload = make_payload()
    token_manager.set_token("u1", "zapier", "t")
    response = await router.route_action({
        "platform": "zapier",
        "action_type": "perform_action",
        "user_id": "u1",
        "payload": payload,
    })
    assert response.status_code == 200
    assert response.content == {
        "status": "success",
        "result": {
            "message": "בוצעה פעולה דרך Zapier",
            "params": payload,
        },
    }

@pytest.mark.asyncio
async def test_missing_platform_error():
    response = await router.route_action({
        "action_type": "perform_action",
        "user_id": "u1",
        "payload": {},
    })
    assert response.status_code == 400
    assert "פלטפורמה" in response.content["error"]

@pytest.mark.asyncio
async def test_unknown_action_error():
    response = await router.route_action({
        "platform": "gmail",
        "action_type": "unknown",
        "user_id": "u1",
        "payload": {},
    })
    assert response.status_code == 400
    assert "לא קיימת" in response.content["error"]
