from config import MODE
from database.db_manager import init_db
from behavior_model.permission_tracker import build_permissions

def run_real_mode():
    from collector.oci_collector import fetch_audit_logs
    print("🔵 Running in REAL mode (OCI logs)")
    fetch_audit_logs()

def run_demo_mode():
    from scripts.event_generater import generate_events_once
    print("🟡 Running in DEMO mode (simulated logs)")
    generate_events_once()


if __name__ == "__main__":
    init_db()

    if MODE == "REAL":
        run_real_mode()
    else:
        run_demo_mode()

    print("\nTracking permissions...\n")
    build_permissions()