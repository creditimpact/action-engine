async def create_task(payload):
    """Create a task in Notion (mocked)."""
    # Simulate interaction with Notion API
    print(f"[NOTION] create_task called with payload: {payload}")
    return {
        "status": "success",
        "platform": "notion",
        "message": "משימה נוצרה בהצלחה",
        "data": payload,
    }
