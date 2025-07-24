import pytest
from fastapi import HTTPException

from action_engine.adapters import (
    gmail_adapter,
    google_calendar_adapter,
    notion_adapter,
    zapier_adapter,
    BaseAdapter,
)
from action_engine.auth import token_manager
from action_engine.tests.conftest import DummyRedis


@pytest.mark.asyncio
async def test_gmail_perform_action():
    await token_manager.init_redis(DummyRedis())
    params = {"key": "value"}
    await token_manager.set_token("u1", "gmail", {"access_token": "t"})
    result = await gmail_adapter.perform_action("u1", params)
    assert result == {"message": "בוצעה פעולה ב־Gmail", "params": params}


@pytest.mark.asyncio
async def test_gmail_perform_action_validation_error():
    await token_manager.init_redis(DummyRedis())
    await token_manager.set_token("u1", "gmail", {"access_token": "t"})
    with pytest.raises(Exception):
        await gmail_adapter.perform_action("u1", {})


@pytest.mark.asyncio
async def test_gmail_send_email(monkeypatch):
    await token_manager.init_redis(DummyRedis())
    payload = {"to": "x@example.com"}
    await token_manager.set_token("u1", "gmail", {"access_token": "tok"})
    called = {}

    async def fake_post(url, headers=None, data=None):
        called["url"] = url
        called["headers"] = headers
        called["data"] = data
        return {"id": "1"}

    monkeypatch.setattr(gmail_adapter.adapter, "post", fake_post)
    result = await gmail_adapter.send_email("u1", payload)
    assert called["url"].startswith("https://gmail.googleapis.com")
    assert called["headers"]["Authorization"] == "Bearer tok"
    assert result == {
        "status": "success",
        "platform": "gmail",
        "message": "Email sent successfully",
        "data": payload,
    }


@pytest.mark.asyncio
async def test_gmail_send_email_error(monkeypatch):
    await token_manager.init_redis(DummyRedis())
    payload = {"to": "x@example.com"}
    await token_manager.set_token("u1", "gmail", {"access_token": "tok"})

    async def fake_post(url, headers=None, data=None):
        raise HTTPException(status_code=500, detail="boom")

    monkeypatch.setattr(gmail_adapter.adapter, "post", fake_post)
    with pytest.raises(HTTPException):
        await gmail_adapter.send_email("u1", payload)


@pytest.mark.asyncio
async def test_gmail_send_email_validation_error():
    await token_manager.init_redis(DummyRedis())
    await token_manager.set_token("u1", "gmail", {"access_token": "t"})
    with pytest.raises(Exception):
        await gmail_adapter.send_email("u1", {})


@pytest.mark.asyncio
async def test_google_calendar_create_event():
    await token_manager.init_redis(DummyRedis())
    payload = {"title": "meeting"}
    await token_manager.set_token("u1", "google_calendar", {"access_token": "t"})
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
    await token_manager.set_token("u1", "google_calendar", {"access_token": "t"})
    with pytest.raises(Exception):
        await google_calendar_adapter.create_event("u1", {})


@pytest.mark.asyncio
async def test_notion_create_task():
    await token_manager.init_redis(DummyRedis())
    payload = {"title": "task"}
    await token_manager.set_token("u1", "notion", {"access_token": "t"})
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
    await token_manager.set_token("u1", "notion", {"access_token": "t"})
    with pytest.raises(Exception):
        await notion_adapter.create_task("u1", {})


@pytest.mark.asyncio
async def test_zapier_perform_action():
    await token_manager.init_redis(DummyRedis())
    params = {"x": 2}
    await token_manager.set_token("u1", "zapier", {"access_token": "t"})
    result = await zapier_adapter.perform_action("u1", params)
    assert result == {"message": "בוצעה פעולה דרך Zapier", "params": params}


@pytest.mark.asyncio
async def test_zapier_perform_action_validation_error():
    await token_manager.init_redis(DummyRedis())
    await token_manager.set_token("u1", "zapier", {"access_token": "t"})
    with pytest.raises(Exception):
        await zapier_adapter.perform_action("u1", {})


@pytest.mark.asyncio
async def test_base_adapter_timeout(monkeypatch):
    adapter = BaseAdapter("dummy")

    called = {}

    class DummyResp:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

        def read(self):
            return b"{}"

    def fake_urlopen(req, timeout=None):
        called["timeout"] = timeout
        return DummyResp()

    import action_engine.adapters.__init__ as base_mod

    monkeypatch.setattr(base_mod.request, "urlopen", fake_urlopen)

    coro = await adapter.send_http_request("GET", "http://x")
    result = await coro
    assert result == {}
    assert called["timeout"] == 10.0

    called.clear()
    coro = await adapter.send_http_request("GET", "http://x", timeout=5)
    result = await coro
    assert result == {}
    assert called["timeout"] == 5

