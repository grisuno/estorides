# estorides_core: parsers

*Community 1 | 21 files | cohesion 0.44*

## Definition

This community groups 21 file(s) rooted at `estorides_core` with dominant language py (cohesion 0.44). Central symbols: `DiscoverJob`, `EventBus`, `KuzuGraphBackend`, `Orchestrator`, `PaginationConfig`, `PlatformInfo`, `ProfileMatch`, `RelationshipInferer`. Core file: `tests/test_socmint.py` (72 symbols). Documented purpose: Background subdomain/domain discoverer.  Drops a seed and walks the passive attack surface recursively. As of v1.3 the recursion itself lives in `pivot_engine.P.

## Files

### `estorides_core` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/discoverer.py` | py | utility | 21 | yes |
| `estorides_core/event_bus.py` | py | infrastructure | 9 | yes |
| `estorides_core/graph_kuzu.py` | py | utility | 11 | yes |
| `estorides_core/mitre_attack.py` | py | utility | 4 | yes |
| `estorides_core/orchestrator.py` | py | utility | 18 | yes |
| `estorides_core/pagination.py` | py | utility | 7 | yes |
| `estorides_core/parsers.py` | py | utility | 65 | yes |
| `estorides_core/relationship_inference.py` | py | utility | 16 | yes |
| `estorides_core/socmint.py` | py | utility | 12 | yes |
| `estorides_core/source_loader.py` | py | utility | 20 | yes |

### `tests` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_event_bus.py` | py | testing | 6 | yes |
| `tests/test_keyless_sources.py` | py | testing | 7 | yes |
| `tests/test_opsec_contact.py` | py | testing | 14 | yes |
| `tests/test_pagination.py` | py | testing | 38 | yes |
| `tests/test_socmint.py` | py | testing | 72 | yes |
| `tests/test_source_loader.py` | py | testing | 12 | yes |
| `tests/test_source_routing.py` | py | testing | 6 | yes |
| `tests/test_system_app_sources.py` | py | testing | 42 | yes |

### `tests/properties` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/properties/test_parsers_properties.py` | py | testing | 1 | yes |
| `tests/properties/test_system_app_sources_properties.py` | py | testing | 6 | yes |

*... and 1 more files in this community.*


## Key Symbols

- `DiscoverJob` (class, `estorides_core/discoverer.py:50`) `class DiscoverJob` - One background discovery session.
- `stop` (method, `estorides_core/discoverer.py:78`) `def stop(self)`
- `should_stop` (method, `estorides_core/discoverer.py:81`) `def should_stop(self)`
- `push_event` (method, `estorides_core/discoverer.py:84`) `def push_event(self, ev)` - Append an event and keep the buffer bounded.
- `_DiscoverJobSink` (class, `estorides_core/discoverer.py:95`) `class _DiscoverJobSink` - Adapts engine `PivotEvent`s to the legacy DiscoverJob event dicts.
- `__init__` (method, `estorides_core/discoverer.py:103`) `def __init__(self, job)`
- `emit` (method, `estorides_core/discoverer.py:106`) `def emit(self, event)`
- `_on_started` (method, `estorides_core/discoverer.py:113`) `def _on_started(self, data)`
- `_on_target_start` (method, `estorides_core/discoverer.py:116`) `def _on_target_start(self, data)`
- `_on_entity` (method, `estorides_core/discoverer.py:126`) `def _on_entity(self, data)`
- `_on_target_done` (method, `estorides_core/discoverer.py:141`) `def _on_target_done(self, data)`
- `_on_target_error` (method, `estorides_core/discoverer.py:153`) `def _on_target_error(self, data)`
- `_on_stopping` (method, `estorides_core/discoverer.py:160`) `def _on_stopping(self, data)`
- `_on_finished` (method, `estorides_core/discoverer.py:163`) `def _on_finished(self, data)`
- `_on_fatal` (method, `estorides_core/discoverer.py:174`) `def _on_fatal(self, data)`
- `_new_job_id` (function, `estorides_core/discoverer.py:189`) `def _new_job_id()` - Monotonic-ish id with a timestamp prefix for natural sort.
- `create_discover_job` (function, `estorides_core/discoverer.py:194`) `def create_discover_job(seed_type, seed_value)` - Create and register a discovery job synchronously.
- `start_discover` (function, `estorides_core/discoverer.py:252`) `def start_discover(seed_type, seed_value)` - Create a discovery job and schedule its worker on the current loop.
- `start_discover_threadsafe` (function, `estorides_core/discoverer.py:285`) `def start_discover_threadsafe(loop, seed_type, seed_value)` - Create the job in the calling thread, fire its worker on `loop`.
- `_run_discoverer` (function, `estorides_core/discoverer.py:319`) `def _run_discoverer(job)` - The background loop. One asyncio task per job, driving the engine.
- `list_jobs` (function, `estorides_core/discoverer.py:349`) `def list_jobs(limit)` - Snapshot of the recent jobs for the /api/discover/jobs endpoint.
- `EventBus` (class, `estorides_core/event_bus.py:24`) `class EventBus` - Synchronous in memory event channel with isolated delivery.
- `__init__` (method, `estorides_core/event_bus.py:27`) `def __init__(self)` - Create an empty bus with no subscribers.
- `subscribe` (method, `estorides_core/event_bus.py:31`) `def subscribe(self, event, handler)` - Register handler for event and return it for unsubscription.
- `unsubscribe` (method, `estorides_core/event_bus.py:41`) `def unsubscribe(self, event, handler)` - Remove handler from event and report whether it was present.
- `publish` (method, `estorides_core/event_bus.py:50`) `def publish(self, event, payload)` - Deliver a copy of payload to each subscriber and count attempts.
- `clear` (method, `estorides_core/event_bus.py:63`) `def clear(self, event)` - Remove subscribers for one event or for the whole bus.
- `subscriber_count` (method, `estorides_core/event_bus.py:71`) `def subscriber_count(self, event)` - Return the number of handlers registered for event.
- `_check_event` (method, `estorides_core/event_bus.py:76`) `def _check_event(self, event)` - Validate that an event name uses the constrained alphabet.
- `get_bus` (function, `estorides_core/event_bus.py:85`) `def get_bus()` - Return the process wide shared bus instance.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 50
- Cross-boundary resolved imports (EXTRACTED): 40

## Connections

- [EXTRACTED] depends_on community 4 <-> 1 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/orchestrator.py.
- [EXTRACTED] depends_on community 1 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_core/discoverer.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 1 <-> 0 (strength 0.9): Extracted import edge crosses communities: estorides_core/discoverer.py imports estorides_core/job_registry.py.
- [EXTRACTED] depends_on community 1 <-> 7 (strength 0.9): Extracted import edge crosses communities: estorides_core/orchestrator.py imports estorides_core/entity_extraction.py.
- [EXTRACTED] depends_on community 1 <-> 3 (strength 0.9): Extracted import edge crosses communities: estorides_core/orchestrator.py imports estorides_core/recon_fusion.py.
- [EXTRACTED] depends_on community 1 <-> 8 (strength 0.9): Extracted import edge crosses communities: estorides_core/system_app_sources.py imports estorides_core/tool_runner.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in estorides_core: parsers changed?
- Should estorides_core: parsers be split, given cohesion 0.44?

## Sources

- `estorides_core/discoverer.py`
- `estorides_core/event_bus.py`
- `estorides_core/graph_kuzu.py`
- `estorides_core/mitre_attack.py`
- `estorides_core/orchestrator.py`
- `estorides_core/pagination.py`
- `estorides_core/parsers.py`
- `estorides_core/relationship_inference.py`
- `estorides_core/socmint.py`
- `estorides_core/source_loader.py`
- `estorides_core/system_app_sources.py`
- `tests/properties/test_parsers_properties.py`
- `tests/properties/test_system_app_sources_properties.py`
- `tests/test_event_bus.py`
- `tests/test_keyless_sources.py`
- `tests/test_opsec_contact.py`
- `tests/test_pagination.py`
- `tests/test_socmint.py`
- `tests/test_source_loader.py`
- `tests/test_source_routing.py`
- *... and 1 more*
