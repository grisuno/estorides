"""M2a event_bus BDD red."""
from __future__ import annotations

import pytest


def test_subscribe_publish_order_and_count():
    from estorides_core.event_bus import EventBus

    bus = EventBus()
    seen: list[str] = []
    bus.subscribe("source_complete", lambda p: seen.append("a"))
    bus.subscribe("source_complete", lambda p: seen.append("b"))
    n = bus.publish("source_complete", {"source": "crtsh"})
    assert n == 2
    assert seen == ["a", "b"]


def test_raising_handler_does_not_block_others():
    from estorides_core.event_bus import EventBus

    def bad(p):
        raise RuntimeError("boom")

    seen: list[str] = []
    bus = EventBus()
    bus.subscribe("source_complete", bad)
    bus.subscribe("source_complete", lambda p: seen.append("ok"))
    n = bus.publish("source_complete", {"source": "crtsh"})
    assert n == 2
    assert seen == ["ok"]


def test_payload_isolation_between_handlers():
    from estorides_core.event_bus import EventBus

    seen: list[str] = []
    bus = EventBus()
    bus.subscribe("source_complete", lambda p: p.update({"x": 1}))
    bus.subscribe("source_complete", lambda p: seen.append(str(sorted(p.keys()))))
    bus.publish("source_complete", {"source": "crtsh"})
    assert seen == ["['source']"]


def test_invalid_inputs_raise():
    from estorides_core.event_bus import EventBus

    bus = EventBus()
    with pytest.raises(ValueError):
        bus.subscribe("", lambda p: None)
    with pytest.raises(TypeError):
        bus.subscribe("source_complete", "not-callable")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        bus.publish("source_complete", "nope")  # type: ignore[arg-type]


def test_singleton_and_unsubscribe():
    from estorides_core.event_bus import EventBus, get_bus

    assert get_bus() is get_bus()
    bus = EventBus()
    handler = lambda p: None  # noqa: E731
    bus.subscribe("run_finished", handler)
    assert bus.subscriber_count("run_finished") == 1
    assert bus.unsubscribe("run_finished", handler) is True
    assert bus.subscriber_count("run_finished") == 0
    assert bus.unsubscribe("run_finished", handler) is False
