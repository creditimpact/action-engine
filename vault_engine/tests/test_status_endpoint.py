import importlib
import pytest
from fastapi import HTTPException

# Import vault_api after FastAPI stubs are loaded via conftest
vault_api = importlib.import_module("vault_engine.vault_api")


@pytest.mark.asyncio
async def test_status_endpoint_unauthorized():
    """Unauthorized requests should raise HTTPException 401."""
    with pytest.raises(HTTPException) as exc:
        await vault_api.status_endpoint("u1", x_engine_id="bad", x_engine_key="bad")
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_status_endpoint_authorized(monkeypatch):
    """Authorized requests return statuses from connection_checker.get_status."""
    statuses = {"google": "connected", "slack": "missing"}
    called = {}

    async def fake_get_status(user_id: str):
        called["user_id"] = user_id
        return statuses

    # Patch both the imported reference in vault_api and the module itself
    import vault_engine.connection_checker as connection_checker
    monkeypatch.setattr(connection_checker, "get_status", fake_get_status)
    monkeypatch.setattr(vault_api, "get_status", fake_get_status)

    resp = await vault_api.status_endpoint(
        "u1", x_engine_id="local", x_engine_key="local-key"
    )
    assert called["user_id"] == "u1"
    assert resp.status_code == 200
    assert resp.content == statuses
