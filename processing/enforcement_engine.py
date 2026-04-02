def enforce_policy(event):
    if event["score"] >= 90:
        return "REVOKED"
    elif event["score"] >= 70:
        return "FLAGGED"
    return "ALLOWED"