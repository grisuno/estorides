# Second Brain

*Last synthesized: 2026-09-29 | 156 files | 5 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `config.py`, `estorides_web.py`, `orchestrator.py`. Architecturally it is 6 layers, dominant testing (77 files) across 5 import-based communities. Recorded risk surface: 0 security findings and 1 dependency cycles.

Surprising tissue lives between estorides_core (community 0), estorides_core (community 1), tests/properties: 1 extracted cross-community imports and 14 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (90% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 156 |
| Symbols | 2718 |
| Resolved imports | 350 |
| Languages | js, py, sh |
| Communities | 5 |
| Doc coverage | 90% (141/156 files) |
| Security findings | 0 |
| Estimated read cost | ~61010 tokens (chars/4, offline so $0) |

## Reading Order

1. Skim Stats and God Nodes below for blast radius.
2. Open the largest community page first, then follow Connections.
3. Use `queries.md` for the next question; log the answer there.

```
grep -rn '<keyword>' index.md community_*.md
readmenator query "<question>" --target estorides
```

## Concept Wiki

- [estorides_core (community 0) (123 files, cohesion 1.00)](./community_0_estorides_core.md)
- [estorides_core (community 1) (15 files, cohesion 1.00)](./community_1_estorides_core.md)
- [tests/properties (3 files, cohesion 1.00)](./community_2_tests_properties.md)
- [estorides_llm (3 files, cohesion 0.67)](./community_3_estorides_llm.md)
- [orphans (12 files, cohesion 0.00)](./community_4_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `estorides_core/config.py` | 84.6 |
| `estorides_web.py` | 75.1 |
| `estorides_core/orchestrator.py` | 55.8 |
| `estorides_cli.py` | 33.1 |
| `estorides_core/entity_extraction.py` | 30.1 |

## Strongest Connections

- 3 -> 0: depends_on (strength 0.9, EXTRACTED)
- 0 -> 1: shares_context (strength 0.5, INFERRED)
- 0 -> 2: shares_context (strength 0.5, INFERRED)
- 0 -> 4: shares_context (strength 0.5, INFERRED)
- 1 -> 2: shares_context (strength 0.5, INFERRED)
- 1 -> 3: shares_context (strength 0.5, INFERRED)
- 1 -> 4: shares_context (strength 0.5, INFERRED)
- 2 -> 3: shares_context (strength 0.5, INFERRED)
- 2 -> 4: shares_context (strength 0.5, INFERRED)
- 3 -> 4: shares_context (strength 0.5, INFERRED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
