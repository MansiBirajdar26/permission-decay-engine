# ---------------- RBAC CONFIG ----------------

USER_ROLES = {
    "Mansi": "Admin",
    "test_user": "Developer",
    "guest": "Viewer"
}

ROLE_WEIGHT = {
    "Admin": 30,
    "Developer": 15,
    "Viewer": 5
}


# ---------------- ACTION RISK ----------------

ACTION_WEIGHT = {
    "DeleteBucket": 40,
    "CreateBucket": 20,
    "UpdatePolicy": 30,
    "LaunchInstance": 25
}


# ---------------- SCORE ENGINE ----------------

def calculate_score(event):
    base = 50

    # role impact
    role = USER_ROLES.get(event["user"], "Viewer")
    role_score = ROLE_WEIGHT.get(role, 5)

    # action impact
    action_score = ACTION_WEIGHT.get(event["action"], 10)

    score = base + role_score + action_score

    # cap at 100
    return min(score, 100)


# ---------------- SEVERITY ----------------

def get_severity(score):
    if score >= 90:
        return "CRITICAL"
    elif score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"


# ---------------- FLAGS ENGINE ----------------

def generate_flags(event, score):
    flags = []

    # risky actions
    if event["action"].startswith("Delete"):
        flags.append("Destructive Action")

    if event["action"] == "UpdatePolicy":
        flags.append("Policy Change")

    # high privilege user
    role = USER_ROLES.get(event["user"], "Viewer")
    if role == "Admin":
        flags.append("Privileged User")

    # high score
    if score >= 85:
        flags.append("Critical Risk")

    return flags


# ---------------- MAIN PROCESSOR ----------------

def process_event(event):
    """
    Input:
        {
            "user": str,
            "action": str,
            "resource": str,
            "timestamp": str
        }

    Output:
        processed event dict ready for DB
    """

    score = calculate_score(event)
    severity = get_severity(score)
    flags = generate_flags(event, score)

    return {
        "user": event["user"],
        "action": event["action"],
        "resource": event["resource"],
        "timestamp": event["timestamp"],
        "score": score,
        "severity": severity,
        "flags": ", ".join(flags) if flags else "None"
    }