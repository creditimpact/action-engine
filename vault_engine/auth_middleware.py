import os
from fastapi import HTTPException, Header

AUTHORIZED_ENGINES = {
    "action": os.getenv("ACTION_ENGINE_KEY", "action-key"),
    "sync": os.getenv("SYNC_ENGINE_KEY", "sync-key"),
    "local": os.getenv("LOCAL_ENGINE_KEY", "local-key"),
}


def verify_engine(engine_id: str | None, engine_key: str | None) -> None:
    """Ensure the caller is an authorized engine."""
    if not engine_id or not engine_key:
        raise HTTPException(status_code=401, detail="Unauthorized")
    key = AUTHORIZED_ENGINES.get(engine_id)
    if key != engine_key:
        raise HTTPException(status_code=401, detail="Unauthorized")
