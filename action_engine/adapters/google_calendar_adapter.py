# google_calendar_adapter.py

async def create_event(payload):
    """
    יוצר אירוע ביומן Google (מימוש ראשוני, דמיוני).
    """
    # תיעוד / הדמיה
    print(f"[GOOGLE_CALENDAR] create_event called with payload: {payload}")

    # Placeholder for Google Calendar API integration
    # Example: await google_calendar_client.create_event(payload)

    # החזרה דמיונית
    return {
        "status": "success",
        "platform": "google_calendar",
        "message": "אירוע נוצר בהצלחה",
        "data": payload
    }
