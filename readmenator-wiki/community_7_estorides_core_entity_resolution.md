# estorides_core: entity_resolution

*Community 7 | 8 files | cohesion 0.36*

## Definition

This community groups 8 file(s) rooted at `estorides_core` with dominant language py (cohesion 0.36). Central symbols: `CanonicalEntity`, `Entity`, `EntityResolver`, `EntityStore`, `MatchScore`, `ResolutionResult`, `SameAsLink`, `TestCanonicalEntityRoundtrip`. Core file: `tests/test_entity_resolution.py` (68 symbols). Documented purpose: estorides_core.entity_extraction.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/entity_extraction.py` | py | business_logic | 21 | yes |
| `estorides_core/entity_resolution.py` | py | business_logic | 35 | yes |
| `estorides_core/entity_store.py` | py | business_logic | 5 | yes |
| `estorides_core/transliteration.py` | py | utility | 4 | yes |
| `tests/test_entity_extraction.py` | py | testing | 7 | yes |
| `tests/test_entity_resolution.py` | py | testing | 68 | yes |
| `tests/test_query_intent.py` | py | testing | 6 | yes |
| `tests/test_structured_extraction.py` | py | testing | 8 | yes |

## Key Symbols

- `Entity` (class, `estorides_core/entity_extraction.py:22`) `class Entity`
- `to_dict` (method, `estorides_core/entity_extraction.py:34`) `def to_dict(self)`
- `_looks_like_phone` (method, `estorides_core/entity_extraction.py:49`) `def _looks_like_phone(query)` - True for E.164-ish numbers with 7-15 digits (never consumes hashes).
- `normalize_query` (method, `estorides_core/entity_extraction.py:57`) `def normalize_query(query)` - Return the routing form of raw operator input.
- `detect_query_type` (method, `estorides_core/entity_extraction.py:100`) `def detect_query_type(query)` - Return the detected type of a free-form query.
- `_is_valid_domain` (method, `estorides_core/entity_extraction.py:127`) `def _is_valid_domain(candidate)`
- `_context` (method, `estorides_core/entity_extraction.py:140`) `def _context(text, start, end, window)`
- `extract_from_text` (method, `estorides_core/entity_extraction.py:146`) `def extract_from_text(text, source)` - Find every recognised entity in a raw text blob.
- `_ip_in_textual_context` (method, `estorides_core/entity_extraction.py:200`) `def _ip_in_textual_context(text, idx)` - Heuristic: only count a numeric match as an IP if it isn't part of a
- `extract_from_json` (method, `estorides_core/entity_extraction.py:210`) `def extract_from_json(payload, source)` - Pull entities out of a JSON-like structure.
- `_clean_scalar` (method, `estorides_core/entity_extraction.py:278`) `def _clean_scalar(value)` - Return a stripped string for a scalar leaf, or None for non-scalars.
- `_looks_like_person` (method, `estorides_core/entity_extraction.py:288`) `def _looks_like_person(value)` - True when a value reads like a human name (has a space, mostly letters).
- `_looks_like_username` (method, `estorides_core/entity_extraction.py:299`) `def _looks_like_username(value)` - True when a value reads like a handle (no spaces, handle charset).
- `_classify_keyed_value` (method, `estorides_core/entity_extraction.py:306`) `def _classify_keyed_value(key, value)` - Map a (key, scalar value) pair to a human-selector entity type, or None.
- `extract_structured` (method, `estorides_core/entity_extraction.py:330`) `def extract_structured(payload, source)` - Extract human selectors (email, username, person, org, phone) by key.
- `visit` (method, `estorides_core/entity_extraction.py:344`) `def visit(node, key)`
- `merge` (method, `estorides_core/entity_extraction.py:382`) `def merge()` - Deduplicate by (type, value) and merge sources / contexts.
- `_fuzzy_cluster` (method, `estorides_core/entity_extraction.py:476`) `def _fuzzy_cluster(entities)` - Group entities of the same type by string similarity and merge.
- `find` (method, `estorides_core/entity_extraction.py:499`) `def find(x, parent)`
- `union` (method, `estorides_core/entity_extraction.py:505`) `def union(a, b, parent)`
- `norm` (method, `estorides_core/entity_extraction.py:510`) `def norm(v)`
- `jaro` (function, `estorides_core/entity_resolution.py:83`) `def jaro(s1, s2)` - Return the Jaro similarity of two strings in ``[0, 1]``.
- `jaro_winkler` (function, `estorides_core/entity_resolution.py:126`) `def jaro_winkler(s1, s2, prefix_weight)` - Jaro-Winkler similarity: Jaro with a shared-prefix bonus.
- `_soundex` (function, `estorides_core/entity_resolution.py:146`) `def _soundex(token)` - Return a 4-character Soundex code for a Latin token.
- `_normalize_domain` (function, `estorides_core/entity_resolution.py:178`) `def _normalize_domain(value)`
- `_normalize_name` (function, `estorides_core/entity_resolution.py:187`) `def _normalize_name(value)` - Order-independent transliterated key for persons and orgs.
- `normalize_value` (function, `estorides_core/entity_resolution.py:206`) `def normalize_value(etype, value)` - Return the canonical normalised form of an entity value.
- `canonical_id` (function, `estorides_core/entity_resolution.py:246`) `def canonical_id(etype, normalized)` - Stable, content-addressed id for a normalised entity.
- `blocking_keys` (function, `estorides_core/entity_resolution.py:257`) `def blocking_keys(etype, normalized, value)` - Return the blocking keys that bucket an entity for comparison.
- `MatchScore` (class, `estorides_core/entity_resolution.py:295`) `class MatchScore` - The result of comparing two entity values of the same type.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 10
- Cross-boundary resolved imports (EXTRACTED): 20

## Connections

- [EXTRACTED] depends_on community 5 <-> 7 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/entity_extraction.py.
- [EXTRACTED] depends_on community 7 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_core/entity_extraction.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 7 <-> 3 (strength 0.9): Extracted import edge crosses communities: estorides_core/entity_resolution.py imports estorides_core/ids.py.
- [EXTRACTED] depends_on community 8 <-> 7 (strength 0.9): Extracted import edge crosses communities: estorides_core/knowledge_graph.py imports estorides_core/entity_extraction.py.
- [EXTRACTED] depends_on community 1 <-> 7 (strength 0.9): Extracted import edge crosses communities: estorides_core/orchestrator.py imports estorides_core/entity_extraction.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in estorides_core: entity_resolution changed?
- Should estorides_core: entity_resolution be split, given cohesion 0.36?

## Sources

- `estorides_core/entity_extraction.py`
- `estorides_core/entity_resolution.py`
- `estorides_core/entity_store.py`
- `estorides_core/transliteration.py`
- `tests/test_entity_extraction.py`
- `tests/test_entity_resolution.py`
- `tests/test_query_intent.py`
- `tests/test_structured_extraction.py`
