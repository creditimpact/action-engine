from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from router import route_action

app = FastAPI()

# ✅ עדכון: מודל בקשה מלא עם כל השדות
class ActionRequest(BaseModel):
    action_type: str
    platform: str
    payload: Dict[str, Any]

@app.post("/perform_action")
async def perform_action(request: ActionRequest):
    return await route_action(request.dict())
