import oci
from database.db_manager import mark_as_revoked


def auto_revoke_permission(user, action, resource):
    print(f"\n🚨 AUTO-REVOKE TRIGGERED")
    print(f"User: {user}")
    print(f"Action: {action}")
    print(f"Resource: {resource}")

    try:
        config = oci.config.from_file()
        identity_client = oci.identity.IdentityClient(config)

        # 🔥 STEP 1: TRY TO MAP USER (SIMULATION)
        # In real system you would map:
        # username → OCID → group → policy

        print("🔍 Resolving user identity...")

        # ⚠️ OCI needs real OCIDs — we simulate structure
        print("⚠️ OCI mapping required (user → group → policy)")

        # 🔥 STEP 2: REALISTIC ACTION SIMULATION
        print("🔧 Simulating IAM action:")
        print("→ Remove user from privileged group")
        print("→ OR disable policy")

        # 🔥 EXAMPLE (REAL CALL — COMMENTED SAFE)
        # identity_client.remove_user_from_group(
        #     user_id="ocid1.user...",
        #     group_id="ocid1.group..."
        # )

        print("✅ IAM action simulated")

    except Exception as e:
        print("❌ OCI ERROR:", e)

    # 🔥 STEP 3: ALWAYS UPDATE DB
    mark_as_revoked(user, action, resource)

    print("✅ Marked as revoked in DB\n")

    return True