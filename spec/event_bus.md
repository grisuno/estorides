# event_bus — Spec

## Purpose
I decouple the orchestrator fanout from SSE, metrics and future plugins. A single in process bus replaces direct callbacks and polling. I use only stdlib and I never block a run when a subscriber fails.

## Inputs
- `bus.subscribe(event, handler)` where handler takes one dict payload and returns None. Same handler subscribed twice runs once.
- `bus.publish(event, payload)` delivers a copy to each handler in subscribe order.
- `bus.clear(event=None)` removes handlers for one event or all.
- Events: `source_complete`, `run_finished`. Payload is a plain JSON safe dict.

## Outputs
- `EventBus` class with `subscribe`, `unsubscribe`, `publish`, `clear`, `subscriber_count`.
- `get_bus()` returns the process wide singleton.
- `publish` returns delivery count. A raising handler is caught and logged, delivery continues.

## Error table
| Condition | Behaviour |
|---|---|
| empty event name | ValueError |
| handler not callable | TypeError |
| handler raises | caught, logged via logging, remaining handlers still run |
| payload not dict | TypeError, nothing delivered |
| unsubscribe unknown | no-op, returns False |

## Security guarantees
- No eval, no exec, no subprocess, no socket, no threads spawned. Synchronous delivery only so ordering stays deterministic.
- Payload is shallow copied per handler so one subscriber cannot mutate the dict seen by the next.
- Event names constrained to `[a-z_]{1,64}` so a hostile source name cannot become an event channel.

## Out of scope
- Cross process or network bus, Redis, Celery, persistence, replay, async delivery. Single user runs in one process.

## BDD scenarios
- Given a fresh bus, when two handlers subscribe to `source_complete` and one publishes, then both run in order and count is 2.
- Given a raising handler plus a good one, when publish runs, then the good one still runs and count is 2.
- Given a payload dict, when two handlers mutate it, then the second sees the original values.
- Given an invalid event name or payload, when called, then it raises ValueError or TypeError and delivers nothing.
- Given the global singleton, when orchestrator finishes a source, then `record_source` and SSE can subscribe without touching orchestrator code.
- Given unsubscribe, when removed then it no longer runs and count drops.
