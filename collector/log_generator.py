import random
from datetime import datetime


def generate_logs():
    users = ["admin", "dev", "guest", "analyst"]
    actions = ["CreateBucket", "DeleteBucket", "UpdatePolicy", "Login"]
    resources = ["vm1", "bucket1", "policy1"]

    events = []

    for _ in range(5):
        events.append({
            "user": random.choice(users),
            "action": random.choice(actions),
            "resource": random.choice(resources),
            "timestamp": datetime.now().isoformat()
        })

    return events