def auto_revoke(event):

    if event.get("status") == "REVOKED":
        print(f"🚨 AUTO-REVOKED: {event['user']} | {event['action']}")

    return event