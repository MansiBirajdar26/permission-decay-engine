# behavior_model/user_risk.py

from collections import defaultdict


class UserRiskEngine:

    def __init__(self):
        self.user_profiles = defaultdict(lambda: {
            "actions": 0,
            "total_score": 0,
            "destructive": 0,
            "policy_changes": 0,
            "flags": set()
        })

    def update_user(self, user, action, score, flags):
        profile = self.user_profiles[user]

        profile["actions"] += 1
        profile["total_score"] += score

        if "Delete" in action:
            profile["destructive"] += 1

        if "UpdatePolicy" in action:
            profile["policy_changes"] += 1

        for f in flags:
            profile["flags"].add(f)

    def classify_user(self, profile):
        avg_score = profile["total_score"] / max(profile["actions"], 1)

        if profile["destructive"] >= 2 or profile["policy_changes"] >= 2:
            return "CRITICAL USER"

        elif avg_score >= 75:
            return "HIGH RISK USER"

        elif avg_score >= 45:
            return "MEDIUM USER"

        else:
            return "LOW USER"

    def build_profiles(self):
        results = {}

        for user, profile in self.user_profiles.items():
            avg_score = profile["total_score"] / max(profile["actions"], 1)

            results[user] = {
                "level": self.classify_user(profile),
                "avg_score": int(avg_score),
                "actions": profile["actions"],
                "flags": list(profile["flags"])
            }

        return results