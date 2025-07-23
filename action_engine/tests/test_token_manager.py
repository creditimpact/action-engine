import pytest
from auth import token_manager


@pytest.mark.asyncio
async def test_token_storage_per_user():
    await token_manager.set_token("user1", "gmail", "tok1")
    await token_manager.set_token("user2", "gmail", "tok2")
    assert await token_manager.get_token("user1", "gmail") == "tok1"
    assert await token_manager.get_token("user2", "gmail") == "tok2"
    assert await token_manager.get_token("user3", "gmail") is None
