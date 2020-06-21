from copy import copy
from typing import Any, Tuple

from functional_abm.event import Event


class _AgentNode:

    agent_ids = set()
    counter = 0

    @staticmethod
    def f(t, antecedents, state, descendants) -> Tuple:
        raise NotImplementedError

    def __init__(
        self,
        agent_type: str,
        scheduler,
        t0,
        antecedents: Any,
        state: Any,
        descendants: Any,
    ):

        self.id = f"{agent_type}_{self.__class__.counter:#0{6}x}"
        self.__class__.agent_ids.add(self.id)
        self.__class__.counter += 1

        self.antecedents = antecedents
        self.state = state
        self.descendants = descendants
        self.scheduler = scheduler

        self.prev_state = None
        self.prev_antecedents = None

        # Submit first event
        self.scheduler.submit(Event(t0, self))

    def observe(self):
        self.prev_state = copy(self.state)
        self.prev_antecedents = copy(self.antecedents)

    def update(self, t):
        new_state, new_descendants, next_event_time = self.f(
            t, self.prev_antecedents, self.prev_state, self.descendants
        )
        self.state = new_state

        for k, v in new_descendants.items():
            self.descendants[k] = v

        if next_event_time:
            self.scheduler.submit(Event(next_event_time, self))


def agent(*, scheduler):
    def inner_agent(f):
        name = f.__name__
        new_type = type(name, (_AgentNode,), {"f": staticmethod(f)})

        def __init__(self, t, antecedents, state, descendants):
            super(new_type, self).__init__(
                name, scheduler, t, antecedents, state, descendants
            )

        new_type.__init__ = __init__
        return new_type

    return inner_agent
