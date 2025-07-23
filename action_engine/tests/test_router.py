import importlib
import pytest

# Import router after fastapi stub is set up in conftest
router = importlib.import_module("router")

def make_payload():
    return {"key": "value"}

@pytest.mark.asyncio
async def test_route_gmail_success():
    payload = make_payload()
    response = await router.route_action({
        "platform": "gmail",
        "action_type": "perform_action",
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
    response = await router.route_action({
        "platform": "google_calendar",
        "action_type": "create_event",
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
    response = await router.route_action({
        "platform": "notion",
        "action_type": "create_task",
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
    response = await router.route_action({
        "platform": "zapier",
        "action_type": "perform_action",
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
        "payload": {},
    })
    assert response.status_code == 400
    assert "פלטפורמה" in response.content["error"]

@pytest.mark.asyncio
async def test_unknown_action_error():
    response = await router.route_action({
        "platform": "gmail",
        "action_type": "unknown",
        "payload": {},
    })
    assert response.status_code == 400
    assert "לא קיימת" in response.content["error"]
