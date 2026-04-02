from datetime import datetime

CRITICAL_DAYS = 30
WARNING_DAYS = 15


def apply_decay(event):
    try:
        last_used = datetime.fromisoformat(event["timestamp"])
    except:
        event["days_unused"] = 0
        return event

    now = datetime.now()
    days_unused = (now - last_used).days

    event["days_unused"] = days_unused

    # DECAY RULES
    if days_unused >= CRITICAL_DAYS:
        event["status"] = "REVOKED"
        event["flags"] += ", Inactive >30d"

    elif days_unused >= WARNING_DAYS:
        event["status"] = "FLAGGED"
        event["flags"] += ", Inactive >15d"

    return event