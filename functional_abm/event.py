class Event:
    __slots__ = "t", "agent"

    def __init__(self, t, agent):
        self.t = t
        self.agent = agent

    def __lt__(self, obj):
        return self.t < obj.t

    def __le__(self, obj):
        return self.t <= obj.t

    def __eq__(self, obj):
        return self.t == obj.t

    def __ne__(self, obj):
        return self.t != obj.t

    def __gt__(self, obj):
        return self.t > obj.t

    def __ge__(self, obj):
        return self.t >= obj.t
