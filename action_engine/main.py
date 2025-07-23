from fastapi import FastAPI
from router import route_action
from validator import ActionRequest

app = FastAPI()


@app.post("/perform_action")
async def perform_action(request: ActionRequest):
    return await route_action(request.dict())
