class BaseScheduler:
    def submit(self, event):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError

    @property
    def finished(self):
        raise NotImplementedError
