import pytest
from adapters import gmail_adapter, google_calendar_adapter, notion_adapter, zapier_adapter

@pytest.mark.asyncio
async def test_gmail_perform_action():
    params = {"a": 1}
    result = await gmail_adapter.perform_action(params)
    assert result == {"message": "בוצעה פעולה ב־Gmail", "params": params}

@pytest.mark.asyncio
async def test_gmail_send_email():
    payload = {"to": "x@example.com"}
    result = await gmail_adapter.send_email(payload)
    assert result == {
        "status": "success",
        "platform": "gmail",
        "message": "Email sent successfully",
        "data": payload,
    }

@pytest.mark.asyncio
async def test_google_calendar_create_event():
    payload = {"title": "meeting"}
    result = await google_calendar_adapter.create_event(payload)
    assert result == {
        "status": "success",
        "platform": "google_calendar",
        "message": "אירוע נוצר בהצלחה",
        "data": payload,
    }

@pytest.mark.asyncio
async def test_notion_create_task():
    payload = {"title": "task"}
    result = await notion_adapter.create_task(payload)
    assert result == {
        "status": "success",
        "platform": "notion",
        "message": "משימה נוצרה בהצלחה",
        "data": payload,
    }

@pytest.mark.asyncio
async def test_zapier_perform_action():
    params = {"x": 2}
    result = await zapier_adapter.perform_action(params)
    assert result == {"message": "בוצעה פעולה דרך Zapier", "params": params}
