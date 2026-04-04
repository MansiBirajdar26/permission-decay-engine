from collector.log_generator import generate_logs
from processing.permission_tracker import process_event
from processing.enforcement_engine import enforce_policy
from processing.decay_engine import apply_decay
from database.db_manager import insert_event
import time


def start_stream():
    print("🔥 Real-time stream started...")

    while True:
        events = generate_logs()

        for e in events:
            processed = process_event(e)

            # 🔥 APPLY DECAY FIRST
            processed = apply_decay(processed)

            # 🔥 ENFORCEMENT ONLY IF NOT REVOKED BY DECAY
            if processed.get("status") != "REVOKED":
                processed["status"] = enforce_policy(processed)

            insert_event(processed)

        time.sleep(5)