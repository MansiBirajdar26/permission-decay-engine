from database.db_manager import insert_event, init_db
from datetime import datetime, timedelta
import random

init_db()

now = datetime.utcnow()

users = ["Mansi", "test_user", "admin", "dev", "analyst", "guest"]
actions = [
    "CreateBucket", "DeleteBucket", "UpdatePolicy",
    "LaunchInstance", "AttachRole", "ReadObject",
    "WriteObject", "ListBuckets"
]
resources = ["bucket1", "bucket2", "policy1", "vm1", "role1", "bucket3", "all"]

# 🔥 generate MANY events
for i in range(30):
    user = random.choice(users)
    action = random.choice(actions)
    resource = random.choice(resources)

    time = (now - timedelta(hours=i)).isoformat()

    insert_event(time, user, action, resource)

print("✅ 30 events inserted")