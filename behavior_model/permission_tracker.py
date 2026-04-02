def process_event(event):
    score = 0
    flags = []

    action = event["action"]

    if "Delete" in action:
        score += 40
        flags.append("Destructive Action")

    if "Policy" in action:
        score += 30
        flags.append("Policy Change")

    if "Launch" in action:
        score += 20

    if "Create" in action:
        score += 10

    if score >= 90:
        severity = "CRITICAL"
    elif score >= 70:
        severity = "HIGH"
    elif score >= 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    event["score"] = score
    event["severity"] = severity
    event["flags"] = ", ".join(flags) if flags else ""

    return event