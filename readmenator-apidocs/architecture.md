# estorides Architecture and Execution Flows

[Back to index](index.md)

## Architecture Overview

15 components stacked in 6 dependency tiers (weighted Eades-Lin-Smyth ordering: arrows point from dependent to dependency, top to bottom). Labels are import counts, thick arrows the top quartile; 13 transitively implied edges are omitted. Dashed red arrows are upward dependencies: the smallest set of imports that closes every cycle and breaks the layering. Cyan components hold entry points. Interactive version: `readmenator-apidocs/index.html#/flows`.

Upward dependencies to fix first: `estorides_core: estorides` -> `estorides_core: parsers` (3 imports); `estorides_export` -> `estorides_core: estorides` (2 imports); `estorides_core: parsers` -> `estorides_core: estorides_web` (1 imports); `estorides_core: hypothesis_engine` -> `estorides_core: estorides` (1 imports); `estorides_core: estorides` -> `estorides_core: estorides_web` (1 imports); `estorides_export` -> `estorides_core: hypothesis_engine` (1 imports)

```mermaid
flowchart TB
    classDef cycle fill:#1f1530,stroke:#f472b6,color:#fce7f3,stroke-width:2px;
    classDef default fill:#111827,stroke:#38bdf8,color:#e5e7eb;
    classDef entry fill:#0e7490,stroke:#22d3ee,color:#ecfeff,stroke-width:2px;
    subgraph lane_0["Tier 1 - entry / orchestration"]
        direction LR
        n_c0["estorides_core: estorides_web<br/>14 files, 230 symbols<br/>Core / utility"]:::entry
        n_d_tools["tools<br/>1 files, 1 symbols<br/>Core / utility"]:::default
        n_d_static["static<br/>3 files, 200 symbols<br/>Core / utility"]:::default
        n_d_estorides_core["estorides_core<br/>2 files, 14 symbols<br/>Business logic"]:::default
        n_d__scratchpad[".scratchpad<br/>11 files, 0 symbols<br/>Core / utility"]:::default
        n_d__root_["(root)<br/>1 files, 2 symbols<br/>Core / utility"]:::default
        n_c9["estorides_core: source_health_monitoring<br/>1 files, 14 symbols<br/>Core / utility"]:::default
        n_c6["estorides_core: people_intel<br/>8 files, 72 symbols<br/>Core / utility"]:::default
    end
    subgraph lane_1["Tier 2"]
        direction LR
        n_c1["estorides_core: parsers<br/>14 files, 238 symbols<br/>Core / utility"]:::cycle
        n_c5["estorides_core: graph_bundle<br/>4 files, 42 symbols<br/>Core / utility"]:::default
    end
    subgraph lane_2["Tier 3"]
        direction LR
        n_c3["estorides_core: estorides<br/>9 files, 332 symbols<br/>Core / utility"]:::cycle
    end
    subgraph lane_3["Tier 4"]
        direction LR
        n_c8["estorides_core: tool_install<br/>5 files, 81 symbols<br/>Core / utility"]:::cycle
        n_c2["estorides_core: hypothesis_engine<br/>7 files, 111 symbols<br/>Core / utility"]:::cycle
    end
    subgraph lane_4["Tier 5"]
        direction LR
        n_c7["estorides_export<br/>10 files, 105 symbols<br/>Core / utility"]:::cycle
    end
    subgraph lane_5["Tier 6 - foundation"]
        direction LR
        n_c4["estorides_core: config<br/>11 files, 208 symbols<br/>Core / utility"]:::default
    end
    n_c0 ==>|"7"| n_c1
    n_c0 ==>|"5"| n_c5
    n_c1 -->|"2"| n_c3
    n_c2 -->|"1"| n_c7
    n_c3 -->|"1"| n_c2
    n_c3 -->|"1"| n_c8
    n_c5 -->|"1"| n_c4
    n_c7 ==>|"6"| n_c4
    n_c8 -->|"2"| n_c7
    n_c0 <-.-|"1 upward"| n_c1
    n_c3 <-.-|"1 upward"| n_c2
    n_c0 <-.-|"1 upward"| n_c3
    n_c1 <-.-|"3 upward"| n_c3
    n_c2 <-.-|"1 upward"| n_c7
    n_c3 <-.-|"2 upward"| n_c7
    linkStyle 9,10,11,12,13,14 stroke:#f87171,stroke-width:2px;
    n_c0 ~~~ n_c1
    n_c1 ~~~ n_c3
    n_c3 ~~~ n_c8
    n_c8 ~~~ n_c7
    n_c7 ~~~ n_c4
```

---

## Execution Flows

Entry points are scored from `__main__` guards, `main` functions, entry-style names and files, and call-graph sources. Each flow walks resolved calls in call-site order (depth <= 4, <= 40 steps); numbers give the call order, dashed arrows revisit an already expanded callee, red arrows are recursion. Interactive version with zoom and per-node docs: `readmenator-apidocs/index.html#/flows`.

### `transforms.run`

`estorides_core/transforms.py:124`, score 9: entry-style name `run`.

Call tree:

```mermaid
flowchart LR
    classDef default fill:#111827,stroke:#38bdf8,color:#e5e7eb;
    classDef entry fill:#0e7490,stroke:#22d3ee,color:#ecfeff,stroke-width:2px;
    n_estorides_core_transforms_py__run["transforms.run<br/>transforms.py:124"]:::entry
    n_estorides_core_transforms_py___resolver_filtered["transforms._resolver_filtered<br/>Resolve #96;(ent_type, value)#96; and keep only lin...<br/>transforms.py:102"]:::default
    n_estorides_core_transforms_py__run -->|"1"| n_estorides_core_transforms_py___resolver_filtered
```

### `estorides_cli (__main__)`

`estorides_cli.py:870`, score 8: `if __name__ == "__main__"` guard.

Call tree:

```mermaid
flowchart LR
    classDef default fill:#111827,stroke:#38bdf8,color:#e5e7eb;
    classDef entry fill:#0e7490,stroke:#22d3ee,color:#ecfeff,stroke-width:2px;
    classDef external fill:#1a1530,stroke:#a78bfa,color:#ede9fe;
    n_estorides_cli_py___main_["estorides_cli (__main__)<br/>estorides_cli.py"]:::entry
    n_estorides_cli_py__main["estorides_cli.main<br/>estorides_cli.py:863"]:::default
    n_estorides_cli_py__build_parser["estorides_cli.build_parser<br/>estorides_cli.py:707"]:::default
    n_estorides_cli_py___add_opsec_flags["estorides_cli._add_opsec_flags<br/>Attach the shared operator-OPSEC flags to a s...<br/>estorides_cli.py:75"]:::default
    n_estorides_cli_py__cmd_run["estorides_cli.cmd_run<br/>estorides_cli.py:205"]:::default
    n_estorides_core_validation_py__validate_query["validation.validate_query<br/>Validate and normalise a user query string.<br/>validation.py:85"]:::external
    n_estorides_core_orchestrator_py__Orchestrator["orchestrator.Orchestrator<br/>orchestrator.py:168"]:::external
    n_estorides_cli_py___resolve_proxy["estorides_cli._resolve_proxy<br/>Resolve the egress proxy from the OPSEC flags.<br/>estorides_cli.py:62"]:::default
    n_estorides_core_orchestrator_py__run["orchestrator.Orchestrator.run<br/>Run a full intelligence cycle.<br/>orchestrator.py:190"]:::external
    n_estorides_cli_py__cmd_discover["estorides_cli.cmd_discover<br/>v1.2 — fanout the surface from a seed.<br/>estorides_cli.py:93"]:::default
    n_estorides_core_entity_extraction_py__detect_query_type["entity_extraction.detect_query_type<br/>Return the detected type of a free-form query.<br/>entity_extraction.py:100"]:::external
    n_estorides_core_discoverer_py__start_discover["discoverer.start_discover<br/>Create a discovery job and schedule its worke...<br/>discoverer.py:252"]:::external
    n_estorides_cli_py___collect_selectors["estorides_cli._collect_selectors<br/>Group discovered entity values by type for th...<br/>estorides_cli.py:46"]:::default
    n_estorides_cli_py___setup_logging["estorides_cli._setup_logging<br/>estorides_cli.py:39"]:::default
    n_estorides_cli_py___main_ -->|"1"| n_estorides_cli_py__main
    n_estorides_cli_py__main -->|"1"| n_estorides_cli_py__build_parser
    n_estorides_cli_py__build_parser -->|"1"| n_estorides_cli_py___add_opsec_flags
    n_estorides_cli_py__build_parser -->|"2"| n_estorides_cli_py__cmd_run
    n_estorides_cli_py__cmd_run -->|"1"| n_estorides_core_validation_py__validate_query
    n_estorides_cli_py__cmd_run -->|"2"| n_estorides_core_orchestrator_py__Orchestrator
    n_estorides_cli_py__cmd_run -->|"3"| n_estorides_cli_py___resolve_proxy
    n_estorides_cli_py__cmd_run -->|"4"| n_estorides_core_orchestrator_py__run
    n_estorides_cli_py__build_parser -->|"3"| n_estorides_cli_py__cmd_discover
    n_estorides_cli_py__cmd_discover -->|"1"| n_estorides_core_entity_extraction_py__detect_query_type
    n_estorides_cli_py__cmd_discover -->|"2"| n_estorides_cli_py___resolve_proxy
    n_estorides_cli_py__cmd_discover -->|"3"| n_estorides_core_discoverer_py__start_discover
    n_estorides_cli_py__cmd_discover -->|"4"| n_estorides_cli_py___collect_selectors
    n_estorides_cli_py__main -->|"2"| n_estorides_cli_py___setup_logging
```

Cross-file sequence:

```mermaid
sequenceDiagram
    autonumber
    participant p_estorides_cli_py as estorides_cli.py
    participant p_estorides_core_validation_py as validation.py
    participant p_estorides_core_orchestrator_py as orchestrator.py
    participant p_estorides_core_entity_extraction_py as entity_extraction.py
    participant p_estorides_core_discoverer_py as discoverer.py
    p_estorides_cli_py->>p_estorides_core_validation_py: validate_query()
    p_estorides_cli_py->>p_estorides_core_orchestrator_py: Orchestrator()
    p_estorides_cli_py->>p_estorides_core_orchestrator_py: Orchestrator.run()
    p_estorides_cli_py->>p_estorides_core_entity_extraction_py: detect_query_type()
    p_estorides_cli_py->>p_estorides_core_discoverer_py: start_discover()
```

### `tool_install (__main__)`

`estorides_core/tool_install.py:541`, score 8: `if __name__ == "__main__"` guard.

Call tree:

```mermaid
flowchart LR
    classDef default fill:#111827,stroke:#38bdf8,color:#e5e7eb;
    classDef entry fill:#0e7490,stroke:#22d3ee,color:#ecfeff,stroke-width:2px;
    classDef external fill:#1a1530,stroke:#a78bfa,color:#ede9fe;
    n_estorides_core_tool_install_py___main_["tool_install (__main__)<br/>tool_install.py"]:::entry
    n_estorides_core_tool_install_py__main["tool_install.main<br/>Minimal CLI: #96;#96;python -m estorides_core.tool_...<br/>tool_install.py:516"]:::default
    n_estorides_core_tool_install_py__list_recipes["tool_install.list_recipes<br/>Names of all tool recipe files in #96;#96;tool_reci...<br/>tool_install.py:270"]:::default
    n_estorides_core_tool_install_py__install_tool["tool_install.install_tool<br/>Install a missing tool from its recipe (if any).<br/>tool_install.py:414"]:::default
    n_estorides_core_tool_install_py__is_valid_binary["tool_install.is_valid_binary<br/>True when #96;#96;name#96;#96; is a plausible bare binary...<br/>tool_install.py:174"]:::default
    n_estorides_core_tool_install_py__InstallResult["tool_install.InstallResult<br/>Outcome of one #96;#96;install_tool#96;#96; invocation.<br/>tool_install.py:103"]:::default
    n_estorides_core_tool_runner_py___resolve_binary["tool_runner._resolve_binary<br/>tool_runner.py:107"]:::external
    n_estorides_core_tool_runner_py__ToolNotFoundError["tool_runner.ToolNotFoundError<br/>tool_runner.py:29"]:::external
    n_estorides_core_tool_install_py__is_valid_recipe_name["tool_install.is_valid_recipe_name<br/>True when #96;#96;name#96;#96; is a safe recipe/tool iden...<br/>tool_install.py:169"]:::default
    n_estorides_core_tool_install_py__load_recipe["tool_install.load_recipe<br/>Load a tool recipe from #96;#96;tool_recipes/#lt;name#gt;...<br/>tool_install.py:210"]:::default
    n_estorides_core_tool_install_py___recipe_path["tool_install._recipe_path<br/>tool_install.py:193"]:::default
    n_estorides_core_tool_install_py__InstallRecipe["tool_install.InstallRecipe<br/>One tool's install recipe, loaded from #96;#96;tool...<br/>tool_install.py:81"]:::default
    n_estorides_core_tool_install_py__has_apt["tool_install.InstallRecipe.has_apt<br/>tool_install.py:95"]:::default
    n_estorides_core_tool_install_py__has_git["tool_install.InstallRecipe.has_git<br/>tool_install.py:98"]:::default
    n_estorides_core_tool_install_py___verify["tool_install._verify<br/>Post-install check: can the binary now be res...<br/>tool_install.py:506"]:::default
    n_static_js_graph_force_js__fn["graph_force.fn<br/>graph_force.js:1267"]:::external
    n_static_js_graph_force_js__hud["graph_force.hud<br/>graph_force.js:1156"]:::external
    n_estorides_core_tool_install_py___main_ -->|"1"| n_estorides_core_tool_install_py__main
    n_estorides_core_tool_install_py__main -->|"1"| n_estorides_core_tool_install_py__list_recipes
    n_estorides_core_tool_install_py__main -->|"2"| n_estorides_core_tool_install_py__install_tool
    n_estorides_core_tool_install_py__install_tool -->|"1"| n_estorides_core_tool_install_py__is_valid_binary
    n_estorides_core_tool_install_py__install_tool -->|"2"| n_estorides_core_tool_install_py__InstallResult
    n_estorides_core_tool_install_py__install_tool -->|"3"| n_estorides_core_tool_runner_py___resolve_binary
    n_estorides_core_tool_runner_py___resolve_binary -->|"1"| n_estorides_core_tool_runner_py__ToolNotFoundError
    n_estorides_core_tool_install_py__install_tool -->|"4"| n_estorides_core_tool_install_py__is_valid_recipe_name
    n_estorides_core_tool_install_py__install_tool -.-> n_estorides_core_tool_install_py__list_recipes
    n_estorides_core_tool_install_py__install_tool -->|"5"| n_estorides_core_tool_install_py__load_recipe
    n_estorides_core_tool_install_py__load_recipe -.-> n_estorides_core_tool_install_py__list_recipes
    n_estorides_core_tool_install_py__load_recipe -->|"1"| n_estorides_core_tool_install_py___recipe_path
    n_estorides_core_tool_install_py__load_recipe -->|"2"| n_estorides_core_tool_install_py__InstallRecipe
    n_estorides_core_tool_install_py__load_recipe -->|"3"| n_estorides_core_tool_install_py__has_apt
    n_estorides_core_tool_install_py__load_recipe -->|"4"| n_estorides_core_tool_install_py__has_git
    n_estorides_core_tool_install_py__install_tool -->|"6"| n_estorides_core_tool_install_py___verify
    n_estorides_core_tool_install_py___verify -.-> n_estorides_core_tool_runner_py___resolve_binary
    n_estorides_core_tool_install_py__install_tool -->|"7"| n_static_js_graph_force_js__fn
    n_static_js_graph_force_js__fn -.->|"recursion"| n_static_js_graph_force_js__fn
    n_static_js_graph_force_js__fn -->|"1"| n_static_js_graph_force_js__hud
    linkStyle 18 stroke:#f87171,stroke-width:2px;
```

Cross-file sequence:

```mermaid
sequenceDiagram
    autonumber
    participant p_estorides_core_tool_install_py as tool_install.py
    participant p_estorides_core_tool_runner_py as tool_runner.py
    participant p_static_js_graph_force_js as graph_force.js
    p_estorides_core_tool_install_py->>p_estorides_core_tool_runner_py: _resolve_binary()
    p_estorides_core_tool_install_py->>p_static_js_graph_force_js: fn()
```

---
