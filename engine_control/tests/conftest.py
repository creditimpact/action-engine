from action_engine.tests.conftest import DummyRedis, pytest_pyfunc_call, pytest_configure

# Add minimal APIRouter stub so engine_control modules can import fastapi.APIRouter

fastapi = __import__("fastapi")

class DummyAPIRouter:
    def post(self, path):
        def decorator(func):
            return func
        return decorator

    def get(self, path):
        def decorator(func):
            return func
        return decorator

fastapi.APIRouter = DummyAPIRouter

__all__ = ["DummyRedis"]
