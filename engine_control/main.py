from fastapi import FastAPI

from .engine_api import router
from .engine_logger import RequestIdMiddleware

app = FastAPI()
app.add_middleware(RequestIdMiddleware)
app.include_router(router)
