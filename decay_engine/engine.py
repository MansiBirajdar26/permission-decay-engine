def evaluate_decay(age_days, score, flags):
    if score >= 85:
        return "REVOKE"
    elif age_days > 30:
        return "REVOKE"
    elif age_days > 15:
        return "REDUCE"
    elif "RapidActivity" in flags:
        return "MONITOR"
    else:
        return "ALLOW"