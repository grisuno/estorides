# Second Brain

*Last synthesized: 2026-10-07 | 157 files | 11 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `config.py`, `estorides_web.py`, `orchestrator.py`. Architecturally it is 6 layers, dominant testing (78 files) across 11 import-based communities. Recorded risk surface: 0 security findings and 3 dependency cycles.

Surprising tissue lives between estorides_core: estorides_web, estorides_core: parsers, estorides_core: config: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (90% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 157 |
| Symbols | 2745 |
| Resolved imports | 370 |
| Languages | js, py, sh |
| Communities | 11 |
| Doc coverage | 90% (142/157 files) |
| Security findings | 0 |
| Estimated read cost | ~61704 tokens (chars/4, offline so $0) |

## Reading Order

1. Skim Stats and God Nodes below for blast radius.
2. Open the largest community page first, then follow Connections.
3. Use `queries.md` for the next question; log the answer there.

```
grep -rn '<keyword>' index.md community_*.md
readmenator query "<question>" --target readmenator_estorides_fo1wx2yt
```

## Concept Wiki

- [estorides_core: estorides_web (25 files, cohesion 0.48)](./community_0_estorides_core_estorides_web.md)
- [estorides_core: parsers (23 files, cohesion 0.49)](./community_1_estorides_core_parsers.md)
- [estorides_core: config (22 files, cohesion 0.39)](./community_2_estorides_core_config.md)
- [estorides_core: hypothesis_engine (19 files, cohesion 0.66)](./community_3_estorides_core_hypothesis_engine.md)
- [estorides_core: people_intel (15 files, cohesion 1.00)](./community_4_estorides_core_people_intel.md)
- [estorides_core: estorides (14 files, cohesion 0.44)](./community_5_estorides_core_estorides.md)
- [estorides_core: tool_install (10 files, cohesion 0.43)](./community_6_estorides_core_tool_install.md)
- [estorides_core: entity_resolution (8 files, cohesion 0.36)](./community_7_estorides_core_entity_resolution.md)
- [estorides_export (8 files, cohesion 0.45)](./community_8_estorides_export.md)
- [estorides_core: source_health_monitoring (3 files, cohesion 1.00)](./community_9_estorides_core_source_health_monitoring.md)
- [orphans (10 files, cohesion 0.00)](./community_10_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `estorides_core/config.py` | 84.6 |
| `estorides_web.py` | 75.4 |
| `estorides_core/orchestrator.py` | 57.8 |
| `estorides_cli.py` | 33.1 |
| `estorides_core/entity_extraction.py` | 30.1 |

## Strongest Connections

- 5 -> 2: depends_on (strength 0.9, EXTRACTED)
- 5 -> 8: depends_on (strength 0.9, EXTRACTED)
- 5 -> 1: depends_on (strength 0.9, EXTRACTED)
- 5 -> 6: depends_on (strength 0.9, EXTRACTED)
- 5 -> 0: depends_on (strength 0.9, EXTRACTED)
- 5 -> 3: depends_on (strength 0.9, EXTRACTED)
- 5 -> 7: depends_on (strength 0.9, EXTRACTED)
- 0 -> 2: depends_on (strength 0.9, EXTRACTED)
- 0 -> 1: depends_on (strength 0.9, EXTRACTED)
- 7 -> 2: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
