from collector.log_generator import generate_logs
from collector.oci_collector import fetch_oci_events
from processing.permission_tracker import process_event
from processing.decay_engine import apply_decay
from processing.enforcement_engine import enforce_policy
from processing.revoke_engine import auto_revoke
from database.db_manager import insert_event
import time

# 🔥 CHANGE THIS
MODE = "DEMO"   # "DEMO" or "REAL"


def start_stream():
    print(f"🔥 Stream started in {MODE} mode...")

    while True:

        # ------------------------
        # DATA SOURCE
        # ------------------------
        if MODE == "REAL":
            events = fetch_oci_events()
        else:
            events = generate_logs()

        # ------------------------
        # PIPELINE
        # ------------------------
        for e in events:
            event = process_event(e)

            event = apply_decay(event)

            if event.get("status") != "REVOKED":
                event["status"] = enforce_policy(event)

            event = auto_revoke(event)

            insert_event(event)

        time.sleep(5)