async def perform_action(params):
    # כאן תבוא האינטגרציה האמיתית עם Gmail
    return {"message": "בוצעה פעולה ב־Gmail", "params": params}


async def send_email(payload: dict) -> dict:
    """Send an email via Gmail.

    This function currently mocks the interaction with the Gmail API and
    simply echoes back the provided payload.
    """
    # Basic logging for action invocation
    print(f"[GMAIL] send_email called with payload: {payload}")

    return {
        "status": "success",
        "platform": "gmail",
        "message": "Email sent successfully",
        "data": payload,
    }

