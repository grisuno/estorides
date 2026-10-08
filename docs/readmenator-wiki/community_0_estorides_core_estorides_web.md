# estorides_core: estorides_web

*Community 0 | 25 files | cohesion 0.48*

## Definition

This community groups 25 file(s) rooted at `tests` with dominant language py (cohesion 0.48). Central symbols: `AuditEvent`, `AuditLog`, `AuthGate`, `BoundedJobRegistry`, `BufferedEventSink`, `DiscoverJob`, `EntityRunner`, `EventSink`. Core file: `estorides_web.py` (94 symbols). Documented purpose: Deprecated entry point. Use:  - the `estorides` console script (installed by `pip install -e .`), or - `python3 estorides_cli.py serve` for the dev server, or -.

## Files

### `tests` (9 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_audit_log.py` | py | testing | 5 | yes |
| `tests/test_auth_gate.py` | py | testing | 10 | yes |
| `tests/test_csp_safe_styles.py` | py | testing | 11 | yes |
| `tests/test_job_registry.py` | py | testing | 8 | yes |
| `tests/test_map_basemap.py` | py | testing | 5 | yes |
| `tests/test_openapi.py` | py | testing | 1 | yes |

### `estorides_core` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/audit.py` | py | utility | 11 | yes |
| `estorides_core/discoverer.py` | py | utility | 21 | yes |
| `estorides_core/graph_kuzu.py` | py | utility | 11 | yes |
| `estorides_core/job_registry.py` | py | utility | 10 | yes |
| `estorides_core/openapi.py` | py | utility | 1 | yes |
| `estorides_core/pivot_engine.py` | py | utility | 25 | yes |

### `.` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `app.py` | py | utility | 0 | yes |
| `estorides_web.py` | py | presentation | 94 | yes |
| `estorides_web_tools.py` | py | presentation | 5 | yes |
| `web.py` | py | utility | 0 | yes |
| `wsgi.py` | py | utility | 0 | yes |

### `tests/properties` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/properties/test_csp_safe_styles_properties.py` | py | testing | 3 | yes |
| `tests/properties/test_search_telemetry_properties.py` | py | testing | 6 | yes |

### `tools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tools/sync_docs.py` | py | utility | 2 | yes |

*... and 5 more files in this community.*


## Key Symbols

- `AuditEvent` (class, `estorides_core/audit.py:55`) `class AuditEvent`
- `to_jsonl` (method, `estorides_core/audit.py:68`) `def to_jsonl(self)`
- `AuditLog` (class, `estorides_core/audit.py:72`) `class AuditLog` - Append-only JSONL audit log with a size cap.
- `__init__` (method, `estorides_core/audit.py:90`) `def __init__(self, path)`
- `record` (method, `estorides_core/audit.py:104`) `def record(self, event)`
- `_maybe_rotate_locked` (method, `estorides_core/audit.py:115`) `def _maybe_rotate_locked(self)` - If the active file is over the cap, rotate in place.
- `query` (method, `estorides_core/audit.py:150`) `def query(self, event)`
- `RateLimiter` (class, `estorides_core/audit.py:180`) `class RateLimiter` - In-process sliding-window rate limiter.
- `__init__` (method, `estorides_core/audit.py:201`) `def __init__(self)`
- `allow` (method, `estorides_core/audit.py:214`) `def allow(self, key)` - Return (allowed, retry_after_seconds).
- `reset` (method, `estorides_core/audit.py:238`) `def reset(self, key)`
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
- `_new_job_id` (method, `estorides_core/discoverer.py:189`) `def _new_job_id()` - Monotonic-ish id with a timestamp prefix for natural sort.
- `create_discover_job` (method, `estorides_core/discoverer.py:194`) `def create_discover_job(seed_type, seed_value)` - Create and register a discovery job synchronously.
- `start_discover` (method, `estorides_core/discoverer.py:252`) `def start_discover(seed_type, seed_value)` - Create a discovery job and schedule its worker on the current loop.
- `start_discover_threadsafe` (method, `estorides_core/discoverer.py:285`) `def start_discover_threadsafe(loop, seed_type, seed_value)` - Create the job in the calling thread, fire its worker on `loop`.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 39
- Cross-boundary resolved imports (EXTRACTED): 41

## Connections

- [EXTRACTED] depends_on community 5 <-> 0 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/discoverer.py.
- [EXTRACTED] depends_on community 0 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_core/audit.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 0 <-> 1 (strength 0.9): Extracted import edge crosses communities: estorides_core/discoverer.py imports estorides_core/orchestrator.py.

## Risks

- [cycle] `estorides_web.py` -> `estorides_web_tools.py` -> `estorides_web.py`
- [layer strict] `estorides_web.py` (presentation) -> `estorides_core/fusion_store.py` (data_access)
- [layer strict] `tests/properties/test_csp_safe_styles_properties.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_auth_gate.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_auth_gate.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_csp_safe_styles.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_csp_safe_styles.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_hardening.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_map_basemap.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_openapi.py` (testing) -> `estorides_web.py` (presentation)
- [layer strict] `tests/test_security_remediation.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_web_helpers.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_web_helpers.py` (testing) -> `estorides_web.py` (presentation)
- [layer strict] `tests/test_web_tools_blueprint.py` (testing) -> `estorides_web.py` (presentation)
- [layer strict] `tests/test_web_tools_blueprint.py` (testing) -> `estorides_web.py` (presentation)

## Open Questions

- Can the cycle `estorides_web.py` -> `estorides_web_tools.py` be broken with an interface?
- What would break if the most connected file in estorides_core: estorides_web changed?
- Should estorides_core: estorides_web be split, given cohesion 0.48?

## Sources

- `app.py`
- `estorides_core/audit.py`
- `estorides_core/discoverer.py`
- `estorides_core/graph_kuzu.py`
- `estorides_core/job_registry.py`
- `estorides_core/openapi.py`
- `estorides_core/pivot_engine.py`
- `estorides_core/search_telemetry.py`
- `estorides_core/web_security.py`
- `estorides_web.py`
- `estorides_web_tools.py`
- `tests/properties/test_csp_safe_styles_properties.py`
- `tests/properties/test_search_telemetry_properties.py`
- `tests/test_audit_log.py`
- `tests/test_auth_gate.py`
- `tests/test_csp_safe_styles.py`
- `tests/test_job_registry.py`
- `tests/test_map_basemap.py`
- `tests/test_openapi.py`
- `tests/test_search_telemetry.py`
- *... and 5 more*
