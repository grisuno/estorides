"""
estorides_core.event_bus
========================
In process publish subscribe channel for orchestrator lifecycle events.

I let metrics, SSE and future plugins observe runs without the
orchestrator importing them. Delivery is synchronous and total:
a failing subscriber never breaks a run and never mutates the
payload seen by the next subscriber.
"""
from __future__ import annotations

import logging
import re
from collections.abc import Callable
from typing import Any

log = logging.getLogger("estorides.event_bus")

_EVENT_RE = re.compile(r"[a-z_]{1,64}\Z")
Handler = Callable[[dict[str, Any]], None]


class EventBus:
    """Synchronous in memory event channel with isolated delivery."""

    def __init__(self) -> None:
        """Create an empty bus with no subscribers."""
        self._subs: dict[str, list[Handler]] = {}

    def subscribe(self, event: str, handler: Handler) -> Handler:
        """Register handler for event and return it for unsubscription."""
        self._check_event(event)
        if not callable(handler):
            raise TypeError("handler must be callable")
        handlers = self._subs.setdefault(event, [])
        if handler not in handlers:
            handlers.append(handler)
        return handler

    def unsubscribe(self, event: str, handler: Handler) -> bool:
        """Remove handler from event and report whether it was present."""
        self._check_event(event)
        handlers = self._subs.get(event, [])
        if handler in handlers:
            handlers.remove(handler)
            return True
        return False

    def publish(self, event: str, payload: dict[str, Any]) -> int:
        """Deliver a copy of payload to each subscriber and count attempts."""
        self._check_event(event)
        if not isinstance(payload, dict):
            raise TypeError("payload must be a dict")
        handlers = list(self._subs.get(event, []))
        for handler in handlers:
            try:
                handler(dict(payload))
            except Exception:
                log.exception("event handler failed")
        return len(handlers)

    def clear(self, event: str | None = None) -> None:
        """Remove subscribers for one event or for the whole bus."""
        if event is None:
            self._subs.clear()
            return
        self._check_event(event)
        self._subs.pop(event, None)

    def subscriber_count(self, event: str) -> int:
        """Return the number of handlers registered for event."""
        self._check_event(event)
        return len(self._subs.get(event, []))

    def _check_event(self, event: str) -> None:
        """Validate that an event name uses the constrained alphabet."""
        if not isinstance(event, str) or not _EVENT_RE.fullmatch(event):
            raise ValueError(f"invalid event name: {event!r}")


_BUS = EventBus()


def get_bus() -> EventBus:
    """Return the process wide shared bus instance."""
    return _BUS


__all__ = ["EventBus", "get_bus"]
