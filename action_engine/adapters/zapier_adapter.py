from action_engine.logging.logger import get_logger

logger = get_logger()


async def perform_action(params):
    """Placeholder Zapier action."""
    # כאן תבוא האינטגרציה עם Zapier Webhook / Trigger
    logger.info("[ZAPIER] perform_action called with params: %s", params)
    return {"message": "בוצעה פעולה דרך Zapier", "params": params}
