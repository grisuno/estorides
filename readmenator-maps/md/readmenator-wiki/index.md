# Second Brain

*Last synthesized: 2026-10-10 | 178 files | 12 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `config.py`, `estorides_web.py`, `orchestrator.py`. Architecturally it is 6 layers, dominant testing (83 files) across 12 import-based communities. Recorded risk surface: 0 security findings and 3 dependency cycles.

Surprising tissue lives between estorides_core: parsers, estorides_core: estorides_web, estorides_core: config: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (85% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 178 |
| Symbols | 3051 |
| Resolved imports | 394 |
| Languages | js, py, sh |
| Communities | 12 |
| Doc coverage | 85% (152/178 files) |
| Security findings | 0 |
| Estimated read cost | ~65721 tokens (chars/4, offline so $0) |

## Reading Order

1. Skim Stats and God Nodes below for blast radius.
2. Open the largest community page first, then follow Connections.
3. Use `queries.md` for the next question; log the answer there.

```
grep -rn '<keyword>' index.md community_*.md
readmenator query "<question>" --target estorides
```

## Concept Wiki

- [estorides_core: parsers (26 files, cohesion 0.52)](./community_0_estorides_core_parsers.md)
- [estorides_core: estorides_web (24 files, cohesion 0.48)](./community_1_estorides_core_estorides_web.md)
- [estorides_core: config (19 files, cohesion 0.37)](./community_2_estorides_core_config.md)
- [estorides_core: hypothesis_engine (19 files, cohesion 0.66)](./community_3_estorides_core_hypothesis_engine.md)
- [estorides_core: estorides (18 files, cohesion 0.46)](./community_4_estorides_core_estorides.md)
- [estorides_core: people_intel (15 files, cohesion 1.00)](./community_5_estorides_core_people_intel.md)
- [estorides_core: tool_install (10 files, cohesion 0.43)](./community_6_estorides_core_tool_install.md)
- [estorides_export (8 files, cohesion 0.45)](./community_7_estorides_export.md)
- [estorides_core: entity_resolution (7 files, cohesion 0.35)](./community_8_estorides_core_entity_resolution.md)
- [estorides_core: graph_bundle (5 files, cohesion 0.71)](./community_9_estorides_core_graph_bundle.md)
- [estorides_core: source_health_monitoring (3 files, cohesion 1.00)](./community_10_estorides_core_source_health_monitoring.md)
- [orphans (24 files, cohesion 0.00)](./community_11_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `estorides_core/config.py` | 84.6 |
| `estorides_web.py` | 81.5 |
| `estorides_core/orchestrator.py` | 57.8 |
| `estorides_cli.py` | 33.1 |
| `estorides_core/entity_extraction.py` | 30.1 |

## Strongest Connections

- 4 -> 2: depends_on (strength 0.9, EXTRACTED)
- 4 -> 7: depends_on (strength 0.9, EXTRACTED)
- 4 -> 0: depends_on (strength 0.9, EXTRACTED)
- 4 -> 6: depends_on (strength 0.9, EXTRACTED)
- 4 -> 3: depends_on (strength 0.9, EXTRACTED)
- 4 -> 8: depends_on (strength 0.9, EXTRACTED)
- 4 -> 1: depends_on (strength 0.9, EXTRACTED)
- 1 -> 2: depends_on (strength 0.9, EXTRACTED)
- 8 -> 2: depends_on (strength 0.9, EXTRACTED)
- 8 -> 3: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
