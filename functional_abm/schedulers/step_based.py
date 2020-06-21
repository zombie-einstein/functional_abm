from functional_abm.schedulers.scheduler import BaseScheduler


class StepBasedScheduler(BaseScheduler):
    """
    Scheduler designed to run step-based models where events can only occur
    at fixed time-steps

    Internally tracks events to be executed as a nested array, extending to
    accommodate events as they are submitted

    If the event scheduler is used then event times must be represented
    by integers (i.e. the simulation/model step the event will occur)

    As opposed to the event-based scheduler the step based scheduler can
    update several agents over the same step

    Attributes:
        max_t (int): Maximum allowed time-step. The scheduler will run until
            this max time, or there are no more events available
        events (list): Array of bins for each step of the model
        t (int): Current model step
    """

    def __init__(self, max_t):
        self.max_t = max_t
        self.events = []
        self.t = 0

    def submit(self, event):
        """
        Submit a new event to be processed by the scheduler

        Args:
            event (Event): Event to be inserted into the processing array
        """
        if len(self.events) < event.t + 1:
            self.events += [[] for _ in range(event.t + 1 - len(self.events))]
        self.events[event.t].append(event)

    def step(self):
        """
        Update one step of the model, updating all agents with events
        scheduled for the current step

        At each update all the agents first update their observation of the
        current state of the model, then update their state
        """
        for e in self.events[self.t]:
            e.agent.observe()
        for e in self.events[self.t]:
            e.agent.update(self.t)
        self.t += 1

    @property
    def finished(self) -> bool:
        """
        Flag if the scheduler has reached the end of the events, either when
        no more events are available or the max number of steps has
        been reached

        Returns:
            bool: True if no more events remain or the ma number of steps
                has been reached
        """
        return self.t >= self.max_t
