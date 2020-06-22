def test_event_scheduler():
    from functional_abm.schedulers.step_based import StepBasedScheduler
    from functional_abm.event import Event

    scheduler = StepBasedScheduler(5)

    class MockAgent:
        def __init__(self):
            self.obs = 0
            self.upd = 0

        def observe(self):
            self.obs += 1

        def update(self, t):
            self.upd += 1

    assert scheduler.finished
    assert scheduler.t == 0

    a1 = MockAgent()
    a2 = MockAgent()

    scheduler.submit(Event(3, a1))
    scheduler.submit(Event(2, a2))
    scheduler.submit(Event(3, a2))
    scheduler.submit(Event(1, a2))

    scheduler.step()
    assert a1.upd == 0 and a1.obs == 0
    assert a2.upd == 0 and a2.obs == 0
    scheduler.step()
    assert a1.upd == 0 and a1.obs == 0
    assert a2.upd == 1 and a2.obs == 1
    scheduler.step()
    assert a1.upd == 0 and a1.obs == 0
    assert a2.upd == 2 and a2.obs == 2
    scheduler.step()
    assert a1.upd == 1 and a1.obs == 1
    assert a2.upd == 3 and a2.obs == 3

    assert scheduler.finished
