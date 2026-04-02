import random
from datetime import datetime

# 🔥 YOUR REAL COMPARTMENT OCID
COMPARTMENT_ID = "ocid1.compartment.oc1..aaaaaaaasftpx47cqbleovqq6wp6ca3w5cvtig6esdgojpqnv7heeg67plga"

def generate_logs():
    users = ["Mansi", "test_user", "guest"]
    actions = ["CreateBucket", "DeleteBucket", "UpdatePolicy", "LaunchInstance"]

    events = []

    for _ in range(5):
        events.append({
            "user": random.choice(users),
            "action": random.choice(actions),
            "resource": COMPARTMENT_ID,   # 🔥 REAL OCI ID USED HERE
            "timestamp": str(datetime.now())
        })

    print(f"🚀 Generated {len(events)} events (OCI Compartment)")
    return events