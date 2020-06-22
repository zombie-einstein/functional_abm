def test_event_ordering():
    from functional_abm.event import Event

    e1 = Event(0, "A")
    e2 = Event(1, "A")

    assert e1 < e2
