import sys
import types
from pathlib import Path

class DummyJSONResponse:
    def __init__(self, content, status_code=200):
        self.content = content
        self.status_code = status_code

a_responses = types.ModuleType("fastapi.responses")
a_responses.JSONResponse = DummyJSONResponse

fastapi = types.ModuleType("fastapi")
fastapi.responses = a_responses

sys.modules.setdefault("fastapi", fastapi)
sys.modules.setdefault("fastapi.responses", a_responses)

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
