async def perform_action(params):
    # כאן תבוא האינטגרציה האמיתית עם Gmail
    return {"message": "בוצעה פעולה ב־Gmail", "params": params}


from action_engine.logging.logger import get_logger

logger = get_logger()


async def send_email(payload):
    """Simulate sending an email via Gmail."""
    # Basic logging for action invocation
    logger.info("[GMAIL] send_email called with payload: %s", payload)

    return {
        "status": "success",
        "platform": "gmail",
        "message": "Email sent successfully",
        "data": payload,
    }

