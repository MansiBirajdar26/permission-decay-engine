# cloud_adapters/oci.py

DRY_RUN = True  # keep this true for safety
def revoke_permission(user, resource):
    # Mock OCI revoke (replace with real SDK later)
    print(f"🚫 Revoking {user}'s access to {resource} in OCI")


def revoke_permission(user_name, resource_name):
    print(f"\n🚨 REVOKE TRIGGERED: {user_name} → {resource_name}")

    if DRY_RUN:
        print("⚠️ DRY RUN → No real OCI action\n")
        return

    try:
        import oci

        config = oci.config.from_file()
        identity_client = oci.identity.IdentityClient(config)

        compartment_id = config["tenancy"]

        policies = identity_client.list_policies(compartment_id).data

        for policy in policies:
            updated_statements = []

            for stmt in policy.statements:
                if user_name in stmt and resource_name in stmt:
                    print(f"❌ Removing: {stmt}")
                    continue
                updated_statements.append(stmt)

            if len(updated_statements) != len(policy.statements):
                identity_client.update_policy(
                    policy_id=policy.id,
                    update_policy_details=oci.identity.models.UpdatePolicyDetails(
                        statements=updated_statements,
                        description=policy.description
                    )
                )

        print("✅ OCI POLICY UPDATED\n")

    except Exception as e:
        print("❌ OCI ERROR:", e)