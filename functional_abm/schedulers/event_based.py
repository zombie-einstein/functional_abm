from queue import PriorityQueue

from functional_abm.schedulers.scheduler import BaseScheduler


class EventBasedScheduler(BaseScheduler):
    def __init__(self, max_t):
        self.max_t = max_t
        self.queue = PriorityQueue()
        self.t = 0

    def submit(self, event):
        self.queue.put(event)

    def step(self):
        e = self.queue.get()
        self.t = e.t
        e.agent.update(self.t)

    @property
    def finished(self):
        return self.queue.empty() or self.t >= self.max_t
