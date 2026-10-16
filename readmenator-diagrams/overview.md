```mermaid
graph LR
    estorides_core_estorides_web["estorides_core: estorides_web"]
    estorides_core_parsers["estorides_core: parsers"]
    estorides_core_config["estorides_core: config"]
    estorides_core_hypothesis_engine["estorides_core: hypothesis_engine"]
    estorides_core_estorides["estorides_core: estorides"]
    estorides_core_graph_bundle["estorides_core: graph_bundle"]
    estorides_core_people_intel["estorides_core: people_intel"]
    estorides_export["estorides_export"]
    estorides_core_tool_install["estorides_core: tool_install"]
    estorides_core_source_health_monitoring["estorides_core: source_health_monitoring"]
    estorides_core_estorides_web -- "calls into" --> estorides_core_parsers
    estorides_core_estorides_web -- "calls into" --> estorides_core_config
    estorides_core_estorides_web -- "calls into" --> estorides_core_hypothesis_engine
    estorides_core_estorides_web -- "calls into" --> estorides_core_estorides
    estorides_core_estorides_web -- "depends on" --> estorides_core_graph_bundle
    estorides_core_estorides_web -- "calls into" --> estorides_export
    estorides_core_estorides_web -- "calls into" --> estorides_core_tool_install
    estorides_core_source_health_monitoring -- "calls into" --> estorides_core_estorides
    estorides_core_parsers -- "calls into" --> estorides_core_estorides_web
    estorides_core_parsers -- "calls into" --> estorides_core_config
    estorides_core_parsers -- "calls into" --> estorides_core_hypothesis_engine
    estorides_core_parsers -- "calls into" --> estorides_core_estorides
    estorides_core_parsers -- "calls into" --> estorides_export
    estorides_core_parsers -- "depends on" --> estorides_core_tool_install
    estorides_core_config -- "calls into" --> estorides_core_estorides_web
    estorides_core_config -- "calls into" --> estorides_core_parsers
    estorides_core_config -- "calls into" --> estorides_core_estorides
    estorides_core_config -- "calls into" --> estorides_export
    estorides_core_hypothesis_engine -- "calls into" --> estorides_core_estorides_web
    estorides_core_hypothesis_engine -- "calls into" --> estorides_core_parsers
    estorides_core_hypothesis_engine -- "depends on" --> estorides_core_config
    estorides_core_hypothesis_engine -- "calls into" --> estorides_core_estorides
    estorides_core_hypothesis_engine -- "depends on" --> estorides_export
    estorides_core_estorides -- "calls into" --> estorides_core_estorides_web
    estorides_core_estorides -- "calls into" --> estorides_core_parsers
    estorides_core_estorides -- "depends on" --> estorides_core_config
    estorides_core_estorides -- "calls into" --> estorides_core_hypothesis_engine
    estorides_core_estorides -- "depends on" --> estorides_core_graph_bundle
    estorides_core_estorides -- "calls into" --> estorides_export
    estorides_core_estorides -- "calls into" --> estorides_core_tool_install
    estorides_core_graph_bundle -- "calls into" --> estorides_core_estorides_web
    estorides_core_graph_bundle -- "calls into" --> estorides_core_parsers
    estorides_core_graph_bundle -- "calls into" --> estorides_core_config
    estorides_core_graph_bundle -- "calls into" --> estorides_core_estorides
    estorides_core_people_intel -- "calls into" --> estorides_core_estorides_web
    estorides_export -- "calls into" --> estorides_core_estorides_web
    estorides_export -- "calls into" --> estorides_core_parsers
    estorides_export -- "calls into" --> estorides_core_config
    estorides_export -- "calls into" --> estorides_core_hypothesis_engine
    estorides_export -- "calls into" --> estorides_core_estorides
    estorides_core_tool_install -- "depends on" --> estorides_core_parsers
    estorides_core_tool_install -- "depends on" --> estorides_core_config
    estorides_core_tool_install -- "calls into" --> estorides_core_estorides
    estorides_core_tool_install -- "calls into" --> estorides_core_graph_bundle
    estorides_core_tool_install -- "calls into" --> estorides_export
    click estorides_core_estorides_web href "./estorides_core_estorides_web.md" "Details"
    click estorides_core_parsers href "./estorides_core_parsers.md" "Details"
    click estorides_core_config href "./estorides_core_config.md" "Details"
    click estorides_core_hypothesis_engine href "./estorides_core_hypothesis_engine.md" "Details"
    click estorides_core_estorides href "./estorides_core_estorides.md" "Details"
    click estorides_core_graph_bundle href "./estorides_core_graph_bundle.md" "Details"
    click estorides_core_people_intel href "./estorides_core_people_intel.md" "Details"
    click estorides_export href "./estorides_export.md" "Details"
    click estorides_core_tool_install href "./estorides_core_tool_install.md" "Details"
```

## Details

Static architecture map of 191 files (js, py, sh) in 10 components: estorides_core: estorides_web, estorides_core: parsers, estorides_core: config, estorides_core: hypothesis_engine, estorides_core: estorides, estorides_core: graph_bundle, estorides_core: people_intel, estorides_export. Structure is extracted statically without LLM calls; component prose may be enriched locally.

### estorides_core: estorides_web (1)

estorides_core: estorides_web groups 27 files (py) around _sse_response, _provides, deco, wrapper, _client_ip. Deprecated entry point.

**Related Classes/Methods**:

- <a href="../estorides_web.py#L78-L82">estorides_web.py::_sse_response</a>
- <a href="../estorides_web.py#L83-L89">estorides_web.py::_provides</a>
- <a href="../estorides_web.py#L90-L91">estorides_web.py::deco</a>
- <a href="../estorides_web.py#L92-L101">estorides_web.py::wrapper</a>
- <a href="../estorides_web.py#L102-L118">estorides_web.py::_client_ip</a>
- <a href="../estorides_web.py#L119-L134">estorides_web.py::_arg_int</a>
- <a href="../estorides_web.py#L135-L148">estorides_web.py::_send_and_cleanup</a>
- <a href="../estorides_web.py#L149-L156">estorides_web.py::_RunStreamJob</a>

### estorides_core: parsers (2)

estorides_core: parsers groups 21 files (py) around _d, _first_dict, _list, _text, parse_dns_json. Background subdomain/domain discoverer.

**Related Classes/Methods**:

- <a href="../estorides_core/parsers.py#L31-L39">estorides_core/parsers.py::_d</a>
- <a href="../estorides_core/parsers.py#L40-L46">estorides_core/parsers.py::_first_dict</a>
- <a href="../estorides_core/parsers.py#L47-L55">estorides_core/parsers.py::_list</a>
- <a href="../estorides_core/parsers.py#L56-L61">estorides_core/parsers.py::_text</a>
- <a href="../estorides_core/parsers.py#L62-L77">estorides_core/parsers.py::parse_dns_json</a>
- <a href="../estorides_core/parsers.py#L78-L95">estorides_core/parsers.py::parse_crtsh_json</a>
- <a href="../estorides_core/parsers.py#L96-L175">estorides_core/parsers.py::parse_rdap</a>
- <a href="../estorides_core/parsers.py#L176-L201">estorides_core/parsers.py::parse_ipapi</a>

### estorides_core: config (3)

estorides_core: config groups 19 files (py) around ensure_data_dirs, ensure_reports_dir, _env_tool_allowlist, contact_level, effective_proxies. estorides_core.async_client

**Related Classes/Methods**:

- <a href="../estorides_core/config.py#L58-L68">estorides_core/config.py::ensure_data_dirs</a>
- <a href="../estorides_core/config.py#L69-L125">estorides_core/config.py::ensure_reports_dir</a>
- <a href="../estorides_core/config.py#L126-L205">estorides_core/config.py::_env_tool_allowlist</a>
- <a href="../estorides_core/config.py#L206-L231">estorides_core/config.py::contact_level</a>
- <a href="../estorides_core/config.py#L232-L365">estorides_core/config.py::effective_proxies</a>
- <a href="../estorides_core/config.py#L366-L372">estorides_core/config.py::CacheConfig</a>
- <a href="../estorides_core/config.py#L373-L378">estorides_core/config.py::is_active</a>
- <a href="../estorides_core/config.py#L379-L392">estorides_core/config.py::PivotPolicyConfig</a>

### estorides_core: hypothesis_engine (4)

estorides_core: hypothesis_engine groups 19 files (py) around SourceReliability, Credibility, SourceType, ConfidenceInput, __post_init__. estorides_core.change_detection

**Related Classes/Methods**:

- <a href="../estorides_core/reliability_scoring.py#L37-L47">estorides_core/reliability_scoring.py::SourceReliability</a>
- <a href="../estorides_core/reliability_scoring.py#L48-L58">estorides_core/reliability_scoring.py::Credibility</a>
- <a href="../estorides_core/reliability_scoring.py#L59-L242">estorides_core/reliability_scoring.py::SourceType</a>
- <a href="../estorides_core/reliability_scoring.py#L243-L252">estorides_core/reliability_scoring.py::ConfidenceInput</a>
- <a href="../estorides_core/reliability_scoring.py#L253-L262">estorides_core/reliability_scoring.py::__post_init__</a>
- <a href="../estorides_core/reliability_scoring.py#L263-L279">estorides_core/reliability_scoring.py::ConfidenceResult</a>
- <a href="../estorides_core/reliability_scoring.py#L280-L286">estorides_core/reliability_scoring.py::_corroboration_weight</a>
- <a href="../estorides_core/reliability_scoring.py#L287-L296">estorides_core/reliability_scoring.py::_freshness_weight</a>

### estorides_core: estorides (5)

estorides_core: estorides groups 17 files (js, py) around SqliteStore, __init__, _init_schema, _tx, close. estorides CLI.

**Related Classes/Methods**:

- <a href="../estorides_core/sqlite_store.py#L34-L49">estorides_core/sqlite_store.py::SqliteStore</a>
- <a href="../estorides_core/sqlite_store.py#L50-L65">estorides_core/sqlite_store.py::__init__</a>
- <a href="../estorides_core/sqlite_store.py#L66-L71">estorides_core/sqlite_store.py::_init_schema</a>
- <a href="../estorides_core/sqlite_store.py#L72-L81">estorides_core/sqlite_store.py::_tx</a>
- <a href="../estorides_core/sqlite_store.py#L82-L88">estorides_core/sqlite_store.py::close</a>
- <a href="../estorides_core/sqlite_store.py#L89-L108">estorides_core/sqlite_store.py::__del__</a>
- <a href="../estorides_core/sqlite_store.py#L109-L111">estorides_core/sqlite_store.py::DictMixin</a>
- <a href="../estorides_core/sqlite_store.py#L112-L119">estorides_core/sqlite_store.py::to_dict</a>

### estorides_core: graph_bundle (6)

estorides_core: graph_bundle groups 15 files (py) around family_color_from_name, node_value, force_settings, _req_str, _opt_str. estorides_core.__init__

**Related Classes/Methods**:

- <a href="../estorides_core/graph_force.py#L48-L64">estorides_core/graph_force.py::family_color_from_name</a>
- <a href="../estorides_core/graph_force.py#L65-L69">estorides_core/graph_force.py::node_value</a>
- <a href="../estorides_core/graph_force.py#L70-L96">estorides_core/graph_force.py::force_settings</a>
- <a href="../estorides_core/graph_force.py#L97-L106">estorides_core/graph_force.py::_req_str</a>
- <a href="../estorides_core/graph_force.py#L107-L112">estorides_core/graph_force.py::_opt_str</a>
- <a href="../estorides_core/graph_force.py#L113-L123">estorides_core/graph_force.py::_opt_int</a>
- <a href="../estorides_core/graph_force.py#L124-L149">estorides_core/graph_force.py::_degrees</a>
- <a href="../estorides_core/graph_force.py#L150-L160">estorides_core/graph_force.py::_is_bridge</a>

### estorides_core: people_intel (7)

estorides_core: people_intel groups 15 files (py) around CloudAsset, to_dict, CloudAssetDiscoveryResult, to_dict, generate_bucket_names.

**Related Classes/Methods**:

- <a href="../estorides_core/cloud_asset_discovery.py#L34-L44">estorides_core/cloud_asset_discovery.py::CloudAsset</a>
- <a href="../estorides_core/cloud_asset_discovery.py#L45-L49">estorides_core/cloud_asset_discovery.py::to_dict</a>
- <a href="../estorides_core/cloud_asset_discovery.py#L50-L55">estorides_core/cloud_asset_discovery.py::CloudAssetDiscoveryResult</a>
- <a href="../estorides_core/cloud_asset_discovery.py#L56-L64">estorides_core/cloud_asset_discovery.py::to_dict</a>
- <a href="../estorides_core/cloud_asset_discovery.py#L65-L83">estorides_core/cloud_asset_discovery.py::generate_bucket_names</a>
- <a href="../estorides_core/cloud_asset_discovery.py#L84-L92">estorides_core/cloud_asset_discovery.py::assess_bucket</a>
- <a href="../estorides_core/cloud_asset_discovery.py#L93-L94">estorides_core/cloud_asset_discovery.py::CloudAssetDiscoveryError</a>
- <a href="../estorides_core/code_exposure.py#L47-L56">estorides_core/code_exposure.py::CodeFinding</a>

### estorides_export (8)

estorides_export groups 15 files (py) around Entity, to_dict, _looks_like_phone, normalize_query, detect_query_type. estorides_core.entity_extraction

**Related Classes/Methods**:

- <a href="../estorides_core/entity_extraction.py#L22-L33">estorides_core/entity_extraction.py::Entity</a>
- <a href="../estorides_core/entity_extraction.py#L34-L48">estorides_core/entity_extraction.py::to_dict</a>
- <a href="../estorides_core/entity_extraction.py#L49-L56">estorides_core/entity_extraction.py::_looks_like_phone</a>
- <a href="../estorides_core/entity_extraction.py#L57-L99">estorides_core/entity_extraction.py::normalize_query</a>
- <a href="../estorides_core/entity_extraction.py#L100-L126">estorides_core/entity_extraction.py::detect_query_type</a>
- <a href="../estorides_core/entity_extraction.py#L127-L139">estorides_core/entity_extraction.py::_is_valid_domain</a>
- <a href="../estorides_core/entity_extraction.py#L140-L145">estorides_core/entity_extraction.py::_context</a>
- <a href="../estorides_core/entity_extraction.py#L146-L199">estorides_core/entity_extraction.py::extract_from_text</a>

### estorides_core: tool_install (9)

estorides_core: tool_install groups 12 files (py) around ToolError, ToolNotAllowedError, ToolInjectionError, ToolNotFoundError, ToolTimeoutError. estorides_core.lan_runner

**Related Classes/Methods**:

- <a href="../estorides_core/tool_runner.py#L17-L20">estorides_core/tool_runner.py::ToolError</a>
- <a href="../estorides_core/tool_runner.py#L21-L24">estorides_core/tool_runner.py::ToolNotAllowedError</a>
- <a href="../estorides_core/tool_runner.py#L25-L28">estorides_core/tool_runner.py::ToolInjectionError</a>
- <a href="../estorides_core/tool_runner.py#L29-L32">estorides_core/tool_runner.py::ToolNotFoundError</a>
- <a href="../estorides_core/tool_runner.py#L33-L37">estorides_core/tool_runner.py::ToolTimeoutError</a>
- <a href="../estorides_core/tool_runner.py#L38-L50">estorides_core/tool_runner.py::ToolResult</a>
- <a href="../estorides_core/tool_runner.py#L51-L58">estorides_core/tool_runner.py::to_dict</a>
- <a href="../estorides_core/tool_runner.py#L59-L85">estorides_core/tool_runner.py::from_failure</a>

### estorides_core: source_health_monitoring (10)

estorides_core: source_health_monitoring groups 3 files (py) around SourceHealthStatus, SourceHealthConfig, __post_init__, SourceHealthInput, __post_init__. estorides_core.source_health_monitoring

**Related Classes/Methods**:

- <a href="../estorides_core/source_health_monitoring.py#L31-L41">estorides_core/source_health_monitoring.py::SourceHealthStatus</a>
- <a href="../estorides_core/source_health_monitoring.py#L42-L57">estorides_core/source_health_monitoring.py::SourceHealthConfig</a>
- <a href="../estorides_core/source_health_monitoring.py#L58-L97">estorides_core/source_health_monitoring.py::__post_init__</a>
- <a href="../estorides_core/source_health_monitoring.py#L98-L111">estorides_core/source_health_monitoring.py::SourceHealthInput</a>
- <a href="../estorides_core/source_health_monitoring.py#L112-L133">estorides_core/source_health_monitoring.py::__post_init__</a>
- <a href="../estorides_core/source_health_monitoring.py#L134-L145">estorides_core/source_health_monitoring.py::SourceHealthResult</a>
- <a href="../estorides_core/source_health_monitoring.py#L146-L159">estorides_core/source_health_monitoring.py::to_dict</a>
- <a href="../estorides_core/source_health_monitoring.py#L160-L172">estorides_core/source_health_monitoring.py::DashboardSummary</a>
