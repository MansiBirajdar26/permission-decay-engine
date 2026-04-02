import time
from collector.oci_collector import fetch_audit_logs
from processing.permission_tracker import build_permissions
from engine.auto_revoke import auto_revoke_permission

print("🚀 IAM Scheduler Running...")

while True:
    try:
        print("\n🔄 Fetching OCI logs...")
        fetch_audit_logs()

        print("🧠 Running risk + decay engine...")
        permissions, _ = build_permissions()

        print("⚡ Executing auto-revoke...")
        for p in permissions:
            if p.auto_revoke and not p.revoked:
                auto_revoke_permission(p.user, p.action, p.resource)

        print("✅ Cycle complete")

    except Exception as e:
        print("❌ Scheduler error:", e)

    time.sleep(300)  # every 5 minutes