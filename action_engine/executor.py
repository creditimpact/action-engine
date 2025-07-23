from typing import Any, Dict

from router import route_action


async def execute(action_model: Any):
    """Execute an action model immediately via :func:`route_action`.

    Parameters
    ----------
    action_model: Any
        Object describing the action. It can be either a dictionary or a
        Pydantic model with a ``dict()`` method.
    """
    # Normalize the input to a simple dictionary that ``route_action`` expects.
    if hasattr(action_model, "dict"):
        payload: Dict[str, Any] = action_model.dict()
    else:
        payload = dict(action_model)

    # Delegate execution to the central router which invokes the proper adapter.
    return await route_action(payload)
