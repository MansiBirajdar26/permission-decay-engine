from collections import defaultdict


class AnomalyEngine:
    def __init__(self):
        self.user_actions = defaultdict(list)

    def detect(self, user, action):
        history = self.user_actions[user]

        # Learn baseline first
        if len(history) < 5:
            history.append(action)
            return False

        # New unseen action → anomaly
        if action not in history:
            history.append(action)
            return True

        history.append(action)
        return False