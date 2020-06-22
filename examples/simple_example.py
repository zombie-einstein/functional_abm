from functional_abm.agent import agent
from functional_abm.schedulers.step_based import StepBasedScheduler


class AgentState:
    def __init__(self, name: str):
        self.name = name
        self.value = 0


def model():

    scheduler = StepBasedScheduler(20)

    @agent(scheduler=scheduler)
    def simple_agent(t, antecedents, state, descendants):
        print(f"Agent: {state.name}, Value: {state.value}, t: {t}")
        state.value += 1
        return t + 2

    agent_state_1 = AgentState("A")
    agent_state_2 = AgentState("B")

    simple_agent(0, [], agent_state_1, {})
    simple_agent(1, [], agent_state_2, {})

    while not scheduler.finished:
        scheduler.step()


model()
