from datetime import datetime

WARNING_DAYS = 15
CRITICAL_DAYS = 30
GRACE_DAYS = 7


def apply_decay(event):
    try:
        last_used = datetime.fromisoformat(event["timestamp"])
    except:
        return event

    now = datetime.now()
    days_unused = (now - last_used).days

    event["days_unused"] = days_unused

    if days_unused >= CRITICAL_DAYS + GRACE_DAYS:
        event["status"] = "REVOKED"

    elif days_unused >= CRITICAL_DAYS:
        event["status"] = "PENDING_APPROVAL"

    elif days_unused >= WARNING_DAYS:
        event["status"] = "FLAGGED"

    return event