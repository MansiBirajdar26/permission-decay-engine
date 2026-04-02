import oci
from datetime import datetime, timedelta, timezone
from database.db_manager import insert_event


# 🔥 PUT YOUR REAL COMPARTMENT OCID HERE
COMPARTMENT_ID = "ocid1.compartment.oc1..aaaaaaaasftpx47cqbleovqq6wp6ca3w5cvtig6esdgojpqnv7heeg67plga"


def fetch_audit_logs():
    print("Fetching logs...")

    # ---- LOAD CONFIG ----
    config = oci.config.from_file()

    # 🔥 FORCE REGION (important)
    config["region"] = "ap-mumbai-1"

    print("Using region:", config["region"])
    print("Using compartment:", COMPARTMENT_ID)

    audit_client = oci.audit.AuditClient(config)

    # ---- TIME WINDOW ----
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=7)   # 🔥 INCREASED RANGE (IMPORTANT)

    print("Fetching logs from:", start_time, "to", end_time)

    events = []

    # ---- INITIAL FETCH ----
    response = audit_client.list_events(
        compartment_id=COMPARTMENT_ID,   # 🔥 FIXED HERE
        start_time=start_time,
        end_time=end_time
    )

    events.extend(response.data)

    # ---- PAGINATION ----
    while response.has_next_page:
        response = audit_client.list_events(
            compartment_id=COMPARTMENT_ID,
            start_time=start_time,
            end_time=end_time,
            page=response.next_page
        )
        events.extend(response.data)

    print(f"Total events fetched: {len(events)}")

    if not events:
        print("❌ No OCI events found")
        return

    inserted = 0
    skipped = 0

    # ---- PROCESS EVENTS ----
    for event in events:
        data = event.data

        event_name = getattr(data, "event_name", None)
        if not event_name:
            skipped += 1
            continue

        # 🔥 REMOVE USELESS NOISE
        if any(x in event_name for x in ["Health", "Metrics", "Summarize"]):
            skipped += 1
            continue

        event_time = event.event_time.isoformat()

        identity = getattr(data, "identity", None)

        user = (
            getattr(identity, "principal_name", None)
            or getattr(identity, "principal_id", None)
            or "OCI_USER"
        )

        action = getattr(data, "request_action", None) or event_name

        resource = (
            getattr(data, "resource_name", None)
            or getattr(data, "resource_id", None)
            or str(getattr(data, "request_parameters", None))
            or "UNKNOWN"
        )

        # ---- SAVE ----
        insert_event({
            "user": user,
            "action": action,
            "resource": resource,
            "timestamp": event_time
        })

        inserted += 1

    print(f"\n✅ Inserted: {inserted}")
    print(f"Skipped: {skipped}\n")