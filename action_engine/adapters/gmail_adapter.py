async def perform_action(params):
    # כאן תבוא האינטגרציה האמיתית עם Gmail
    return {"message": "בוצעה פעולה ב־Gmail", "params": params}


async def send_email(payload):
    """Simulate sending an email via Gmail."""
    # Logging or debugging output for the mocked action
    print(f"[Gmail] Sending email with payload: {payload}")

    return {
        "status": "success",
        "platform": "gmail",
        "message": "Email sent successfully",
        "data": payload,
    }

