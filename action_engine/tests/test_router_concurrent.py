import asyncio
import importlib
import pytest
from action_engine.auth import token_manager
from action_engine.tests.conftest import DummyRedis

# Import router after FastAPI stubs are set up in conftest
router = importlib.import_module("action_engine.router")


def make_payload(platform="gmail"):
    if platform == "gmail":
        return {"key": "value"}
    if platform == "google_calendar":
        return {"title": "meeting"}
    if platform == "notion":
        return {"title": "task"}
    if platform == "zapier":
        return {"x": 1}
    return {}


@pytest.mark.asyncio
async def test_router_concurrent_actions():
    await token_manager.init_redis(DummyRedis())

    combos = [
        ("gmail", "perform_action"),
        ("google_calendar", "create_event"),
        ("notion", "create_task"),
        ("zapier", "perform_action"),
    ]

    tasks = []
    expected = []
    tokens = {}

    for i in range(5):
        for platform, action_type in combos:
            user_id = f"u{i}_{platform}"
            payload = make_payload(platform)
            token_data = {"access_token": f"t{i}_{platform}"}
            await token_manager.set_token(user_id, platform, token_data)
            tokens[(user_id, platform)] = token_data

            tasks.append(
                router.route_action(
                    {
                        "platform": platform,
                        "action_type": action_type,
                        "user_id": user_id,
                        "payload": payload,
                    }
                )
            )

            if platform == "gmail":
                expected.append(
                    {
                        "status": "success",
                        "result": {"message": "בוצעה פעולה ב־Gmail", "params": payload},
                    }
                )
            elif platform == "google_calendar":
                expected.append(
                    {
                        "status": "success",
                        "result": {
                            "status": "success",
                            "platform": "google_calendar",
                            "message": "אירוע נוצר בהצלחה",
                            "data": payload,
                        },
                    }
                )
            elif platform == "notion":
                expected.append(
                    {
                        "status": "success",
                        "result": {
                            "status": "success",
                            "platform": "notion",
                            "message": "משימה נוצרה בהצלחה",
                            "data": payload,
                        },
                    }
                )
            else:  # zapier
                expected.append(
                    {
                        "status": "success",
                        "result": {"message": "בוצעה פעולה דרך Zapier", "params": payload},
                    }
                )

    responses = await asyncio.gather(*tasks)

    for resp, exp in zip(responses, expected):
        assert resp.status_code == 200
        assert resp.content == exp

    # verify tokens unaffected across concurrent calls
    for (user_id, platform), token in tokens.items():
        assert await token_manager.get_token(user_id, platform) == token
