import pytest
from action_engine.adapters import gmail_adapter, google_calendar_adapter, notion_adapter, zapier_adapter
from action_engine.auth import token_manager
from action_engine.tests.conftest import DummyRedis

@pytest.mark.asyncio
async def test_gmail_perform_action():
    await token_manager.init_redis(DummyRedis())
    params = {"key": "value"}
    await token_manager.set_token("u1", "gmail", "t")
    result = await gmail_adapter.perform_action("u1", params)
    assert result == {"message": "בוצעה פעולה ב־Gmail", "params": params}


@pytest.mark.asyncio
async def test_gmail_perform_action_validation_error():
    await token_manager.init_redis(DummyRedis())
    await token_manager.set_token("u1", "gmail", "t")
    with pytest.raises(Exception):
        await gmail_adapter.perform_action("u1", {})

@pytest.mark.asyncio
async def test_gmail_send_email():
    await token_manager.init_redis(DummyRedis())
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
async def test_gmail_send_email_validation_error():
    await token_manager.init_redis(DummyRedis())
    await token_manager.set_token("u1", "gmail", "t")
    with pytest.raises(Exception):
        await gmail_adapter.send_email("u1", {})

@pytest.mark.asyncio
async def test_google_calendar_create_event():
    await token_manager.init_redis(DummyRedis())
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
async def test_google_calendar_create_event_validation_error():
    await token_manager.init_redis(DummyRedis())
    await token_manager.set_token("u1", "google_calendar", "t")
    with pytest.raises(Exception):
        await google_calendar_adapter.create_event("u1", {})

@pytest.mark.asyncio
async def test_notion_create_task():
    await token_manager.init_redis(DummyRedis())
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
async def test_notion_create_task_validation_error():
    await token_manager.init_redis(DummyRedis())
    await token_manager.set_token("u1", "notion", "t")
    with pytest.raises(Exception):
        await notion_adapter.create_task("u1", {})

@pytest.mark.asyncio
async def test_zapier_perform_action():
    await token_manager.init_redis(DummyRedis())
    params = {"x": 2}
    await token_manager.set_token("u1", "zapier", "t")
    result = await zapier_adapter.perform_action("u1", params)
    assert result == {"message": "בוצעה פעולה דרך Zapier", "params": params}


@pytest.mark.asyncio
async def test_zapier_perform_action_validation_error():
    await token_manager.init_redis(DummyRedis())
    await token_manager.set_token("u1", "zapier", "t")
    with pytest.raises(Exception):
        await zapier_adapter.perform_action("u1", {})
