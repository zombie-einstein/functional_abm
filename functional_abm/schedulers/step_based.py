from functional_abm.schedulers.scheduler import BaseScheduler


class StepBasedScheduler(BaseScheduler):
    def __init__(self, max_t):
        self.max_t = max_t
        self.events = []
        self.t = 0

    def submit(self, event):
        if len(self.events) < event.t + 1:
            self.events += [[] for _ in range(event.t + 1 - len(self.events))]
        self.events[event.t].append(event)

    def step(self):
        for e in self.events[self.t]:
            e.agent.observe()
        for e in self.events[self.t]:
            e.agent.update(self.t)
        self.t += 1

    @property
    def finished(self):
        return self.t >= self.max_t
