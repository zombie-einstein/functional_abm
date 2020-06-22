from copy import copy
from typing import Any

from functional_abm.event import Event
from functional_abm.schedulers.scheduler import BaseScheduler


class _AgentNode:
    """
    Represent an agent and it's connections on the ABM processing graph

    An agent-node wraps an agent update function and links up input nodes
    (including the nodes previous state) and downstream nodes that can
    be altered by this node

    The node then handles the update calls made by the scheduler

    Attributes:
        agent_type (str): Agent type identifier
        scheduler (BaseScheduler): Reference to scheduler running the model
        t0: Time of the agents first scheduled event
        antecedents: Data structure containing references to nodes that act
            as inputs to this node, this will be passed as an argument to the
            wrapped node
        state: Reference to the state managed by this agent node
        descendants: Data structure containing references to nodes that can be
            changed by this node
    """

    agent_ids = set()
    counter = 0

    @staticmethod
    def f(t, antecedents, state, descendants):
        raise NotImplementedError

    def __init__(
        self,
        agent_type: str,
        scheduler: BaseScheduler,
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

        self.prev_antecedents = None

        # Submit first event
        self.scheduler.submit(Event(t0, self))

    def observe(self):
        """
        Updates the observed inputs for this node

        Copies the nodes state and state of antecedents
        """
        self.prev_antecedents = copy(self.antecedents)

    def update(self, t):
        """
        Update this node

        Calls the wrapped function passing the parameters stored as attributes
        of this node. It updates the nodes state, and those of it's
        descendants (where relevant)

        Args:
            t: The current simulated time (i.e. when the update
                event is called)
        """
        next_event_time = self.f(
            t, self.prev_antecedents, self.state, self.descendants
        )
        if next_event_time:
            self.scheduler.submit(Event(next_event_time, self))


def agent(*, scheduler: BaseScheduler):
    """
    Outer decorator calling inner node-wrapping decorator that produces
    an agent node type from an agent update function

    Args:
        scheduler (BaseScheduler): scheduler used to tun the simulation

    Returns:
        inner decorator
    """

    def inner_agent(f):
        """
        Inner decorator wrapping an agent update function to produce a new
        type representing agent nodes

        Args:
            f: Agent update function called but the new node type

        Returns (type): Agent node type
        """
        name = f.__name__
        new_type = type(name, (_AgentNode,), {"f": staticmethod(f)})

        def __init__(self, t, antecedents, state, descendants):
            super(new_type, self).__init__(
                name, scheduler, t, antecedents, state, descendants
            )

        new_type.__init__ = __init__
        return new_type

    return inner_agent
