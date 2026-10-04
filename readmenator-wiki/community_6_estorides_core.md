# estorides_core

*Community 6 | 43 files | cohesion 0.55*

## Definition

This community groups 43 file(s) rooted at `estorides_core` with dominant language py (cohesion 0.55). Central symbols: `AnthropicBackend`, `CacheConfig`, `CanonicalEntity`, `EntityResolver`, `EntityStore`, `EventBus`, `FusionResult`, `GroupedEntity`. Core file: `tests/test_socmint.py` (72 symbols). Documented purpose: estorides.config.

## Files

### `estorides_core` (17 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/config.py` | py | infrastructure | 26 | yes |
| `estorides_core/entity_resolution.py` | py | business_logic | 35 | yes |
| `estorides_core/entity_store.py` | py | business_logic | 5 | yes |
| `estorides_core/event_bus.py` | py | infrastructure | 9 | yes |
| `estorides_core/mitre_attack.py` | py | utility | 4 | yes |
| `estorides_core/observation_models.py` | py | business_logic | 14 | yes |

### `tests` (17 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_config_env.py` | py | testing | 13 | yes |
| `tests/test_entity_resolution.py` | py | testing | 68 | yes |
| `tests/test_event_bus.py` | py | testing | 6 | yes |
| `tests/test_keyless_sources.py` | py | testing | 7 | yes |
| `tests/test_observation_models.py` | py | testing | 28 | yes |
| `tests/test_ops_observability.py` | py | testing | 6 | yes |

### `tests/properties` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/properties/test_observation_models_properties.py` | py | testing | 7 | yes |
| `tests/properties/test_parsers_properties.py` | py | testing | 1 | yes |
| `tests/properties/test_recon_fusion_properties.py` | py | testing | 17 | yes |
| `tests/properties/test_search_telemetry_properties.py` | py | testing | 6 | yes |
| `tests/properties/test_system_app_sources_properties.py` | py | testing | 6 | yes |

### `estorides_llm` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_llm/__init__.py` | py | utility | 0 | yes |
| `estorides_llm/intelligence_prompts.py` | py | utility | 1 | yes |
| `estorides_llm/manager.py` | py | utility | 22 | yes |

*... and 23 more files in this community.*


## Key Symbols

- `ensure_data_dirs` (function, `estorides_core/config.py:58`) `def ensure_data_dirs()` - Idempotently create DATA_DIR.
- `ensure_reports_dir` (function, `estorides_core/config.py:69`) `def ensure_reports_dir()` - Idempotently create REPORTS_DIR.
- `_env_tool_allowlist` (function, `estorides_core/config.py:126`) `def _env_tool_allowlist()`
- `contact_level` (function, `estorides_core/config.py:205`) `def contact_level(contact)` - Map a contact class to its numeric severity, unknown values to active.
- `effective_proxies` (function, `estorides_core/config.py:231`) `def effective_proxies(explicit)` - Resolve the proxy rotation pool from an explicit value or the env.
- `CacheConfig` (class, `estorides_core/config.py:365`) `class CacheConfig` - Disk response-cache behaviour.
- `is_active` (method, `estorides_core/config.py:372`) `def is_active(self)` - Cache is only consulted when enabled and the TTL is positive.
- `PivotPolicyConfig` (class, `estorides_core/config.py:378`) `class PivotPolicyConfig` - Which entity types are worth pivoting on, and how leads are scored.
- `is_pivotable` (method, `estorides_core/config.py:392`) `def is_pivotable(self, entity_type)` - True when an entity of `entity_type` should be re-queried.
- `lead_score` (method, `estorides_core/config.py:396`) `def lead_score(self, entity_type, depth, parent_score)` - Priority of expanding this lead. Higher expands sooner.
- `PivotConfig` (class, `estorides_core/config.py:403`) `class PivotConfig` - Bounds and defaults for the recursive pivot engine.
- `clamp_depth` (method, `estorides_core/config.py:426`) `def clamp_depth(self, value)` - Clamp a requested depth into [1, max_depth_cap].
- `clamp_steps` (method, `estorides_core/config.py:430`) `def clamp_steps(self, value)` - Clamp a requested step budget into [1, max_steps_cap].
- `clamp_entities` (method, `estorides_core/config.py:434`) `def clamp_entities(self, value)` - Clamp a requested entity budget into [1, max_entities_cap].
- `clamp_parallel` (method, `estorides_core/config.py:438`) `def clamp_parallel(self, value)` - Clamp a requested fan-out width into [1, parallel_cap].
- `clamp_deadline` (method, `estorides_core/config.py:442`) `def clamp_deadline(self, value)` - Clamp a requested per-target deadline into (0, deadline_cap_seconds].
- `StreamConfig` (class, `estorides_core/config.py:448`) `class StreamConfig` - Server-Sent-Events streaming knobs (buffer size, cadence).
- `ReconFusionConfig` (class, `estorides_core/config.py:460`) `class ReconFusionConfig` - Centralised tunables for the passive recon fusion engine.
- `__post_init__` (method, `estorides_core/config.py:481`) `def __post_init__(self)`
- `SchemaConfig` (class, `estorides_core/config.py:492`) `class SchemaConfig` - Bounds and version for the strict observation/entity data contracts.
- `WebConfig` (class, `estorides_core/config.py:519`) `class WebConfig` - Per-endpoint defaults and render limits for the Flask layer.
- `RetryConfig` (class, `estorides_core/config.py:534`) `class RetryConfig` - Central retry bounds for HTTP fanout.
- `delay` (method, `estorides_core/config.py:542`) `def delay(self, attempt)` - Exponential backoff for 1-indexed attempt, clamped to cap.
- `_pivot_weight_map` (method, `estorides_core/config.py:549`) `def _pivot_weight_map()` - Default per-type lead weights for the pivot scorer.
- `_csv_frozenset` (method, `estorides_core/config.py:566`) `def _csv_frozenset(name, default)` - Read a comma-separated env var into a frozenset, else the default.
- `retry_delay` (method, `estorides_core/config.py:671`) `def retry_delay(attempt)` - Return the backoff sleep for a 1-indexed attempt.
- `jaro` (function, `estorides_core/entity_resolution.py:83`) `def jaro(s1, s2)` - Return the Jaro similarity of two strings in ``[0, 1]``.
- `jaro_winkler` (function, `estorides_core/entity_resolution.py:126`) `def jaro_winkler(s1, s2, prefix_weight)` - Jaro-Winkler similarity: Jaro with a shared-prefix bonus.
- `_soundex` (function, `estorides_core/entity_resolution.py:146`) `def _soundex(token)` - Return a 4-character Soundex code for a Latin token.
- `_normalize_domain` (function, `estorides_core/entity_resolution.py:178`) `def _normalize_domain(value)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 98
- Cross-boundary resolved imports (EXTRACTED): 60

## Connections

- [EXTRACTED] depends_on community 1 <-> 6 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 2 <-> 6 (strength 0.9): Extracted import edge crosses communities: estorides_core/active_recon.py imports estorides_core/tool_runner.py.
- [EXTRACTED] depends_on community 3 <-> 6 (strength 0.9): Extracted import edge crosses communities: estorides_core/async_client.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 6 <-> 4 (strength 0.9): Extracted import edge crosses communities: estorides_core/entity_resolution.py imports estorides_core/ids.py.
- [EXTRACTED] depends_on community 8 <-> 6 (strength 0.9): Extracted import edge crosses communities: estorides_core/tool_install.py imports estorides_core/config.py.
- [INFERRED] shares_context community 0 <-> 6 (strength 0.5): Inferred shared context (language py) with no import path between community 0 (root) and community 6 (estorides_core).

## Risks

- [taint medium] `estorides_core/async_client.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/intel_resolver.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [layer strict] `tests/test_entity_resolution.py` (testing) -> `estorides_core/entity_extraction.py` (presentation)
- [layer strict] `tests/test_socmint.py` (testing) -> `estorides_core/entity_extraction.py` (presentation)

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `estorides_core/tool_runner.py`)? What purpose do they serve?
- What would break if the most connected file in estorides_core changed?
- Should estorides_core be split, given cohesion 0.55?

## Sources

- `estorides_core/config.py`
- `estorides_core/entity_resolution.py`
- `estorides_core/entity_store.py`
- `estorides_core/event_bus.py`
- `estorides_core/mitre_attack.py`
- `estorides_core/observation_models.py`
- `estorides_core/ops_observability.py`
- `estorides_core/orchestrator.py`
- `estorides_core/pagination.py`
- `estorides_core/parsers.py`
- `estorides_core/recon_fusion.py`
- `estorides_core/relationship_inference.py`
- `estorides_core/search_telemetry.py`
- `estorides_core/source_loader.py`
- `estorides_core/system_app_sources.py`
- `estorides_core/tool_runner.py`
- `estorides_core/transliteration.py`
- `estorides_llm/__init__.py`
- `estorides_llm/intelligence_prompts.py`
- `estorides_llm/manager.py`
- *... and 23 more*
