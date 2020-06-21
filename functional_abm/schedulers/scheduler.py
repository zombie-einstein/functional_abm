from functional_abm.event import Event


class BaseScheduler:
    """
    Abstract scheduler class. Broadly a scheduler sorts events submitted
    by agents, and processing them in time order, updating the model/simulation
    at each step
    """

    def submit(self, event: Event):
        """
        Submit a event to be processed by the model

        Args:
            event (Event): New event
        """
        raise NotImplementedError

    def step(self):
        """
        Advance the model one step
        """
        raise NotImplementedError

    @property
    def finished(self) -> bool:
        """
        Flag indicating if the scheduler has completed execution

        Returns:
            bool: Flag indicating if the scheduler has completed execution
        """
        raise NotImplementedError
