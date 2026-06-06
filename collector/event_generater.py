from database.db_manager import insert_event
from datetime import datetime
import random

def generate_events_once():
    users = ["demo_user", "tester"]
    actions = ["CreateBucket", "DeleteBucket", "UpdatePolicy"]
    resources = ["bucket-x", "policy-y"]

    for _ in range(20):
        insert_event(
            datetime.utcnow().isoformat(),
            random.choice(users),
            random.choice(actions),
            random.choice(resources)
        )