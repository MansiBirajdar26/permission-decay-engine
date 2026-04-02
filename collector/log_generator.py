import random
from datetime import datetime, timedelta

COMPARTMENT_ID = "ocid1.compartment.oc1..aaaaaaaasftpx47cqbleovqq6wp6ca3w5cvtig6esdgojpqnv7heeg67plga"


def generate_logs():
    users = ["Mansi", "admin", "guest", "dev"]
    actions = ["CreateBucket", "DeleteBucket", "UpdatePolicy", "LaunchInstance"]

    events = []

    for _ in range(5):
        # 🔥 simulate past usage (important for decay)
        random_days = random.randint(0, 40)
        timestamp = datetime.now() - timedelta(days=random_days)

        events.append({
            "user": random.choice(users),
            "action": random.choice(actions),
            "resource": COMPARTMENT_ID,
            "timestamp": timestamp.isoformat()
        })

    return events