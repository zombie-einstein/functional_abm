class Event:
    """
    Data object containing a time and a reference to an agent that will
    be processed at that timestamp

    Events are designed to be used to schedule the processing of events in the
    model, the attribute `t` is used to order events (in ascending order)
    and can be thought of as representing a simulated time

    Attributes:
        t (Any): Time-stamp of event. The type used for `t` should be
            comparable (i.e. sortable)
        agent (Any): Reference to agent/function/object attached to this event
    """

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
