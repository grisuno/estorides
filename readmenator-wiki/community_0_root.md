# root

*Community 0 | 3 files | cohesion 0.67*

## Definition

This community groups 3 file(s) rooted at `root` with dominant language py (cohesion 0.67). Central symbols: no extracted symbols. Documented purpose: Deprecated entry point. Use:  - the `estorides` console script (installed by `pip install -e .`), or - `python3 estorides_cli.py serve` for the dev server, or -.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `app.py` | py | utility | 0 | yes |
| `web.py` | py | utility | 0 | yes |
| `wsgi.py` | py | utility | 0 | yes |

## Key Symbols

- No symbols extracted in this community.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 2
- Cross-boundary resolved imports (EXTRACTED): 1

## Connections

- [EXTRACTED] depends_on community 0 <-> 1 (strength 0.9): Extracted import edge crosses communities: wsgi.py imports estorides_web.py.
- [INFERRED] shares_context community 0 <-> 2 (strength 0.5): Inferred shared context (language py) with no import path between community 0 (root) and community 2 (estorides_core).
- [INFERRED] shares_context community 0 <-> 3 (strength 0.5): Inferred shared context (language py and layer utility) with no import path between community 0 (root) and community 3 (estorides_core).
- [INFERRED] shares_context community 0 <-> 5 (strength 0.5): Inferred shared context (language py and layer utility) with no import path between community 0 (root) and community 5 (estorides_core).
- [INFERRED] shares_context community 0 <-> 6 (strength 0.5): Inferred shared context (language py) with no import path between community 0 (root) and community 6 (estorides_core).
- [INFERRED] shares_context community 0 <-> 7 (strength 0.5): Inferred shared context (language py) with no import path between community 0 (root) and community 7 (tests/properties).
- [INFERRED] shares_context community 0 <-> 8 (strength 0.5): Inferred shared context (language py) with no import path between community 0 (root) and community 8 (tests).
- [INFERRED] shares_context community 0 <-> 9 (strength 0.5): Inferred shared context (language py) with no import path between community 0 (root) and community 9 (orphans).

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in root changed?
- Should root be split, given cohesion 0.67?

## Sources

- `app.py`
- `web.py`
- `wsgi.py`
