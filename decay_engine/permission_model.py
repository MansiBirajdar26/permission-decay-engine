class Permission:
    def __init__(self, user, action, resource, timestamp):
        self.user = user
        self.action = action
        self.resource = resource
        self.timestamp = timestamp

        self.score = 0
        self.flags = []
        self.decision = "ALLOW"
        self.time_str = ""