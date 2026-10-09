# API (page 2 of 3)
Previous: [API.md](API.md)

## estorides_core/people_intel.py
Imported by: `estorides_core/recon_pipeline.py`, `tests/test_people_intel.py`
- `BreachRecord.to_dict` (method) `estorides_core/people_intel.py:22` `def to_dict(self)`
- `Employee.to_dict` (method) `estorides_core/people_intel.py:40` `def to_dict(self)`
- `BreachContext.to_dict` (method) `estorides_core/people_intel.py:62` `def to_dict(self)`
- `PeopleIntelResult.to_dict` (method) `estorides_core/people_intel.py:75` `def to_dict(self)`
- `PeopleIntelResult.infer_email_pattern` (method) `estorides_core/people_intel.py:98` `def infer_email_pattern(emails)`
- `PeopleIntelResult.correlate_breaches` (method) `estorides_core/people_intel.py:153` `def correlate_breaches(employees)`
- `PeopleIntelResult.analyse_employees` (method) `estorides_core/people_intel.py:176` `def analyse_employees(employees, domain)`

## estorides_core/pivot_engine.py
Depends on: `estorides_core/config.py`
Imported by: `estorides_core/discoverer.py`, `estorides_web.py`, `tests/test_structured_extraction.py`
- `EventSink.emit` (method) `estorides_core/pivot_engine.py:62` `def emit(self, event)` -- Publish one event.
- `ListEventSink.__init__` (method) `estorides_core/pivot_engine.py:70` `def __init__(self)`
- `ListEventSink.emit` (method) `estorides_core/pivot_engine.py:73` `def emit(self, event)`
- `BufferedEventSink.__init__` (method) `estorides_core/pivot_engine.py:87` `def __init__(self, capacity)`
- `BufferedEventSink.emit` (method) `estorides_core/pivot_engine.py:94` `def emit(self, event)`
- `EntityRunner.run` (method) `estorides_core/pivot_engine.py:120` `def run(self, query)`
- `PivotBudget.time_left` (method) `estorides_core/pivot_engine.py:155` `def time_left(self)` -- Seconds remaining before the global wall-clock deadline.
- `PivotBudget.exhausted` (method) `estorides_core/pivot_engine.py:159` `def exhausted(self)` -- Reason the run must stop, or None while budget remains.
- `PivotEngine.__init__` (method) `estorides_core/pivot_engine.py:198` `def __init__(self, runner, sink)`
- `PivotEngine.run` (method) `estorides_core/pivot_engine.py:264` `def run(self, seed_type, seed_value)` -- Execute the cross-search from `(seed_type, seed_value)`.

## estorides_core/recon_fusion.py
Depends on: `estorides_core/config.py`, `estorides_core/ids.py`, `estorides_core/reliability_scoring.py`
Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`
- `RelevanceTier.ordered` (method) `estorides_core/recon_fusion.py:40` `def ordered(cls)` -- Return tiers in canonical display order.
- `GroupedEntity.to_dict` (method) `estorides_core/recon_fusion.py:64` `def to_dict(self)`
- `FusionResult.to_dict` (method) `estorides_core/recon_fusion.py:95` `def to_dict(self)`
- `ReconFusionEngine.__init__` (method) `estorides_core/recon_fusion.py:166` `def __init__(self, config)`
- `ReconFusionEngine.classify` (method) `estorides_core/recon_fusion.py:169` `def classify(self, query, query_type, observations, entities)` -- Classify raw observations and entities into relevance-tiered groups.

## estorides_core/recon_pipeline.py
Depends on: `estorides_core/cloud_asset_discovery.py`, `estorides_core/code_exposure.py`, `estorides_core/pdns_monitor.py`, `estorides_core/people_intel.py`, `estorides_core/supply_chain.py`, `estorides_core/tech_fingerprint.py`, `estorides_core/vuln_correlation.py`
- `run_passive_recon` (function) `estorides_core/recon_pipeline.py:22` `def run_passive_recon(query, headers, html, cookies, employees, code_findings, third_parties, pdns_subdomains...`

## estorides_core/relationship_inference.py
Imported by: `estorides_core/orchestrator.py`
- `RelationshipInferer.__call__` (method) `estorides_core/relationship_inference.py:51` `def __call__(self, observation, query, kg)`
- `RelationshipInferer.register_inferer` (method) `estorides_core/relationship_inference.py:63` `def register_inferer(source_name)` -- Decorator: register `func` as the inferer for `source_name`.
- `RelationshipInferer.deco` (method) `estorides_core/relationship_inference.py:70` `def deco(func)`
- `RelationshipInferer.infer_relationship` (method) `estorides_core/relationship_inference.py:78` `def infer_relationship(observation, query, kg)` -- Dispatch an observation to its inferer (if any).

## estorides_core/reliability_scoring.py
Imported by: `estorides_core/change_detection.py`, `estorides_core/fusion_store.py`, `estorides_core/hypothesis_engine.py`, `estorides_core/recon_fusion.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/test_change_detection.py`, `tests/test_hypothesis_engine.py`, `tests/test_reliability_scoring.py`
- `ConfidenceResult.compute_confidence` (method) `estorides_core/reliability_scoring.py:312` `def compute_confidence(inp)` -- Compute the audit-trailed confidence score for one observation.
- `ConfidenceResult.merge_confidence` (method) `estorides_core/reliability_scoring.py:350` `def merge_confidence(existing, new_observation)` -- Merge a new observation's confidence into an existing entity score.
- `ConfidenceResult.reliability_from_name` (method) `estorides_core/reliability_scoring.py:400` `def reliability_from_name(source_name)` -- Look up the reliability for a source by name; never raises.
- `ConfidenceResult.source_type_from_name` (method) `estorides_core/reliability_scoring.py:415` `def source_type_from_name(source_name)` -- Look up the source type hierarchy for a source by name; never raises.
- `ConfidenceResult.reliability_weight` (method) `estorides_core/reliability_scoring.py:430` `def reliability_weight(source_name, overrides)` -- Numeric reliability weight for a source name; never raises.
- `ConfidenceResult.reliability_weight_for_letter` (method) `estorides_core/reliability_scoring.py:452` `def reliability_weight_for_letter(letter)` -- Numeric weight for a reliability letter (A-F); never raises.

## estorides_core/scope.py
Imported by: `estorides_cli.py`, `tests/test_scope.py`
- `normalise_asset` (function) `estorides_core/scope.py:52` `def normalise_asset(raw)` -- Reduce a raw asset string to a comparable host or IP literal.
- `is_ip` (function) `estorides_core/scope.py:79` `def is_ip(asset)` -- True when `asset` parses as a bare IPv4 or IPv6 address.
- `ScopeRule.matches` (method) `estorides_core/scope.py:93` `def matches(self, asset)` -- True when `asset` (already normalised) is covered by this rule.
- `ScopeRule.describe` (method) `estorides_core/scope.py:97` `def describe(self)` -- Human-readable form of the rule, for reports and audit.
- `WildcardRule.matches` (method) `estorides_core/scope.py:107` `def matches(self, asset)`
- `WildcardRule.describe` (method) `estorides_core/scope.py:112` `def describe(self)`
- `ExactHostRule.matches` (method) `estorides_core/scope.py:122` `def matches(self, asset)`
- `ExactHostRule.describe` (method) `estorides_core/scope.py:125` `def describe(self)`
- `CidrRule.matches` (method) `estorides_core/scope.py:135` `def matches(self, asset)`
- `CidrRule.describe` (method) `estorides_core/scope.py:143` `def describe(self)`
- `RegexRule.matches` (method) `estorides_core/scope.py:153` `def matches(self, asset)`
- `RegexRule.describe` (method) `estorides_core/scope.py:156` `def describe(self)`
- `RegexRule.parse_rule` (method) `estorides_core/scope.py:211` `def parse_rule(line)` -- Parse one rule line into a ScopeRule, or None for blank/comment/invalid.
- `RegexRule.parse_rules` (method) `estorides_core/scope.py:223` `def parse_rules(lines)` -- Parse many rule lines, skipping blanks, comments and invalid entries.
- `ScopeMatcher.__init__` (method) `estorides_core/scope.py:242` `def __init__(self, in_scope, out_of_scope)`
- `ScopeMatcher.in_rules` (method) `estorides_core/scope.py:251` `def in_rules(self)`
- `ScopeMatcher.out_rules` (method) `estorides_core/scope.py:255` `def out_rules(self)`
- `ScopeMatcher.classify` (method) `estorides_core/scope.py:258` `def classify(self, raw_asset)` -- Return IN_SCOPE, OUT_OF_SCOPE or UNKNOWN for a single asset.
- `ScopeMatcher.partition` (method) `estorides_core/scope.py:269` `def partition(self, assets)` -- Bucket many assets, returning sorted, de-duplicated lists.
- `ScopeMatcher.load_rules_file` (method) `estorides_core/scope.py:285` `def load_rules_file(path)` -- Build a matcher from a rules file, honouring the out-of-scope divider.
- `ScopeMatcher.load_assets` (method) `estorides_core/scope.py:303` `def load_assets(path)` -- Read assets from a file: a discover surface JSON or a flat host list.
- `ScopeReport.hosts` (method) `estorides_core/scope.py:352` `def hosts(self)` -- In-scope hostnames (everything in-scope that is not an IP).
- `ScopeReport.ips` (method) `estorides_core/scope.py:357` `def ips(self)` -- In-scope bare IP addresses.
- `ScopeReport.to_dict` (method) `estorides_core/scope.py:361` `def to_dict(self)`
- `ScopeReport.build_report` (method) `estorides_core/scope.py:371` `def build_report(matcher, assets)` -- Classify `assets` with `matcher` and return a :class:`ScopeReport`.
- `ScopeReport.write_flat_lists` (method) `estorides_core/scope.py:381` `def write_flat_lists(report, out_dir)` -- Write newline-delimited flat lists for piping into active tooling.

## estorides_core/search_telemetry.py
Depends on: `estorides_core/config.py`
Imported by: `estorides_web.py`, `tests/properties/test_search_telemetry_properties.py`, `tests/test_csp_safe_styles.py`, `tests/test_search_telemetry.py`, `tests/test_ui_professional.py`
- `InvalidTelemetryConfigError.disallowed_brands_in` (method) `estorides_core/search_telemetry.py:75` `def disallowed_brands_in(text)` -- Return the third-party brand tokens found in ``text``.
- `InvalidTelemetryConfigError.emoji_in` (method) `estorides_core/search_telemetry.py:89` `def emoji_in(text)` -- Return the emoji glyphs found in ``text``, de-duplicated in order.
- `InvalidTelemetryConfigError.percent_encoded_emoji_in` (method) `estorides_core/search_telemetry.py:103` `def percent_encoded_emoji_in(text)` -- Return percent-encoded supplementary-plane emoji sequences in ``text``.
- `SearchTelemetry.__init__` (method) `estorides_core/search_telemetry.py:223` `def __init__(self, config)`
- `SearchTelemetry.shortcuts` (method) `estorides_core/search_telemetry.py:229` `def shortcuts(self)` -- Return the keyboard-shortcut catalog.
- `SearchTelemetry.tips` (method) `estorides_core/search_telemetry.py:233` `def tips(self)` -- Return the onboarding tips catalog.
- `SearchTelemetry.phases` (method) `estorides_core/search_telemetry.py:237` `def phases(self)` -- Return the search-phase vocabulary.
- `SearchTelemetry.phase` (method) `estorides_core/search_telemetry.py:241` `def phase(self, key)` -- Return the phase for ``key`` or raise :class:`UnknownPhaseError`.
- `SearchTelemetry.progress` (method) `estorides_core/search_telemetry.py:249` `def progress(self, completed, total, phase_key)` -- Compute a clamped, render-ready :class:`ProgressView`.
- `SearchTelemetry.context` (method) `estorides_core/search_telemetry.py:288` `def context(self)` -- Return the JSON-serialisable catalog for template/JS injection.

## estorides_core/socmint.py
Imported by: `estorides_web.py`, `tests/test_socmint.py`
- `ProfileMatch.to_dict` (method) `estorides_core/socmint.py:92` `def to_dict(self)`
- `SocialMediaProfile.to_dict` (method) `estorides_core/socmint.py:119` `def to_dict(self)`
- `SocialMediaInferer.__init__` (method) `estorides_core/socmint.py:214` `def __init__(self)`
- `SocialMediaInferer.resolve` (method) `estorides_core/socmint.py:218` `def resolve(self, username, platforms)` -- Build a SocialMediaProfile for a username across all platforms.
- `SocialMediaInferer.discover_from_text` (method) `estorides_core/socmint.py:311` `def discover_from_text(self, text)` -- Extract social media profiles from a text blob.
- `SocialMediaInferer.platform_list` (method) `estorides_core/socmint.py:344` `def platform_list(self)` -- Return the full platform registry as a serialisable list.

## estorides_core/source_health_monitoring.py
Imported by: `tests/properties/test_source_health_monitoring_properties.py`, `tests/test_source_health_monitoring.py`
- `SourceHealthResult.to_dict` (method) `estorides_core/source_health_monitoring.py:146` `def to_dict(self)`
- `HealthDashboard.to_dict` (method) `estorides_core/source_health_monitoring.py:184` `def to_dict(self)`
- `HealthDashboard.compute_health` (method) `estorides_core/source_health_monitoring.py:235` `def compute_health(inp, config)` -- Compute the health assessment for a single source.
- `HealthDashboard.build_dashboard` (method) `estorides_core/source_health_monitoring.py:295` `def build_dashboard(records, config)` -- Build a health dashboard from per-source health inputs.

## estorides_core/source_loader.py
Depends on: `estorides_core/config.py`
Imported by: `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_opsec_contact.py`, `tests/test_socmint.py`, `tests/test_source_loader.py`, `tests/test_system_app_sources.py`
- `Source.__init__` (method) `estorides_core/source_loader.py:28` `def __init__(self, data)`
- `SourceRegistry.__init__` (method) `estorides_core/source_loader.py:41` `def __init__(self, sources_dir)`
- `SourceRegistry.load` (method) `estorides_core/source_loader.py:47` `def load(self)`
- `SourceRegistry.get` (method) `estorides_core/source_loader.py:200` `def get(self, name)`
- `SourceRegistry.all` (method) `estorides_core/source_loader.py:203` `def all(self)`
- `SourceRegistry.by_category` (method) `estorides_core/source_loader.py:206` `def by_category(self, category)`
- `SourceRegistry.categories` (method) `estorides_core/source_loader.py:209` `def categories(self)`
- `SourceRegistry.names` (method) `estorides_core/source_loader.py:212` `def names(self)`
- `SourceRegistry.filter` (method) `estorides_core/source_loader.py:215` `def filter(self)` -- Return sources matching the given predicates.
- `SourceRegistry.write_source_file` (method) `estorides_core/source_loader.py:272` `def write_source_file(self, data)` -- Write a source dict to the correct YAML file, overwriting if exists.
- `SourceRegistry.delete_source_file` (method) `estorides_core/source_loader.py:342` `def delete_source_file(self, name)` -- Delete a source file by name.
- `SourceRegistry.summary` (method) `estorides_core/source_loader.py:351` `def summary(self)` -- Compact summary used by /api/status.

## estorides_core/sqlite_store.py
Imported by: `estorides_core/cases.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/monitoring.py`, `tests/test_sqlite_store.py`
- `SqliteStore.__init__` (method) `estorides_core/sqlite_store.py:50` `def __init__(self, path)`
- `SqliteStore.close` (method) `estorides_core/sqlite_store.py:82` `def close(self)`
- `DictMixin.to_dict` (method) `estorides_core/sqlite_store.py:93` `def to_dict(self)`

## estorides_core/ssrf_guard.py
Imported by: `estorides_core/alerter.py`, `estorides_core/async_client.py`, `estorides_core/feeds.py`, `estorides_core/intel_resolver.py`, `estorides_core/ontology.py`, `estorides_core/osiris_sources.py`, `tests/test_security_remediation.py`
- `GuardResult.check_url` (method) `estorides_core/ssrf_guard.py:194` `def check_url(url)` -- Validate a URL for outbound fetch.
- `GuardResult.assert_safe` (method) `estorides_core/ssrf_guard.py:262` `def assert_safe(url)` -- Raise SSRFError if `url` is not safe to fetch.

## estorides_core/supply_chain.py
Imported by: `estorides_core/recon_pipeline.py`, `tests/test_supply_chain.py`
- `ThirdParty.to_dict` (method) `estorides_core/supply_chain.py:61` `def to_dict(self)`
- `SharedInfra.to_dict` (method) `estorides_core/supply_chain.py:73` `def to_dict(self)`
- `Relationship.to_dict` (method) `estorides_core/supply_chain.py:84` `def to_dict(self)`
- `SupplyChainResult.to_dict` (method) `estorides_core/supply_chain.py:96` `def to_dict(self)`
- `SupplyChainResult.detect_mx_provider` (method) `estorides_core/supply_chain.py:106` `def detect_mx_provider(mx_records)`
- `SupplyChainResult.detect_ns_provider` (method) `estorides_core/supply_chain.py:114` `def detect_ns_provider(ns_records)`
- `SupplyChainResult.detect_cdn` (method) `estorides_core/supply_chain.py:122` `def detect_cdn(cname)`
- `SupplyChainResult.analyse_third_parties` (method) `estorides_core/supply_chain.py:129` `def analyse_third_parties(third_parties, subsidiaries)`
- `SupplyChainResult.detect_shared_infrastructure` (method) `estorides_core/supply_chain.py:140` `def detect_shared_infrastructure(asn)`

## estorides_core/system_app_sources.py
Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`
- `SystemAppResult.to_dict` (method) `estorides_core/system_app_sources.py:76` `def to_dict(self)`
- `SystemAppResult.is_system_app` (method) `estorides_core/system_app_sources.py:81` `def is_system_app(source)` -- True when a source dict is a system_app (or has a binary tool).
- `SystemAppResult.tool_available` (method) `estorides_core/system_app_sources.py:91` `def tool_available(binary)` -- Resolve a binary on the filesystem (shutil.which).
- `SystemAppResult.render_args` (method) `estorides_core/system_app_sources.py:96` `def render_args(args, query, outdir)` -- Substitute ``{query}``/``{outdir}`` placeholders in an args template.
- `SystemAppResult.repl` (method) `estorides_core/system_app_sources.py:109` `def repl(m)`
- `SystemAppResult.parser` (method) `estorides_core/system_app_sources.py:165` `def parser(payload)`
- `SystemAppResult.parse_amass_json` (method) `estorides_core/system_app_sources.py:193` `def parse_amass_json(payload)` -- amass ``-json`` output: one JSON object per line (DNS + infra).
- `SystemAppResult.parse_maigret_json` (method) `estorides_core/system_app_sources.py:225` `def parse_maigret_json(payload)` -- maigret ``--json simple``: one object keyed by site name.
- `SystemAppResult.parse_phoneinfoga_json` (method) `estorides_core/system_app_sources.py:247` `def parse_phoneinfoga_json(payload)` -- phoneinfoga v2 ``scan``: a single JSON object (possibly after logs).
- `SystemAppResult.parse_sherlock_text` (method) `estorides_core/system_app_sources.py:260` `def parse_sherlock_text(payload)`
- `SystemAppResult.parse_holehe_text` (method) `estorides_core/system_app_sources.py:265` `def parse_holehe_text(payload)`
- `SystemAppResult.parse_wafw00f_text` (method) `estorides_core/system_app_sources.py:270` `def parse_wafw00f_text(payload)`
- `SystemAppResult.parse_sublist3r_lines` (method) `estorides_core/system_app_sources.py:275` `def parse_sublist3r_lines(payload)`
- `SystemAppResult.parse_dnsrecon_text` (method) `estorides_core/system_app_sources.py:280` `def parse_dnsrecon_text(payload)`
- `SystemAppResult.parse_dnsenum_text` (method) `estorides_core/system_app_sources.py:285` `def parse_dnsenum_text(payload)`
- `SystemAppResult.parse_fierce_text` (method) `estorides_core/system_app_sources.py:292` `def parse_fierce_text(payload)`
- `SystemAppResult.parse_dmitry_text` (method) `estorides_core/system_app_sources.py:297` `def parse_dmitry_text(payload)`
- `SystemAppResult.parse_urlcrazy_text` (method) `estorides_core/system_app_sources.py:302` `def parse_urlcrazy_text(payload)`
- `SystemAppResult.parse_metagoofil_text` (method) `estorides_core/system_app_sources.py:307` `def parse_metagoofil_text(payload)`
- `SystemAppResult.parse_whatweb_text` (method) `estorides_core/system_app_sources.py:312` `def parse_whatweb_text(payload)`
- `SystemAppResult.parse_theharvester_text` (method) `estorides_core/system_app_sources.py:317` `def parse_theharvester_text(payload)`
- `SystemAppResult.parse_usufy_text` (method) `estorides_core/system_app_sources.py:322` `def parse_usufy_text(payload)`
- `SystemAppResult.parse_mailfy_text` (method) `estorides_core/system_app_sources.py:327` `def parse_mailfy_text(payload)`
- `SystemAppResult.parse_phonefy_text` (method) `estorides_core/system_app_sources.py:332` `def parse_phonefy_text(payload)`
- `SystemAppResult.parse_searchfy_text` (method) `estorides_core/system_app_sources.py:337` `def parse_searchfy_text(payload)`
- `SystemAppResult.parse_tool_output` (method) `estorides_core/system_app_sources.py:365` `def parse_tool_output(source_name, parser_name, data)` -- Parse tool output with the declared parser; never raises.
- `SystemAppResult.execute` (method) `estorides_core/system_app_sources.py:396` `def execute(source, query)` -- Execute one system_app source through the tool_runner sandbox.
- `SystemAppResult.fail` (method) `estorides_core/system_app_sources.py:418` `def fail(code, message)`

## estorides_core/tech_fingerprint.py
Imported by: `estorides_core/recon_pipeline.py`, `tests/test_tech_fingerprint.py`
- `Tech.to_dict` (method) `estorides_core/tech_fingerprint.py:97` `def to_dict(self)`
- `TechFingerprintResult.to_dict` (method) `estorides_core/tech_fingerprint.py:107` `def to_dict(self)`
- `TechFingerprintResult.fingerprint` (method) `estorides_core/tech_fingerprint.py:115` `def fingerprint(headers, html, cookies, status)`

## estorides_core/tool_install.py
Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
Imported by: `estorides_web_tools.py`, `tests/test_central_config.py`, `tests/test_tool_doctor.py`, `tests/test_tool_install.py`
- `InstallRecipe.has_apt` (method) `estorides_core/tool_install.py:95` `def has_apt(self)`
- `InstallRecipe.has_git` (method) `estorides_core/tool_install.py:98` `def has_git(self)`
- `InstallResult.to_dict` (method) `estorides_core/tool_install.py:113` `def to_dict(self)`
- `InstallResult.is_valid_recipe_name` (method) `estorides_core/tool_install.py:169` `def is_valid_recipe_name(name)` -- True when ``name`` is a safe recipe/tool identifier (no separators).
- `InstallResult.is_valid_binary` (method) `estorides_core/tool_install.py:174` `def is_valid_binary(name)` -- True when ``name`` is a plausible bare binary name (no path).
- `InstallResult.load_recipe` (method) `estorides_core/tool_install.py:210` `def load_recipe(name)` -- Load a tool recipe from ``tool_recipes/<name>.yaml`` (or ``None``).
- `InstallResult.recipe_available` (method) `estorides_core/tool_install.py:254` `def recipe_available(name)` -- True when a recipe exists for ``name`` (the UI gates the button on this).
- `InstallResult.tool_available` (method) `estorides_core/tool_install.py:259` `def tool_available(binary)` -- True when the binary resolves on PATH (mirrors system_app_sources).
- `InstallResult.list_recipes` (method) `estorides_core/tool_install.py:270` `def list_recipes()` -- Names of all tool recipe files in ``tool_recipes/`` (sorted).
- `ToolStatus.to_dict` (method) `estorides_core/tool_install.py:287` `def to_dict(self)`
- `ToolStatus.doctor` (method) `estorides_core/tool_install.py:321` `def doctor(sources_dir)` -- Read-only readiness report over system_app binaries + recipes.
- `ToolStatus.install_tool` (method) `estorides_core/tool_install.py:414` `def install_tool(tool_name)` -- Install a missing tool from its recipe (if any).
- `ToolStatus.main` (method) `estorides_core/tool_install.py:516` `def main(argv)` -- Minimal CLI: ``python -m estorides_core.tool_install <tool> [--force]``.

## estorides_core/tool_runner.py
Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
Imported by: `estorides_core/active_recon.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/properties/test_tool_runner_properties.py`, `tests/test_active_recon.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`
- `ToolResult.to_dict` (method) `estorides_core/tool_runner.py:51` `def to_dict(self)`
- `ToolResult.from_failure` (method) `estorides_core/tool_runner.py:59` `def from_failure(cls, tool_name, error_code, error_message, duration_s, exit_code, stdout, stderr, parsed_entities)`
- `ToolErrorResult.to_dict` (method) `estorides_core/tool_runner.py:93` `def to_dict(self)`
- `ToolErrorResult.run_tool` (method) `estorides_core/tool_runner.py:156` `def run_tool(tool_name, args, target, timeout, max_output_bytes, cwd)`

## estorides_core/transforms.py
Depends on: `estorides_core/intel_resolver.py`
Imported by: `estorides_web.py`, `tests/test_transforms.py`
- `Transform.summary` (method) `estorides_core/transforms.py:83` `def summary(self)`
- `Transform.run` (method) `estorides_core/transforms.py:122` `def run(ent_type, value)`
- `TransformRegistry.__init__` (method) `estorides_core/transforms.py:228` `def __init__(self)`
- `TransformRegistry.register` (method) `estorides_core/transforms.py:231` `def register(self, t)`
- `TransformRegistry.for_type` (method) `estorides_core/transforms.py:234` `def for_type(self, ent_type)`
- `TransformRegistry.run` (method) `estorides_core/transforms.py:246` `def run(self, transform_id, ent_type, value)`
- `TransformRegistry.load_yaml_dir` (method) `estorides_core/transforms.py:280` `def load_yaml_dir(self, directory)` -- Register every transform declared in ``*.yaml`` under `directory`.
- `TransformRegistry.run` (method) `estorides_core/transforms.py:335` `def run(ent_type, value)`
- `TransformRegistry.sub` (method) `estorides_core/transforms.py:338` `def sub(s, depth)`
- `TransformRegistry.iter_sse_events` (method) `estorides_core/transforms.py:406` `def iter_sse_events(transform_id, ent_type, value, runner)` -- Yield ``(kind, payload)`` tuples for the SSE stream endpoint.

## estorides_core/transliteration.py
Imported by: `estorides_core/entity_resolution.py`, `tests/test_entity_resolution.py`
- `to_latin` (function) `estorides_core/transliteration.py:87` `def to_latin(text)` -- Return a lowercased, diacritic-free Latin transliteration.
- `consonant_skeleton` (function) `estorides_core/transliteration.py:112` `def consonant_skeleton(text)` -- Return the Latin transliteration with vowels and spaces removed.
- `is_non_latin` (function) `estorides_core/transliteration.py:139` `def is_non_latin(text)` -- True if any character is outside the Basic Latin / Latin-1 range.

## estorides_core/validation.py
Depends on: `estorides_core/entity_extraction.py`
Imported by: `estorides_cli.py`, `estorides_web.py`, `tests/test_tool_runner.py`
- `QueryValidationError.__init__` (method) `estorides_core/validation.py:57` `def __init__(self, reason, message)`
- `Query.validate_query` (method) `estorides_core/validation.py:85` `def validate_query(raw)` -- Validate and normalise a user query string.

## estorides_core/vuln_correlation.py
Imported by: `estorides_core/recon_pipeline.py`, `tests/test_vuln_correlation.py`
- `DefaultCred.to_dict` (method) `estorides_core/vuln_correlation.py:19` `def to_dict(self)`
- `VulnEntry.to_dict` (method) `estorides_core/vuln_correlation.py:38` `def to_dict(self)`
- `VulnCorrelationResult.to_dict` (method) `estorides_core/vuln_correlation.py:52` `def to_dict(self)`
- `VulnCorrelationResult.lookup_cve_for_tech` (method) `estorides_core/vuln_correlation.py:169` `def lookup_cve_for_tech(tech_name, version)`
- `VulnCorrelationResult.correlate_technologies` (method) `estorides_core/vuln_correlation.py:202` `def correlate_technologies(technologies)`
- `VulnCorrelationResult.compute_attack_readiness` (method) `estorides_core/vuln_correlation.py:228` `def compute_attack_readiness(vulnerabilities)`

## estorides_core/web_security.py
Imported by: `estorides_web.py`, `estorides_web_tools.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_hardening.py`, `tests/test_map_basemap.py`, `tests/test_security_remediation.py`, `tests/test_web_helpers.py`
- `build_https_url` (function) `estorides_core/web_security.py:58` `def build_https_url(public_host, path, query_string)` -- Build a safe HTTPS redirect target from a trusted host and client path.
- `WebSecurityConfig.is_cors_enabled` (method) `estorides_core/web_security.py:128` `def is_cors_enabled(self)`
- `WebSecurityConfig.is_origin_allowed` (method) `estorides_core/web_security.py:132` `def is_origin_allowed(self)` -- CORS is opt-in; this is the runtime check used by the after_request hook.
- `WebSecurityConfig.load_security_config` (method) `estorides_core/web_security.py:144` `def load_security_config()` -- Resolve the security policy from env vars.
- `WebSecurityConfig.install_security` (method) `estorides_core/web_security.py:169` `def install_security(app, cfg)` -- Wire security middleware into a Flask app.
- `WebSecurityConfig.make_auth_gate` (method) `estorides_core/web_security.py:321` `def make_auth_gate()` -- Build the auth gate from the current environment.
- `AuthGate.enabled` (method) `estorides_core/web_security.py:351` `def enabled(self)`
- `AuthGate.check` (method) `estorides_core/web_security.py:354` `def check(self)`
- `AuthGate.auth_meta_for_index` (method) `estorides_core/web_security.py:362` `def auth_meta_for_index(self)` -- Token to embed in `index.html` so the UI can auto-authenticate.
- `AuthGate.issue_session_cookie_kwargs` (method) `estorides_core/web_security.py:371` `def issue_session_cookie_kwargs(self)` -- Arguments for `set_cookie` to install the session cookie.
- `AuthGate.require_auth` (method) `estorides_core/web_security.py:388` `def require_auth(view)` -- Decorator: enforce the bearer-token gate on a view.
- `AuthGate.wrapper` (method) `estorides_core/web_security.py:402` `def wrapper()`
- `AuthGate.install_auth_gate` (method) `estorides_core/web_security.py:421` `def install_auth_gate(app, gate)` -- Attach the gate to a Flask app and a module-level slot.
- `AuthGate.auto_generated_token` (method) `estorides_core/web_security.py:444` `def auto_generated_token()` -- Return the auto-generated token (None if user set ESTORIDES_AUTH_TOKEN manually).

## estorides_export/encryption.py
Depends on: `estorides_core/knowledge_graph.py`, `estorides_export/__init__.py`
Imported by: `estorides_export/__init__.py`, `estorides_web.py`, `tests/test_encrypted_export.py`
- `encrypt_file` (function) `estorides_export/encryption.py:51` `def encrypt_file(plaintext_path, recipient_pubkey)` -- Encrypt `plaintext_path` to `<plaintext_path>.age` for the recipient.
- `export_stix_encrypted` (function) `estorides_export/encryption.py:100` `def export_stix_encrypted(kg, recipient_pubkey, path)` -- Build the STIX bundle, write to disk, encrypt to <path>.age.
- `export_misp_encrypted` (function) `estorides_export/encryption.py:128` `def export_misp_encrypted(kg, recipient_pubkey, path)`

## estorides_export/misp.py
Depends on: `estorides_core/config.py`, `estorides_core/knowledge_graph.py`
Imported by: `estorides_export/__init__.py`
- `event_from_graph` (function) `estorides_export/misp.py:36` `def event_from_graph(kg)`
- `export` (function) `estorides_export/misp.py:79` `def export(kg, path)`

## estorides_export/recon_report.py
Imported by: `estorides_export/__init__.py`, `tests/test_recon_report.py`
- `ReportMetadata.to_dict` (method) `estorides_export/recon_report.py:35` `def to_dict(self)`
- `ReportSection.to_dict` (method) `estorides_export/recon_report.py:46` `def to_dict(self)`
- `ReportResult.to_dict` (method) `estorides_export/recon_report.py:57` `def to_dict(self)`
- `ReportResult.redact_sensitive` (method) `estorides_export/recon_report.py:61` `def redact_sensitive(text)`
- `ReportResult.build_subdomain_tree` (method) `estorides_export/recon_report.py:67` `def build_subdomain_tree(subdomains)`
- `ReportResult.build_executive_summary` (method) `estorides_export/recon_report.py:92` `def build_executive_summary(critical_findings, total_targets, domain, classification)`
- `ReportResult.generate_report` (method) `estorides_export/recon_report.py:115` `def generate_report(query, target_scoring, metadata)`

## estorides_export/report.py
Imported by: `estorides_cli.py`, `estorides_export/__init__.py`, `static/js/estorides.js`, `tests/test_hardening.py`
- `render_markdown_report` (function) `estorides_export/report.py:196` `def render_markdown_report(case, entities, sources_queried, sources_succeeded, diff)` -- Build a Markdown report for `case`.

## estorides_export/stix.py
Depends on: `estorides_core/config.py`, `estorides_core/knowledge_graph.py`
Imported by: `estorides_export/__init__.py`
- `bundle_from_graph` (function) `estorides_export/stix.py:55` `def bundle_from_graph(kg)`
- `export` (function) `estorides_export/stix.py:145` `def export(kg, path)`

## estorides_llm/intelligence_prompts.py
Imported by: `estorides_llm/manager.py`
- `format_context` (function) `estorides_llm/intelligence_prompts.py:97` `def format_context(sources)` -- Render a list of observation dicts into a context block for the LLM.

## estorides_llm/manager.py
Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
Imported by: `estorides_llm/__init__.py`
- `LLMBackend.__call__` (method) `estorides_llm/manager.py:69` `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)` -- Return (content, model_id).
- `LLMBackend.stream_generate` (method) `estorides_llm/manager.py:80` `def stream_generate(self, prompt, context, model, temperature, request_timeout)` -- Optional: stream (kind, text) chunks.
- `LLMBackend.register` (method) `estorides_llm/manager.py:97` `def register(name)` -- Decorator: register a backend under `name`.
- `LLMBackend.deco` (method) `estorides_llm/manager.py:105` `def deco(backend_or_cls)`
- `OllamaBackend.get_status` (method) `estorides_llm/manager.py:124` `def get_status()` -- Return available ollama models and reachability status.
- `OllamaBackend.stream_generate` (method) `estorides_llm/manager.py:188` `def stream_generate(self, prompt, context, model, temperature, request_timeout)` -- Stream an ollama response as (kind, text) chunks.
- `OllamaBackend.__call__` (method) `estorides_llm/manager.py:227` `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- `_OpenAICompatibleBackend.__call__` (method) `estorides_llm/manager.py:274` `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- `AnthropicBackend.__call__` (method) `estorides_llm/manager.py:319` `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- `LLMManager.__init__` (method) `estorides_llm/manager.py:357` `def __init__(self)`
- `LLMManager.generate` (method) `estorides_llm/manager.py:373` `def generate(self, prompt)` -- Try each backend in priority order; return the first that succeeds.
- `LLMManager.get_ollama_status` (method) `estorides_llm/manager.py:414` `def get_ollama_status(self)` -- Return ollama reachability and available models.
- `LLMManager.stream` (method) `estorides_llm/manager.py:422` `def stream(self, prompt)` -- Stream an analysis from a specific ollama model.

## estorides_web.py
Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_force.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/openapi.py`, `estorides_core/ops_observability.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`, `estorides_web_tools.py`
Imported by: `estorides_cli.py`, `estorides_web_tools.py`, `tests/test_openapi.py`, `tests/test_web_helpers.py`, `tests/test_web_tools_blueprint.py`, `tools/sync_docs.py`, `wsgi.py`
- `deco` (method) `estorides_web.py:88` `def deco(view)`
- `wrapper` (method) `estorides_web.py:90` `def wrapper()`
- `_RunStreamJob.__init__` (method) `estorides_web.py:155` `def __init__(self, job_id, query, query_type, case_id)`
- `_RunStreamJob.stop` (method) `estorides_web.py:164` `def stop(self)`
- `_RunStreamJob.should_stop` (method) `estorides_web.py:167` `def should_stop(self)`
- `_RunStreamJob.status` (method) `estorides_web.py:171` `def status(self)`
- `_RunStreamJob.done` (method) `estorides_web.py:175` `def done(self)`
- `_RunStreamJob.deco` (method) `estorides_web.py:197` `def deco(view)`
- `_RunStreamJob.wrapper` (method) `estorides_web.py:199` `def wrapper()`
- `_RunStreamJob.create_app` (method) `estorides_web.py:234` `def create_app()`
- `_RunStreamJob.healthz` (method) `estorides_web.py:270` `def healthz()` -- Return liveness without auth for container probes.
- `_RunStreamJob.readyz` (method) `estorides_web.py:281` `def readyz()` -- Return readiness based on source registry state.
- `_RunStreamJob.metrics` (method) `estorides_web.py:295` `def metrics()` -- Return Prometheus text counters for this process.
- `_RunStreamJob.openapi_doc` (method) `estorides_web.py:302` `def openapi_doc()` -- Return the generated OpenAPI document for this app.
- `_RunStreamJob.index` (method) `estorides_web.py:307` `def index()`
- `_RunStreamJob.api_status` (method) `estorides_web.py:328` `def api_status()`
- `_RunStreamJob.api_ollama_status` (method) `estorides_web.py:334` `def api_ollama_status()`
- `_RunStreamJob.api_run` (method) `estorides_web.py:340` `def api_run()`
- `_RunStreamJob.api_graph` (method) `estorides_web.py:396` `def api_graph()`
- `_RunStreamJob.api_feeds` (method) `estorides_web.py:485` `def api_feeds()` -- Return real-time feed points (quakes, fires, news) for the map.
- `_RunStreamJob.api_export` (method) `estorides_web.py:516` `def api_export(fmt)`
- `_RunStreamJob.api_cases_list` (method) `estorides_web.py:594` `def api_cases_list()`
- `_RunStreamJob.api_cases_get` (method) `estorides_web.py:607` `def api_cases_get(case_id)`
- `_RunStreamJob.api_cases_delete` (method) `estorides_web.py:621` `def api_cases_delete(case_id)`
- `_RunStreamJob.api_cases_save` (method) `estorides_web.py:629` `def api_cases_save(case_id)` -- Bookmark a case from the UI.
- `_RunStreamJob.api_cases_diff` (method) `estorides_web.py:652` `def api_cases_diff()` -- Symmetric diff between two cases by entity (type, value).
- `_RunStreamJob.api_intel_resolve` (method) `estorides_web.py:677` `def api_intel_resolve()` -- Cross-feed entity resolution (Osiris-style /resolve).
- `_RunStreamJob.api_intel_graph` (method) `estorides_web.py:716` `def api_intel_graph()` -- Cypher query against the Kùzu persistent graph.
- `_RunStreamJob.api_intel_stats` (method) `estorides_web.py:755` `def api_intel_stats()` -- Stats for both the case store and the Kùzu graph.
- `_RunStreamJob.api_fusion_stats` (method) `estorides_web.py:776` `def api_fusion_stats()` -- One-glance dashboard of the fused, cross-run fact base.
- `_RunStreamJob.api_fusion_sources` (method) `estorides_web.py:784` `def api_fusion_sources()` -- The YAML source catalogue with accumulated fetch/ok counters.
- `_RunStreamJob.api_fusion_entities` (method) `estorides_web.py:793` `def api_fusion_entities()` -- Search fused entities.
- `_RunStreamJob.api_fusion_entity` (method) `estorides_web.py:814` `def api_fusion_entity(eid)` -- Full fused view of one entity: provenance, properties, edges.
- `_RunStreamJob.api_fusion_analytics_entity_timeline` (method) `estorides_web.py:832` `def api_fusion_analytics_entity_timeline(eid)`
- `_RunStreamJob.api_fusion_analytics_entity_summary` (method) `estorides_web.py:842` `def api_fusion_analytics_entity_summary(eid)`
- `_RunStreamJob.api_fusion_analytics_source_stats` (method) `estorides_web.py:852` `def api_fusion_analytics_source_stats(source_name)`
- `_RunStreamJob.api_fusion_analytics_consensus` (method) `estorides_web.py:862` `def api_fusion_analytics_consensus(eid)`
- `_RunStreamJob.api_fusion_analytics_top_changed` (method) `estorides_web.py:872` `def api_fusion_analytics_top_changed()`
- `_RunStreamJob.admin_sources` (method) `estorides_web.py:882` `def admin_sources()` -- Render the YAML source manager page.
- `_RunStreamJob.api_sources_yaml_list` (method) `estorides_web.py:899` `def api_sources_yaml_list()` -- Return every YAML source with full configuration.
- `_RunStreamJob.api_sources_yaml_create` (method) `estorides_web.py:925` `def api_sources_yaml_create()` -- Create a new YAML source.
- `_RunStreamJob.api_sources_yaml_update` (method) `estorides_web.py:946` `def api_sources_yaml_update(name)` -- Update/replace a YAML source.
- `_RunStreamJob.api_sources_yaml_delete` (method) `estorides_web.py:965` `def api_sources_yaml_delete(name)` -- Delete a YAML source.
- `_RunStreamJob.api_fusion_analytics_corroboration_matrix` (method) `estorides_web.py:982` `def api_fusion_analytics_corroboration_matrix()`
- `_RunStreamJob.api_socmint_resolve` (method) `estorides_web.py:996` `def api_socmint_resolve()` -- Resolve a username across known social media platforms.
- `_RunStreamJob.api_socmint_platforms` (method) `estorides_web.py:1018` `def api_socmint_platforms()` -- Return the list of all known social media platforms.
- `_RunStreamJob.api_socmint_discover` (method) `estorides_web.py:1026` `def api_socmint_discover()` -- Extract social media profile URLs from a text blob.
- `_RunStreamJob.api_watch_list` (method) `estorides_web.py:1069` `def api_watch_list()` -- List all watch targets.
- `_RunStreamJob.api_watch_create` (method) `estorides_web.py:1078` `def api_watch_create()` -- Create a new watch target.
- `_RunStreamJob.api_watch_get` (method) `estorides_web.py:1112` `def api_watch_get(watch_id)`
- `_RunStreamJob.api_watch_delete` (method) `estorides_web.py:1124` `def api_watch_delete(watch_id)`
- `_RunStreamJob.api_watch_enable` (method) `estorides_web.py:1135` `def api_watch_enable(watch_id)`
- `_RunStreamJob.api_watch_disable` (method) `estorides_web.py:1148` `def api_watch_disable(watch_id)`
- `_RunStreamJob.api_watch_history` (method) `estorides_web.py:1160` `def api_watch_history(watch_id)`
- `_RunStreamJob.api_alerts_channels` (method) `estorides_web.py:1170` `def api_alerts_channels()` -- List configured alert channels and their status.
- `_RunStreamJob.api_alerts_test` (method) `estorides_web.py:1178` `def api_alerts_test()` -- Send a test alert to a channel.
- `_RunStreamJob.api_scheduler_status` (method) `estorides_web.py:1194` `def api_scheduler_status()`
- `_RunStreamJob.api_transforms` (method) `estorides_web.py:1212` `def api_transforms()` -- List the transforms applicable to an entity type.
- `_RunStreamJob.api_transform_run` (method) `estorides_web.py:1226` `def api_transform_run()` -- Run one transform and return nodes/links for graph merge.
- `_RunStreamJob.api_transform_stream` (method) `estorides_web.py:1248` `def api_transform_stream()` -- Stream one transform as SSE `node`/`link` events plus `done`.
- `_RunStreamJob.api_osiris_bgp` (method) `estorides_web.py:1287` `def api_osiris_bgp()`
- `_RunStreamJob.api_osiris_mac` (method) `estorides_web.py:1301` `def api_osiris_mac()`
- `_RunStreamJob.api_osiris_phone` (method) `estorides_web.py:1315` `def api_osiris_phone()`
- `_RunStreamJob.api_osiris_github` (method) `estorides_web.py:1329` `def api_osiris_github()`
- `_RunStreamJob.api_osiris_leaks` (method) `estorides_web.py:1343` `def api_osiris_leaks()`
- `_RunStreamJob.api_osiris_kev` (method) `estorides_web.py:1357` `def api_osiris_kev()`
- `_RunStreamJob.api_osiris_malware` (method) `estorides_web.py:1366` `def api_osiris_malware()`
- `_RunStreamJob.api_osiris_threats` (method) `estorides_web.py:1371` `def api_osiris_threats()`
- `_RunStreamJob.api_discover_start` (method) `estorides_web.py:1384` `def api_discover_start()`
- `_RunStreamJob.api_discover_jobs` (method) `estorides_web.py:1430` `def api_discover_jobs()`
- `_RunStreamJob.api_discover_stop` (method) `estorides_web.py:1436` `def api_discover_stop()`
- `_RunStreamJob.api_discover_stream` (method) `estorides_web.py:1448` `def api_discover_stream()` -- Server-Sent Events for a discoverer job.
- `_RunStreamJob.gen` (method) `estorides_web.py:1461` `def gen()`
- `_RunStreamJob.api_run_stream_start` (method) `estorides_web.py:1498` `def api_run_stream_start()`
- `_RunStreamJob.api_run_stream_stop` (method) `estorides_web.py:1565` `def api_run_stream_stop()`
- `_RunStreamJob.api_run_stream` (method) `estorides_web.py:1577` `def api_run_stream()`
- `_RunStreamJob.gen` (method) `estorides_web.py:1583` `def gen()`
- `_RunStreamJob.api_analyze_stream` (method) `estorides_web.py:1624` `def api_analyze_stream()`
- `_RunStreamJob.gen` (method) `estorides_web.py:1653` `def gen()`

## estorides_web_tools.py
Depends on: `estorides_core/audit.py`, `estorides_core/tool_install.py`, `estorides_core/web_security.py`, `estorides_web.py`
Imported by: `estorides_web.py`
- `api_tools_list` (function) `estorides_web_tools.py:49` `def api_tools_list()`
- `api_tools_doctor` (function) `estorides_web_tools.py:68` `def api_tools_doctor()`
- `api_tool_install` (function) `estorides_web_tools.py:75` `def api_tool_install(name)`
- `api_tool_install_status` (function) `estorides_web_tools.py:120` `def api_tool_install_status(name)`

## install.sh
- `install_full` (function) `install.sh:51` -- 3) Two install passes: full first, minimal fallback.
- `install_minimal` (function) `install.sh:55`


Next: [API_p3.md](API_p3.md)
