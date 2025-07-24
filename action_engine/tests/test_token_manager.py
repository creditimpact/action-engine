import json
import time
import pytest
from action_engine.auth import token_manager
from action_engine.tests.conftest import DummyRedis


@pytest.mark.asyncio
async def test_token_storage_per_user():
    await token_manager.init_redis(DummyRedis())
    await token_manager.set_token("user1", "gmail", {"access_token": "tok1"})
    await token_manager.set_token("user2", "gmail", {"access_token": "tok2"})
    assert await token_manager.get_token("user1", "gmail") == {"access_token": "tok1"}
    assert await token_manager.get_token("user2", "gmail") == {"access_token": "tok2"}
    assert await token_manager.get_token("user3", "gmail") is None


@pytest.mark.asyncio
async def test_token_isolation_between_platforms():
    await token_manager.init_redis(DummyRedis())
    await token_manager.set_token("user1", "gmail", {"access_token": "tok1"})
    await token_manager.set_token("user1", "notion", {"access_token": "tok2"})
    assert await token_manager.get_token("user1", "gmail") == {"access_token": "tok1"}
    assert await token_manager.get_token("user1", "notion") == {"access_token": "tok2"}


@pytest.mark.asyncio
async def test_missing_redis_raises_error(monkeypatch):
    # Simulate redis not available
    await token_manager.init_redis(DummyRedis())
    monkeypatch.setattr(token_manager, "_redis_client", None)
    monkeypatch.setattr(token_manager, "redis", None)
    with pytest.raises(RuntimeError):
        await token_manager.get_token("u", "gmail")


@pytest.mark.asyncio
async def test_refresh_if_needed():
    await token_manager.init_redis(DummyRedis())
    expired = {
        "access_token": "old",
        "refresh_token": "ref",
        "expires_at": 0,
    }
    await token_manager.set_token("u", "gmail", expired)
    token = await token_manager.get_access_token("u", "gmail")
    assert token.startswith("refreshed-")


@pytest.mark.asyncio
async def test_refresh_encrypted_token():
    await token_manager.init_redis(DummyRedis())
    past = time.time() - 1
    token_data = {
        "access_token": "old", 
        "refresh_token": "r1", 
        "expires_at": past,
    }
    encoded = token_manager._encrypt(json.dumps(token_data))
    await token_manager._redis_client.set("u:gmail", encoded)
    token = await token_manager.get_access_token("u", "gmail")
    assert token.startswith("refreshed-")


@pytest.mark.asyncio
async def test_no_refresh_without_expires_at():
    await token_manager.init_redis(DummyRedis())
    data = {
        "access_token": "curr",
        "refresh_token": "r2",
    }
    encoded = token_manager._encrypt(json.dumps(data))
    await token_manager._redis_client.set("u:gmail", encoded)
    token = await token_manager.get_access_token("u", "gmail")
    assert token == "curr"
