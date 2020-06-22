def test_event_scheduler():
    from functional_abm.schedulers.event_based import EventBasedScheduler
    from functional_abm.event import Event

    scheduler = EventBasedScheduler(5)

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

    scheduler.submit(Event(0.3, a1))
    scheduler.submit(Event(0.2, a2))
    scheduler.submit(Event(0.4, a1))
    scheduler.submit(Event(0.1, a2))
    scheduler.submit(Event(0.5, a1))

    scheduler.step()
    assert scheduler.t == 0.1
    assert a1.upd == 0 and a1.obs == 0
    assert a2.upd == 1 and a2.obs == 1
    scheduler.step()
    assert scheduler.t == 0.2
    assert a1.upd == 0 and a1.obs == 0
    assert a2.upd == 2 and a2.obs == 2
    scheduler.step()
    assert scheduler.t == 0.3
    assert a1.upd == 1 and a1.obs == 1
    assert a2.upd == 2 and a2.obs == 2
    scheduler.step()
    assert scheduler.t == 0.4
    assert a1.upd == 2 and a1.obs == 2
    assert a2.upd == 2 and a2.obs == 2
    scheduler.step()
    assert scheduler.t == 0.5
    assert a1.upd == 3 and a1.obs == 3
    assert a2.upd == 2 and a2.obs == 2

    assert scheduler.finished
