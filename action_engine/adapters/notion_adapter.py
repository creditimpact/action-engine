async def create_task(payload):
    """Create a task in Notion (mocked)."""
    # Simulate interaction with Notion API
    print(f"[Notion] Creating task with payload: {payload}")
    return {
        "status": "success",
        "platform": "notion",
        "message": "משימה נוצרה בהצלחה",
        "data": payload,
    }
