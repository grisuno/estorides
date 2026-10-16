# Second Brain

*Last synthesized: 2026-10-16 | 191 files | 11 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `config.py`, `estorides_web.py`, `orchestrator.py`. Architecturally it is 6 layers, dominant testing (90 files) across 11 import-based communities. Recorded risk surface: 0 security findings and 3 dependency cycles.

Surprising tissue lives between estorides_core: estorides_web, estorides_core: parsers, estorides_core: hypothesis_engine: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (86% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 191 |
| Symbols | 3183 |
| Resolved imports | 412 |
| Languages | js, py, sh |
| Communities | 11 |
| Doc coverage | 86% (165/191 files) |
| Security findings | 0 |
| Estimated read cost | ~67865 tokens (chars/4, offline so $0) |

## Reading Order

1. Skim Stats and God Nodes below for blast radius.
2. Open the largest community page first, then follow Connections.
3. Use `queries.md` for the next question; log the answer there.

```
grep -rn '<keyword>' index.md community_*.md
readmenator query "<question>" --target estorides
```

## Concept Wiki

- [estorides_core: estorides_web (27 files, cohesion 0.51)](./community_0_estorides_core_estorides_web.md)
- [estorides_core: parsers (24 files, cohesion 0.47)](./community_1_estorides_core_parsers.md)
- [estorides_core: hypothesis_engine (19 files, cohesion 0.66)](./community_2_estorides_core_hypothesis_engine.md)
- [estorides_core: estorides (17 files, cohesion 0.45)](./community_3_estorides_core_estorides.md)
- [estorides_core: config (17 files, cohesion 0.37)](./community_4_estorides_core_config.md)
- [estorides_core: graph_bundle (15 files, cohesion 0.68)](./community_5_estorides_core_graph_bundle.md)
- [estorides_core: people_intel (15 files, cohesion 1.00)](./community_6_estorides_core_people_intel.md)
- [estorides_export (15 files, cohesion 0.46)](./community_7_estorides_export.md)
- [estorides_core: tool_install (12 files, cohesion 0.46)](./community_8_estorides_core_tool_install.md)
- [estorides_core: source_health_monitoring (3 files, cohesion 1.00)](./community_9_estorides_core_source_health_monitoring.md)
- [orphans (27 files, cohesion 0.00)](./community_10_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `estorides_core/config.py` | 88.9 |
| `estorides_web.py` | 83.7 |
| `estorides_core/orchestrator.py` | 57.8 |
| `estorides_cli.py` | 33.1 |
| `estorides_core/entity_extraction.py` | 30.1 |

## Strongest Connections

- 3 -> 4: depends_on (strength 0.9, EXTRACTED)
- 3 -> 7: depends_on (strength 0.9, EXTRACTED)
- 3 -> 1: depends_on (strength 0.9, EXTRACTED)
- 3 -> 8: depends_on (strength 0.9, EXTRACTED)
- 3 -> 2: depends_on (strength 0.9, EXTRACTED)
- 3 -> 0: depends_on (strength 0.9, EXTRACTED)
- 5 -> 4: depends_on (strength 0.9, EXTRACTED)
- 0 -> 4: depends_on (strength 0.9, EXTRACTED)
- 1 -> 4: depends_on (strength 0.9, EXTRACTED)
- 1 -> 0: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
