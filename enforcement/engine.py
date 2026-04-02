from processing.permission_tracker import build_permissions
from database.db_manager import mark_as_revoked


def enforce_policies():
    permissions, _ = build_permissions()

    revoked_count = 0

    for p in permissions:
        # 🔥 AUTO-REVOKE CONDITION
        if p.decision == "AUTO-REVOKE":
            mark_as_revoked(p.user, p.action, p.resource)
            revoked_count += 1
            print(f"🔥 AUTO-REVOKED: {p.user} | {p.action} | {p.resource}")

    print(f"✅ Enforcement complete. Revoked: {revoked_count}")