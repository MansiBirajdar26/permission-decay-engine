import oci
from datetime import datetime


def fetch_oci_events():
    """
    Fetch basic OCI events (simulated minimal real integration)
    """

    try:
        config = oci.config.from_file()
        identity_client = oci.identity.IdentityClient(config)

        compartment_id = config["tenancy"]

        users = identity_client.list_users(compartment_id).data

        events = []

        for u in users[:5]:  # limit to avoid spam
            events.append({
                "user": u.name,
                "action": "Login",
                "resource": "OCI Console",
                "timestamp": datetime.now().isoformat()
            })

        print(f"🚀 Fetched {len(events)} OCI users")

        return events

    except Exception as e:
        print("❌ OCI fetch failed, falling back to demo:", str(e))

        return []