import pytest
from auth import token_manager


def test_token_storage_per_user():
    token_manager.set_token("user1", "gmail", "tok1")
    token_manager.set_token("user2", "gmail", "tok2")
    assert token_manager.get_token("user1", "gmail") == "tok1"
    assert token_manager.get_token("user2", "gmail") == "tok2"
    assert token_manager.get_token("user3", "gmail") is None
