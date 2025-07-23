async def perform_action(params):
    # כאן תבוא האינטגרציה עם Zapier Webhook / Trigger
    return {"message": "בוצעה פעולה דרך Zapier", "params": params}


async def trigger_zap(payload: dict) -> dict:
    """Trigger a Zap via webhook (mocked)."""
    print(f"[ZAPIER] trigger_zap called with payload: {payload}")

    # Placeholder for actual webhook call
    # Example: await zapier_client.trigger(payload)

    return {
        "status": "success",
        "platform": "zapier",
        "message": "Zap triggered successfully",
        "data": payload,
    }
