def enforce_policy(event):

    if event.get("status") == "PENDING_APPROVAL":
        return "PENDING_APPROVAL"

    if event["score"] >= 90:
        return "REVOKED"

    if event["score"] >= 70:
        return "FLAGGED"

    return "ALLOWED"