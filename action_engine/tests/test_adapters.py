import pytest
from action_engine.adapters import gmail_adapter, google_calendar_adapter, notion_adapter, zapier_adapter
from action_engine.auth import token_manager

@pytest.mark.asyncio
async def test_gmail_perform_action():
    params = {"a": 1}
    await token_manager.set_token("u1", "gmail", "t")
    result = await gmail_adapter.perform_action("u1", params)
    assert result == {"message": "בוצעה פעולה ב־Gmail", "params": params}

@pytest.mark.asyncio
async def test_gmail_send_email():
    payload = {"to": "x@example.com"}
    await token_manager.set_token("u1", "gmail", "t")
    result = await gmail_adapter.send_email("u1", payload)
    assert result == {
        "status": "success",
        "platform": "gmail",
        "message": "Email sent successfully",
        "data": payload,
    }

@pytest.mark.asyncio
async def test_google_calendar_create_event():
    payload = {"title": "meeting"}
    await token_manager.set_token("u1", "google_calendar", "t")
    result = await google_calendar_adapter.create_event("u1", payload)
    assert result == {
        "status": "success",
        "platform": "google_calendar",
        "message": "אירוע נוצר בהצלחה",
        "data": payload,
    }

@pytest.mark.asyncio
async def test_notion_create_task():
    payload = {"title": "task"}
    await token_manager.set_token("u1", "notion", "t")
    result = await notion_adapter.create_task("u1", payload)
    assert result == {
        "status": "success",
        "platform": "notion",
        "message": "משימה נוצרה בהצלחה",
        "data": payload,
    }

@pytest.mark.asyncio
async def test_zapier_perform_action():
    params = {"x": 2}
    await token_manager.set_token("u1", "zapier", "t")
    result = await zapier_adapter.perform_action("u1", params)
    assert result == {"message": "בוצעה פעולה דרך Zapier", "params": params}
