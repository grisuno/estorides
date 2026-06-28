# Issue #46: Latent Cypher injection in KuzuGraphBackend.neighbors() via unsanitised relation parameter

- **State:** open
- **Created:** 2026-06-08T11:43:30Z
- **Updated:** 2026-06-08T11:43:30Z
- **Labels:** None

---

## Summary
The `neighbors()` method in `estorides_core/graph_kuzu.py` constructs a Cypher query string using an f-string that embeds the caller-controlled `relation` parameter without sanitisation. Although the current call site in `estorides_web.py` passes a hardcoded `relation=None` (line 504), the function signature accepts arbitrary strings and will interpolate them directly into the Cypher query. Any future caller that passes a user-controlled `relation` parameter would create a Cypher injection vulnerability.

## Evidence
`estorides_core/graph_kuzu.py` lines 356–363:
```python
def neighbors(
    self,
    node_id: str,
    hops: int = 1,
    relation: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    rel_filter = f":{relation}" if relation else ""   # UNSANITISED
    q = (
        f"MATCH (n:Ent {{id: $id}})-[{rel_filter}*1..{int(hops)}]"  # INJECTED
        f"-(m:Ent) "
        f"RETURN DISTINCT m.id, m.type, m.value, m.kind "
        f"LIMIT {int(limit)}"
    )
    return self.cypher(q, {"id": node_id})
```

If `relation` were ever passed as `"OBSERVED_BY|CO_OCCURS {p: $inject}`, the injected Cypher would execute. The current web route does not expose `relation` as a URL parameter, but the public method signature has no guard.

Additionally, `stats()` method at lines 401–414 uses f-string interpolation of `label` and `rel` from internal dictionaries (not user-controlled), but the pattern shows inconsistency: some queries use parameters (`$id`, `$src`, `$dst`) while structural elements (labels, relationship types) are always interpolated.

## Why this matters
Kuzu does not support parameterised label or relationship-type substitution (this is a common limitation in graph databases). This forces structural elements into f-strings. The danger is that the public API of `neighbors()` accepts a `relation` string that, if exposed to user input in a future route, would enable Cypher injection — data exfiltration, schema manipulation.

## Attack or failure scenario
(Hypothetical future exposure): A developer adds `relation = request.args.get("relation")` and calls `kuzu_backend.neighbors(nid, relation=relation)`. An attacker sends `?relation=]-(x:Source)-[:OBSERVED_BY*0..]->(y:Ent) WHERE y.value =~ ".*" RETURN y.value //`. The injected query returns all entity values in the graph, bypassing the intended neighbor query.

## Root cause
Cypher does not support parameterised relationship type labels, so structural interpolation is unavoidable. The function was written without a validate-against-allowlist step for the `relation` parameter, creating a latent injection vector in the public API.

## Recommended fix
1. Add an allowlist validation for `relation` at the entry to `neighbors()`:
```python
_VALID_RELATIONS = frozenset(_RELATION_TO_EDGE.values())  # OBSERVED_BY, CO_OCCURS, etc.

def neighbors(self, node_id, hops=1, relation=None, limit=100):
    if relation is not None and relation not in _VALID_RELATIONS:
        raise ValueError(f"invalid relation {relation!r}; must be one of {_VALID_RELATIONS}")
    rel_filter = f":{relation}" if relation else ""
    ...
```
2. Mark the parameter in the docstring as "must be a value from `_RELATION_TO_EDGE`."
3. Add a test that verifies `neighbors()` raises `ValueError` for an arbitrary string in `relation`.

## Acceptance criteria
- `neighbors()` raises `ValueError` for any `relation` value not in the `_RELATION_TO_EDGE` allowlist.
- The `_VALID_RELATIONS` frozenset is derived from `_RELATION_TO_EDGE` so it stays in sync.
- A unit test covers the invalid-relation path.

## Suggested labels
security, bug

## Priority
P2

## Severity
High — Latent Cypher injection in a public API method. Not currently exploitable via any web route, but requires only one future `request.args.get("relation")` call to become a confirmed Critical.

## Confidence
Confirmed — the unvalidated f-string interpolation of `relation` is present in the code; the current non-exposure is verified by inspection of call sites.
