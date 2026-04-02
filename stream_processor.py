from collector.log_generator import generate_logs
from behavior_model.permission_tracker import process_event
from processing.enforcement_engine import enforce_policy
from database.db_manager import insert_event
import time

def start_stream():
    print("🔥 Real-time stream started...")

    while True:
        events = generate_logs()

        for e in events:
            # 1. Process (score + severity)
            processed = process_event(e)

            # 2. Decide enforcement
            status = enforce_policy(processed)
            processed["status"] = status

            # 3. Insert into DB (NOW safe)
            insert_event(processed)

        time.sleep(5)