def enforce_policy(event):
    """
    Decide enforcement action based on score
    NO DB CALLS HERE
    """

    if event["score"] >= 90:
        return "REVOKED"

    elif event["score"] >= 70:
        return "FLAGGED"

    return "ALLOWED"