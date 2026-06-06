import random


def process_event(e):
    """
    Converts raw event → enriched IAM event
    Adds:
    - risk score
    - severity
    - default status
    """

    # ------------------------
    # RISK SCORE (simple model)
    # ------------------------
    score = random.randint(50, 100)

    # ------------------------
    # SEVERITY MAPPING
    # ------------------------
    if score >= 90:
        severity = "CRITICAL"
    elif score >= 75:
        severity = "HIGH"
    elif score >= 60:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    # ------------------------
    # FINAL EVENT STRUCTURE
    # ------------------------
    return {
        "timestamp": e.get("timestamp"),   # ✅ keep original
        "user": e.get("user"),
        "action": e.get("action"),
        "resource": e.get("resource"),

        "score": score,
        "severity": severity,

        "status": "ALLOWED",               # default
        "flags": "",                       # updated later
        "days_unused": 0                   # updated in decay
    }