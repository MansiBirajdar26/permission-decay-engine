import requests

WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"


def send_alert(permission):
    print("\n🚨 ALERT 🚨")
    print(f"Time: {permission.time_str}")
    print(f"User: {permission.user}")
    print(f"Action: {permission.action}")
    print(f"Resource: {permission.resource}")
    print(f"Score: {permission.score}")
    print("------------------------")

    try:
        requests.post(WEBHOOK_URL, json={
            "text": f"""🚨 IAM ALERT
Time: {permission.time_str}
User: {permission.user}
Action: {permission.action}
Score: {permission.score}
"""
        })
    except:
        pass