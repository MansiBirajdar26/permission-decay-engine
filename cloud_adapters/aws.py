from cloud_adapters.aws import revoke_access


def enforce_policies(permissions):
    for p in permissions:
        if p.decision == "REVOKE":
            revoke_access(p.user, p.action)
            print(f"[AUTO] REVOKED {p.user} → {p.action}")

        elif p.decision == "REDUCE":
            print(f"[AUTO] REDUCED access for {p.user}")

        elif p.decision == "MONITOR":
            print(f"[AUTO] MONITORING {p.user}")