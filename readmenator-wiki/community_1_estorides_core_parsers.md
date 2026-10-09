# estorides_core: parsers

*Community 1 | 23 files | cohesion 0.49*

## Definition

This community groups 23 file(s) rooted at `estorides_core` with dominant language py (cohesion 0.49). Central symbols: `EntityResolver`, `EventBus`, `Fake`, `OntologyEngine`, `Orchestrator`, `PaginationConfig`, `PlatformInfo`, `ProfileMatch`. Core file: `tests/test_socmint.py` (72 symbols). Documented purpose: estorides_core.event_bus.

## Files

### `estorides_core` (12 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/event_bus.py` | py | infrastructure | 9 | yes |
| `estorides_core/intel_resolver.py` | py | utility | 26 | yes |
| `estorides_core/mitre_attack.py` | py | utility | 4 | yes |
| `estorides_core/ontology.py` | py | utility | 25 | yes |
| `estorides_core/orchestrator.py` | py | utility | 18 | yes |
| `estorides_core/pagination.py` | py | utility | 7 | yes |
| `estorides_core/parsers.py` | py | utility | 65 | yes |
| `estorides_core/relationship_inference.py` | py | utility | 16 | yes |
| `estorides_core/socmint.py` | py | utility | 12 | yes |

### `tests` (9 files)

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
| `tests/test_transforms.py` | py | testing | 12 | yes |

### `tests/properties` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/properties/test_parsers_properties.py` | py | testing | 1 | yes |
| `tests/properties/test_system_app_sources_properties.py` | py | testing | 6 | yes |

*... and 3 more files in this community.*


## Key Symbols

- `EventBus` (class, `estorides_core/event_bus.py:24`) `class EventBus` - Synchronous in memory event channel with isolated delivery.
- `__init__` (method, `estorides_core/event_bus.py:27`) `def __init__(self)` - Create an empty bus with no subscribers.
- `subscribe` (method, `estorides_core/event_bus.py:31`) `def subscribe(self, event, handler)` - Register handler for event and return it for unsubscription.
- `unsubscribe` (method, `estorides_core/event_bus.py:41`) `def unsubscribe(self, event, handler)` - Remove handler from event and report whether it was present.
- `publish` (method, `estorides_core/event_bus.py:50`) `def publish(self, event, payload)` - Deliver a copy of payload to each subscriber and count attempts.
- `clear` (method, `estorides_core/event_bus.py:63`) `def clear(self, event)` - Remove subscribers for one event or for the whole bus.
- `subscriber_count` (method, `estorides_core/event_bus.py:71`) `def subscriber_count(self, event)` - Return the number of handlers registered for event.
- `_check_event` (method, `estorides_core/event_bus.py:76`) `def _check_event(self, event)` - Validate that an event name uses the constrained alphabet.
- `get_bus` (method, `estorides_core/event_bus.py:85`) `def get_bus()` - Return the process wide shared bus instance.
- `_run_sparql` (function, `estorides_core/intel_resolver.py:90`) `def _run_sparql(query)` - Execute a SPARQL SELECT against the Wikidata endpoint.
- `_val` (function, `estorides_core/intel_resolver.py:111`) `def _val(row, key)` - Pull a string value out of a SPARQL JSON row.
- `_TTLCache` (class, `estorides_core/intel_resolver.py:120`) `class _TTLCache`
- `__init__` (method, `estorides_core/intel_resolver.py:121`) `def __init__(self)`
- `get` (method, `estorides_core/intel_resolver.py:127`) `def get(self, kind, key)`
- `put` (method, `estorides_core/intel_resolver.py:140`) `def put(self, kind, key, value)`
- `stats` (method, `estorides_core/intel_resolver.py:148`) `def stats(self)`
- `EntityResolver` (class, `estorides_core/intel_resolver.py:156`) `class EntityResolver` - Cross-feed entity resolution.
- `__init__` (method, `estorides_core/intel_resolver.py:165`) `def __init__(self)`
- `resolve` (method, `estorides_core/intel_resolver.py:174`) `def resolve(self, ent_type, ent_id)`
- `_vt_get` (method, `estorides_core/intel_resolver.py:214`) `def _vt_get(self, path, limit)` - GET a VirusTotal v3 path, returning parsed JSON or None.
- `_vt_add_relationship` (method, `estorides_core/intel_resolver.py:245`) `def _vt_add_relationship(self, path)` - Expand one VirusTotal relationship endpoint into nodes/links.
- `_vt_flag_malicious` (method, `estorides_core/intel_resolver.py:290`) `def _vt_flag_malicious(self, path, node, sources)` - Stamp a node with VirusTotal detection stats (counter-intel signal).
- `_resolve_ip` (method, `estorides_core/intel_resolver.py:306`) `def _resolve_ip(self, ip)`
- `_resolve_domain` (method, `estorides_core/intel_resolver.py:412`) `def _resolve_domain(self, domain)`
- `_resolve_file` (method, `estorides_core/intel_resolver.py:473`) `def _resolve_file(self, file_hash)` - Resolve a file hash via VirusTotal relationships.
- `_resolve_company` (method, `estorides_core/intel_resolver.py:510`) `def _resolve_company(self, name)`
- `_resolve_person` (method, `estorides_core/intel_resolver.py:569`) `def _resolve_person(self, name)`
- `_resolve_country` (method, `estorides_core/intel_resolver.py:638`) `def _resolve_country(self, name)`
- `_resolve_cve` (method, `estorides_core/intel_resolver.py:678`) `def _resolve_cve(self, cve_id)`
- `_resolve_btc` (method, `estorides_core/intel_resolver.py:750`) `def _resolve_btc(self, addr)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 57
- Cross-boundary resolved imports (EXTRACTED): 37

## Connections

- [EXTRACTED] depends_on community 5 <-> 1 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/orchestrator.py.
- [EXTRACTED] depends_on community 0 <-> 1 (strength 0.9): Extracted import edge crosses communities: estorides_core/discoverer.py imports estorides_core/orchestrator.py.
- [EXTRACTED] depends_on community 1 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_core/intel_resolver.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 1 <-> 7 (strength 0.9): Extracted import edge crosses communities: estorides_core/orchestrator.py imports estorides_core/entity_extraction.py.
- [EXTRACTED] depends_on community 1 <-> 8 (strength 0.9): Extracted import edge crosses communities: estorides_core/orchestrator.py imports estorides_core/knowledge_graph.py.
- [EXTRACTED] depends_on community 1 <-> 3 (strength 0.9): Extracted import edge crosses communities: estorides_core/orchestrator.py imports estorides_core/recon_fusion.py.
- [EXTRACTED] depends_on community 1 <-> 6 (strength 0.9): Extracted import edge crosses communities: estorides_core/system_app_sources.py imports estorides_core/tool_runner.py.

## Risks

- [taint medium] `estorides_core/intel_resolver.py` -> `estorides_core/intel_resolver.py` via `requests` (0 hops)
- [taint medium] `estorides_core/intel_resolver.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/intel_resolver.py` -> `estorides_core/ontology.py` via `requests` (1 hops)
- [taint medium] `estorides_core/intel_resolver.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)

## Open Questions

- Is the dangerous import `requests` in `estorides_core/intel_resolver.py` still required, or can it be isolated?
- What would break if the most connected file in estorides_core: parsers changed?
- Should estorides_core: parsers be split, given cohesion 0.49?

## Sources

- `estorides_core/event_bus.py`
- `estorides_core/intel_resolver.py`
- `estorides_core/mitre_attack.py`
- `estorides_core/ontology.py`
- `estorides_core/orchestrator.py`
- `estorides_core/pagination.py`
- `estorides_core/parsers.py`
- `estorides_core/relationship_inference.py`
- `estorides_core/socmint.py`
- `estorides_core/source_loader.py`
- `estorides_core/system_app_sources.py`
- `estorides_core/transforms.py`
- `tests/properties/test_parsers_properties.py`
- `tests/properties/test_system_app_sources_properties.py`
- `tests/test_event_bus.py`
- `tests/test_keyless_sources.py`
- `tests/test_opsec_contact.py`
- `tests/test_pagination.py`
- `tests/test_socmint.py`
- `tests/test_source_loader.py`
- *... and 3 more*
