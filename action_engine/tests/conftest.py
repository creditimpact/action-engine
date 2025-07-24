import sys
import types
from pathlib import Path

class DummyJSONResponse:
    def __init__(self, content, status_code=200):
        self.content = content
        self.status_code = status_code


class DummyHTTPException(Exception):
    """Lightweight stand-in for FastAPI HTTPException."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail

a_responses = types.ModuleType("fastapi.responses")
a_responses.JSONResponse = DummyJSONResponse

a_exceptions = types.ModuleType("fastapi.exceptions")
a_exceptions.HTTPException = DummyHTTPException

fastapi = types.ModuleType("fastapi")
fastapi.responses = a_responses
fastapi.HTTPException = DummyHTTPException
def Header(default=None):
    return default
fastapi.Header = Header

# Minimal FastAPI stub so modules importing FastAPI don't fail
class DummyFastAPI:
    def __init__(self):
        self.middlewares = []

    def post(self, path):
        def decorator(func):
            return func
        return decorator

    def add_middleware(self, middleware_class, **options):
        self.middlewares.append((middleware_class, options))

fastapi.FastAPI = DummyFastAPI

sys.modules.setdefault("fastapi", fastapi)
sys.modules.setdefault("fastapi.responses", a_responses)
sys.modules.setdefault("fastapi.exceptions", a_exceptions)

# -- Pydantic stubs ---------------------------------------------------------
pydantic = types.ModuleType("pydantic")

class BaseModel:
    def __init__(self, **data):
        for k, v in data.items():
            setattr(self, k, v)

    def dict(self):
        return self.__dict__


class ValidationError(Exception):
    pass

pydantic.BaseModel = BaseModel
pydantic.ValidationError = ValidationError

sys.modules.setdefault("pydantic", pydantic)

# Ensure project root is on the import path so tests can import modules
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Minimal support for `pytest.mark.asyncio` without external dependency
import inspect
import asyncio
import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem):
    if pyfuncitem.get_closest_marker("asyncio"):
        func = pyfuncitem.obj
        if inspect.iscoroutinefunction(func):
            asyncio.run(func(**pyfuncitem.funcargs))
            return True

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "asyncio: mark test to run asynchronously using asyncio.run"
    )


class DummyRedis:
    def __init__(self):
        self.store = {}

    async def ping(self):  # pragma: no cover - simple stub
        return True

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value):
        self.store[key] = value
