from queue import PriorityQueue

from functional_abm.schedulers.scheduler import BaseScheduler


class EventBasedScheduler(BaseScheduler):
    """
    Scheduler designed to execute individual agent events in turn

    As opposed to the step-based scheduler, the event-based scheduler
    updates agents in turn and times can be represented by arbitrary types
    as long as they are comparable (e.g. datetimes, floats)

     Attributes:
         max_t: Maximum time the model is allowed to run up to
         queue: Priority queue used to sort events for processing
         t: Current mode time (i.e. the time of the current/last
            processed event)
    """

    def __init__(self, max_t):
        self.max_t = max_t
        self.queue = PriorityQueue()
        self.t = 0

    def submit(self, event):
        """
        Submit a new event to be processed by the scheduler

        Submitted events are placed in sorted order in the processing queue

        Args:
            event (Event): Event to be inserted into the processing queue
        """
        self.queue.put(event)

    def step(self):
        """
        Run one step of the model

        Takes the next event from the queue and updates the relevant agent
        """
        e = self.queue.get()
        self.t = e.t
        e.agent.observe()
        e.agent.update(self.t)

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
        return self.queue.empty() or self.t >= self.max_t
