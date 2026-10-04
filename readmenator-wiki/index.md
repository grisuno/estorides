# Second Brain

*Last synthesized: 2026-10-04 | 157 files | 10 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `config.py`, `estorides_web.py`, `orchestrator.py`. Architecturally it is 6 layers, dominant testing (78 files) across 10 import-based communities. Recorded risk surface: 0 security findings and 1 dependency cycles.

Surprising tissue lives between root, tests (community 1), estorides_core (community 2): 9 extracted cross-community imports and 11 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (90% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 157 |
| Symbols | 2745 |
| Resolved imports | 358 |
| Languages | js, py, sh |
| Communities | 10 |
| Doc coverage | 90% (142/157 files) |
| Security findings | 0 |
| Estimated read cost | ~61704 tokens (chars/4, offline so $0) |

## Reading Order

1. Skim Stats and God Nodes below for blast radius.
2. Open the largest community page first, then follow Connections.
3. Use `queries.md` for the next question; log the answer there.

```
grep -rn '<keyword>' index.md community_*.md
readmenator query "<question>" --target estorides
```

## Concept Wiki

- [root (3 files, cohesion 0.67)](./community_0_root.md)
- [tests (community 1) (56 files, cohesion 0.66)](./community_1_tests.md)
- [estorides_core (community 2) (2 files, cohesion 0.33)](./community_2_estorides_core.md)
- [estorides_core (community 3) (8 files, cohesion 0.41)](./community_3_estorides_core.md)
- [estorides_core (community 4) (11 files, cohesion 0.72)](./community_4_estorides_core.md)
- [estorides_core (community 5) (15 files, cohesion 1.00)](./community_5_estorides_core.md)
- [estorides_core (community 6) (43 files, cohesion 0.55)](./community_6_estorides_core.md)
- [tests/properties (3 files, cohesion 1.00)](./community_7_tests_properties.md)
- [tests (community 8) (4 files, cohesion 0.43)](./community_8_tests.md)
- [orphans (12 files, cohesion 0.00)](./community_9_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `estorides_core/config.py` | 84.6 |
| `estorides_web.py` | 75.4 |
| `estorides_core/orchestrator.py` | 55.8 |
| `estorides_cli.py` | 33.1 |
| `estorides_core/entity_extraction.py` | 30.1 |

## Strongest Connections

- 1 -> 6: depends_on (strength 0.9, EXTRACTED)
- 2 -> 6: depends_on (strength 0.9, EXTRACTED)
- 1 -> 3: depends_on (strength 0.9, EXTRACTED)
- 3 -> 6: depends_on (strength 0.9, EXTRACTED)
- 6 -> 4: depends_on (strength 0.9, EXTRACTED)
- 1 -> 4: depends_on (strength 0.9, EXTRACTED)
- 8 -> 6: depends_on (strength 0.9, EXTRACTED)
- 1 -> 8: depends_on (strength 0.9, EXTRACTED)
- 0 -> 1: depends_on (strength 0.9, EXTRACTED)
- 0 -> 2: shares_context (strength 0.5, INFERRED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
