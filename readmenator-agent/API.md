# API (page 1 of 3)
Pages: [API.md](API.md), [API_p2.md](API_p2.md), [API_p3.md](API_p3.md)

## estorides_cli.py
Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`
Imported by: `tests/test_cli_watch.py`
- `cmd_discover` (function) `estorides_cli.py:93` `def cmd_discover(args)` -- v1.2 — fanout the surface from a seed.
- `cmd_run` (function) `estorides_cli.py:205` `def cmd_run(args)`
- `cmd_scope` (function) `estorides_cli.py:282` `def cmd_scope(args)` -- Classify discovered assets against a program's scope rules.
- `cmd_graph_export` (function) `estorides_cli.py:328` `def cmd_graph_export(args)`
- `cmd_export_stix` (function) `estorides_cli.py:357` `def cmd_export_stix(args)`
- `cmd_export_misp` (function) `estorides_cli.py:367` `def cmd_export_misp(args)`
- `cmd_report` (function) `estorides_cli.py:377` `def cmd_report(args)` -- Render a Markdown report for a case.
- `cmd_diff` (function) `estorides_cli.py:418` `def cmd_diff(args)` -- Diff two cases.
- `cmd_status` (function) `estorides_cli.py:446` `def cmd_status(_)`
- `cmd_fusion` (function) `estorides_cli.py:453` `def cmd_fusion(args)` -- Query the cross-run fusion datastore.
- `cmd_watch_add` (function) `estorides_cli.py:496` `def cmd_watch_add(args)` -- Add a new recurring watch target.
- `cmd_watch_list` (function) `estorides_cli.py:560` `def cmd_watch_list(args)` -- List all watch targets.
- `cmd_watch_remove` (function) `estorides_cli.py:580` `def cmd_watch_remove(args)` -- Delete a watch target.
- `cmd_watch_enable` (function) `estorides_cli.py:592` `def cmd_watch_enable(args)`
- `cmd_watch_disable` (function) `estorides_cli.py:605` `def cmd_watch_disable(args)`
- `cmd_watch_history` (function) `estorides_cli.py:617` `def cmd_watch_history(args)`
- `cmd_alerts_test` (function) `estorides_cli.py:638` `def cmd_alerts_test(args)`
- `cmd_alerts_channels` (function) `estorides_cli.py:650` `def cmd_alerts_channels(args)`
- `cmd_scheduler_start` (function) `estorides_cli.py:662` `def cmd_scheduler_start(args)`
- `cmd_scheduler_stop` (function) `estorides_cli.py:672` `def cmd_scheduler_stop(args)`
- `cmd_scheduler_status` (function) `estorides_cli.py:682` `def cmd_scheduler_status(args)`
- `cmd_serve` (function) `estorides_cli.py:690` `def cmd_serve(args)`
- `build_parser` (function) `estorides_cli.py:707` `def build_parser()`
- `main` (function) `estorides_cli.py:863` `def main(argv)`

## estorides_core/active_recon.py
Depends on: `estorides_core/tool_runner.py`
Imported by: `tests/test_active_recon.py`
- `NmapResult.to_dict` (method) `estorides_core/active_recon.py:24` `def to_dict(self)`
- `NmapResult.to_entities` (method) `estorides_core/active_recon.py:27` `def to_entities(self)`
- `NiktoResult.to_dict` (method) `estorides_core/active_recon.py:41` `def to_dict(self)`
- `NiktoResult.to_entities` (method) `estorides_core/active_recon.py:44` `def to_entities(self)`
- `SqlmapResult.to_dict` (method) `estorides_core/active_recon.py:58` `def to_dict(self)`
- `SqlmapResult.to_entities` (method) `estorides_core/active_recon.py:61` `def to_entities(self)`
- `DnsreconResult.to_dict` (method) `estorides_core/active_recon.py:77` `def to_dict(self)`
- `DnsreconResult.to_entities` (method) `estorides_core/active_recon.py:80` `def to_entities(self)`
- `TheHarvesterResult.to_dict` (method) `estorides_core/active_recon.py:95` `def to_dict(self)`
- `TheHarvesterResult.to_entities` (method) `estorides_core/active_recon.py:98` `def to_entities(self)`
- `run_nmap` (function) `estorides_core/active_recon.py:213` `def run_nmap(target, args)`
- `run_nikto` (function) `estorides_core/active_recon.py:243` `def run_nikto(target, args)`
- `run_sqlmap` (function) `estorides_core/active_recon.py:269` `def run_sqlmap(target, args)`
- `run_dnsrecon` (function) `estorides_core/active_recon.py:295` `def run_dnsrecon(target, args)`
- `run_theHarvester` (function) `estorides_core/active_recon.py:325` `def run_theHarvester(target, args)`

## estorides_core/alerter.py
Depends on: `estorides_core/ssrf_guard.py`
Imported by: `estorides_cli.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_security_remediation.py`
- `_NoRedirectHandler.redirect_request` (method) `estorides_core/alerter.py:64` `def redirect_request(self, req, fp, code, msg, headers, newurl)`
- `AlertDispatcher.send` (method) `estorides_core/alerter.py:201` `def send(self, channel, title, body, severity)` -- Send an alert to a single channel.
- `AlertDispatcher.send_watch_alert` (method) `estorides_core/alerter.py:260` `def send_watch_alert(self, watch, entity_count, obs_count, new_entities)` -- Send alerts for a completed watch run to all configured channels.
- `AlertDispatcher.test` (method) `estorides_core/alerter.py:280` `def test(self, channel)` -- Send a test alert to verify channel configuration.
- `AlertDispatcher.available_channels` (method) `estorides_core/alerter.py:290` `def available_channels(self)` -- Return list of configured channels with their status.

## estorides_core/async_client.py
Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
Imported by: `estorides_core/orchestrator.py`, `tests/test_async_client.py`
- `CircuitBreaker.allow` (method) `estorides_core/async_client.py:69` `def allow(self, host)`
- `CircuitBreaker.record_success` (method) `estorides_core/async_client.py:75` `def record_success(self, host)`
- `CircuitBreaker.record_failure` (method) `estorides_core/async_client.py:79` `def record_failure(self, host)`
- `ResponseCache.__init__` (method) `estorides_core/async_client.py:95` `def __init__(self, path)`
- `ResponseCache.get` (method) `estorides_core/async_client.py:145` `def get(self, method, url, body)`
- `ResponseCache.set` (method) `estorides_core/async_client.py:161` `def set(self, method, url, body, value)`
- `AsyncClient.__init__` (method) `estorides_core/async_client.py:175` `def __init__(self)`
- `AsyncClient.session` (method) `estorides_core/async_client.py:264` `def session(self)`
- `AsyncClient.fetch` (method) `estorides_core/async_client.py:270` `def fetch(self, method, url)` -- Fetch a URL.
- `sync_fetch` (function) `estorides_core/async_client.py:400` `def sync_fetch(method, url)`

## estorides_core/audit.py
Depends on: `estorides_core/config.py`
Imported by: `estorides_web.py`, `estorides_web_tools.py`, `tests/test_audit_log.py`
- `AuditEvent.to_jsonl` (method) `estorides_core/audit.py:68` `def to_jsonl(self)`
- `AuditLog.__init__` (method) `estorides_core/audit.py:90` `def __init__(self, path)`
- `AuditLog.record` (method) `estorides_core/audit.py:104` `def record(self, event)`
- `AuditLog.query` (method) `estorides_core/audit.py:150` `def query(self, event)`
- `RateLimiter.__init__` (method) `estorides_core/audit.py:201` `def __init__(self)`
- `RateLimiter.allow` (method) `estorides_core/audit.py:214` `def allow(self, key)` -- Return (allowed, retry_after_seconds).
- `RateLimiter.reset` (method) `estorides_core/audit.py:238` `def reset(self, key)`

## estorides_core/case_crypto.py
Imported by: `estorides_core/cases.py`, `tests/test_case_crypto.py`
- `crypto_status` (function) `estorides_core/case_crypto.py:36` `def crypto_status()` -- Report whether field encryption is active and why.
- `encrypt_text` (function) `estorides_core/case_crypto.py:50` `def encrypt_text(plain)` -- Encrypt plain text when enabled else return it unchanged.
- `decrypt_text` (function) `estorides_core/case_crypto.py:65` `def decrypt_text(token)` -- Decrypt a token, passing through plaintext and errors safely.

## estorides_core/cases.py
Depends on: `estorides_core/case_crypto.py`, `estorides_core/config.py`, `estorides_core/sqlite_store.py`
Imported by: `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_case_crypto.py`, `tests/test_hardening.py`, `tests/test_obs_fts.py`
- `CaseStore.fts_available` (method) `estorides_core/cases.py:147` `def fts_available(self)` -- True when the FTS5 index exists and answers queries.
- `CaseStore.search_observations_fts` (method) `estorides_core/cases.py:151` `def search_observations_fts(self, query, limit)` -- Full text search over observations ordered by rank.
- `CaseStore.create_case` (method) `estorides_core/cases.py:173` `def create_case(self, query, query_type, notes)` -- Open a new case and return its id (8-char slug).
- `CaseStore.add_observation` (method) `estorides_core/cases.py:189` `def add_observation(self, case_id, observation)` -- Persist a single observation row.
- `CaseStore.add_entities` (method) `estorides_core/cases.py:223` `def add_entities(self, case_id, entities)` -- Persist the merged entity list.
- `CaseStore.finalise` (method) `estorides_core/cases.py:246` `def finalise(self, case_id, analysis, kg_path, mitre, source_count, obs_count, entity_count, status)`
- `CaseStore.delete_case` (method) `estorides_core/cases.py:276` `def delete_case(self, case_id)`
- `CaseStore.set_notes` (method) `estorides_core/cases.py:280` `def set_notes(self, case_id, notes)` -- Overwrite the free-text `notes` column for a case.
- `CaseStore.get_case` (method) `estorides_core/cases.py:291` `def get_case(self, case_id)`
- `CaseStore.list_observations` (method) `estorides_core/cases.py:304` `def list_observations(self, case_id)`
- `CaseStore.list_entities` (method) `estorides_core/cases.py:327` `def list_entities(self, case_id)`
- `CaseStore.diff_entities` (method) `estorides_core/cases.py:342` `def diff_entities(self, case_a, case_b)` -- Compare two cases by entity (type, value) keys.
- `CaseStore.search_cases` (method) `estorides_core/cases.py:389` `def search_cases(self, query_substring, limit, query_type)` -- Lightweight case search.
- `CaseStore.search_by_entity` (method) `estorides_core/cases.py:419` `def search_by_entity(self, ent_type, value, limit)` -- Find every case that observed a given entity.
- `CaseStore.stats` (method) `estorides_core/cases.py:447` `def stats(self)`

## estorides_core/change_detection.py
Depends on: `estorides_core/ids.py`, `estorides_core/reliability_scoring.py`
Imported by: `tests/properties/test_change_detection_properties.py`, `tests/test_change_detection.py`
- `detect_changes` (function) `estorides_core/change_detection.py:284` `def detect_changes(snapshot_before, snapshot_after)` -- Diff two snapshots.

## estorides_core/cloud_asset_discovery.py
Imported by: `estorides_core/recon_pipeline.py`, `tests/test_cloud_asset_discovery.py`
- `CloudAsset.to_dict` (method) `estorides_core/cloud_asset_discovery.py:45` `def to_dict(self)`
- `CloudAssetDiscoveryResult.to_dict` (method) `estorides_core/cloud_asset_discovery.py:56` `def to_dict(self)`
- `generate_bucket_names` (function) `estorides_core/cloud_asset_discovery.py:65` `def generate_bucket_names(domain)`
- `assess_bucket` (function) `estorides_core/cloud_asset_discovery.py:84` `def assess_bucket(url, method)`

## estorides_core/code_exposure.py
Imported by: `estorides_core/recon_pipeline.py`, `tests/test_code_exposure.py`
- `CodeFinding.to_dict` (method) `estorides_core/code_exposure.py:57` `def to_dict(self)`
- `SeveritySummary.to_dict` (method) `estorides_core/code_exposure.py:69` `def to_dict(self)`
- `CodeExposureResult.to_dict` (method) `estorides_core/code_exposure.py:81` `def to_dict(self)`
- `validate_aws_key` (function) `estorides_core/code_exposure.py:91` `def validate_aws_key(key)`
- `classify_finding` (function) `estorides_core/code_exposure.py:99` `def classify_finding(content, source, file_path)`
- `analyse_findings` (function) `estorides_core/code_exposure.py:189` `def analyse_findings(findings, rate_limited)`

## estorides_core/config.py
Imported by: `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/ops_observability.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_async_client.py`, `tests/test_config_env.py`, `tests/test_monitoring.py`, `tests/test_opsec_contact.py`, `tests/test_recon_fusion.py`, `tests/test_retry_policy.py`, `tests/test_socmint.py`, `tests/test_structured_extraction.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`
- `ensure_data_dirs` (function) `estorides_core/config.py:58` `def ensure_data_dirs()` -- Idempotently create DATA_DIR.
- `ensure_reports_dir` (function) `estorides_core/config.py:69` `def ensure_reports_dir()` -- Idempotently create REPORTS_DIR.
- `contact_level` (function) `estorides_core/config.py:206` `def contact_level(contact)` -- Map a contact class to its numeric severity, unknown values to active.
- `effective_proxies` (function) `estorides_core/config.py:232` `def effective_proxies(explicit)` -- Resolve the proxy rotation pool from an explicit value or the env.
- `CacheConfig.is_active` (method) `estorides_core/config.py:373` `def is_active(self)` -- Cache is only consulted when enabled and the TTL is positive.
- `PivotPolicyConfig.is_pivotable` (method) `estorides_core/config.py:393` `def is_pivotable(self, entity_type)` -- True when an entity of `entity_type` should be re-queried.
- `PivotPolicyConfig.lead_score` (method) `estorides_core/config.py:397` `def lead_score(self, entity_type, depth, parent_score)` -- Priority of expanding this lead.
- `PivotConfig.clamp_depth` (method) `estorides_core/config.py:427` `def clamp_depth(self, value)` -- Clamp a requested depth into [1, max_depth_cap].
- `PivotConfig.clamp_steps` (method) `estorides_core/config.py:431` `def clamp_steps(self, value)` -- Clamp a requested step budget into [1, max_steps_cap].
- `PivotConfig.clamp_entities` (method) `estorides_core/config.py:435` `def clamp_entities(self, value)` -- Clamp a requested entity budget into [1, max_entities_cap].
- `PivotConfig.clamp_parallel` (method) `estorides_core/config.py:439` `def clamp_parallel(self, value)` -- Clamp a requested fan-out width into [1, parallel_cap].
- `PivotConfig.clamp_deadline` (method) `estorides_core/config.py:443` `def clamp_deadline(self, value)` -- Clamp a requested per-target deadline into (0, deadline_cap_seconds].
- `RetryConfig.delay` (method) `estorides_core/config.py:543` `def delay(self, attempt)` -- Exponential backoff for 1-indexed attempt, clamped to cap.
- `retry_delay` (function) `estorides_core/config.py:672` `def retry_delay(attempt)` -- Return the backoff sleep for a 1-indexed attempt.

## estorides_core/discoverer.py
Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
Imported by: `estorides_cli.py`, `estorides_web.py`, `static/js/estorides.js`
- `DiscoverJob.stop` (method) `estorides_core/discoverer.py:78` `def stop(self)`
- `DiscoverJob.should_stop` (method) `estorides_core/discoverer.py:81` `def should_stop(self)`
- `DiscoverJob.push_event` (method) `estorides_core/discoverer.py:84` `def push_event(self, ev)` -- Append an event and keep the buffer bounded.
- `_DiscoverJobSink.__init__` (method) `estorides_core/discoverer.py:103` `def __init__(self, job)`
- `_DiscoverJobSink.emit` (method) `estorides_core/discoverer.py:106` `def emit(self, event)`
- `create_discover_job` (function) `estorides_core/discoverer.py:194` `def create_discover_job(seed_type, seed_value)` -- Create and register a discovery job synchronously.
- `start_discover` (function) `estorides_core/discoverer.py:252` `def start_discover(seed_type, seed_value)` -- Create a discovery job and schedule its worker on the current loop.
- `start_discover_threadsafe` (function) `estorides_core/discoverer.py:285` `def start_discover_threadsafe(loop, seed_type, seed_value)` -- Create the job in the calling thread, fire its worker on `loop`.
- `list_jobs` (function) `estorides_core/discoverer.py:349` `def list_jobs(limit)` -- Snapshot of the recent jobs for the /api/discover/jobs endpoint.

## estorides_core/entity_extraction.py
Depends on: `estorides_core/config.py`
Imported by: `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_extraction.py`, `tests/test_entity_resolution.py`, `tests/test_query_intent.py`, `tests/test_socmint.py`, `tests/test_structured_extraction.py`
- `Entity.to_dict` (method) `estorides_core/entity_extraction.py:34` `def to_dict(self)`
- `normalize_query` (function) `estorides_core/entity_extraction.py:57` `def normalize_query(query)` -- Return the routing form of raw operator input.
- `detect_query_type` (function) `estorides_core/entity_extraction.py:100` `def detect_query_type(query)` -- Return the detected type of a free-form query.
- `extract_from_text` (function) `estorides_core/entity_extraction.py:146` `def extract_from_text(text, source)` -- Find every recognised entity in a raw text blob.
- `extract_from_json` (function) `estorides_core/entity_extraction.py:210` `def extract_from_json(payload, source)` -- Pull entities out of a JSON-like structure.
- `extract_structured` (function) `estorides_core/entity_extraction.py:330` `def extract_structured(payload, source)` -- Extract human selectors (email, username, person, org, phone) by key.
- `visit` (function) `estorides_core/entity_extraction.py:344` `def visit(node, key)`
- `merge` (function) `estorides_core/entity_extraction.py:382` `def merge()` -- Deduplicate by (type, value) and merge sources / contexts.
- `find` (function) `estorides_core/entity_extraction.py:499` `def find(x, parent)`
- `union` (function) `estorides_core/entity_extraction.py:505` `def union(a, b, parent)`
- `norm` (function) `estorides_core/entity_extraction.py:510` `def norm(v)`

## estorides_core/entity_resolution.py
Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/ids.py`, `estorides_core/transliteration.py`
Imported by: `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`
- `jaro` (function) `estorides_core/entity_resolution.py:83` `def jaro(s1, s2)` -- Return the Jaro similarity of two strings in ``[0, 1]``.
- `jaro_winkler` (function) `estorides_core/entity_resolution.py:126` `def jaro_winkler(s1, s2, prefix_weight)` -- Jaro-Winkler similarity: Jaro with a shared-prefix bonus.
- `normalize_value` (function) `estorides_core/entity_resolution.py:206` `def normalize_value(etype, value)` -- Return the canonical normalised form of an entity value.
- `canonical_id` (function) `estorides_core/entity_resolution.py:246` `def canonical_id(etype, normalized)` -- Stable, content-addressed id for a normalised entity.
- `blocking_keys` (function) `estorides_core/entity_resolution.py:257` `def blocking_keys(etype, normalized, value)` -- Return the blocking keys that bucket an entity for comparison.
- `score_pair` (function) `estorides_core/entity_resolution.py:302` `def score_pair(etype, a_value, b_value, a_norm, b_norm)` -- Score how likely two same-type entities denote the same object.
- `CanonicalEntity.to_dict` (method) `estorides_core/entity_resolution.py:357` `def to_dict(self)`
- `CanonicalEntity.to_entity` (method) `estorides_core/entity_resolution.py:373` `def to_entity(self)` -- Project back onto the legacy :class:`Entity` shape.
- `SameAsLink.to_dict` (method) `estorides_core/entity_resolution.py:409` `def to_dict(self)`
- `ResolutionResult.to_dict` (method) `estorides_core/entity_resolution.py:425` `def to_dict(self)`
- `_UnionFind.__init__` (method) `estorides_core/entity_resolution.py:435` `def __init__(self, n)`
- `_UnionFind.find` (method) `estorides_core/entity_resolution.py:438` `def find(self, x)`
- `_UnionFind.union` (method) `estorides_core/entity_resolution.py:444` `def union(self, a, b)`
- `EntityResolver.__init__` (method) `estorides_core/entity_resolution.py:469` `def __init__(self)`
- `EntityResolver.resolve` (method) `estorides_core/entity_resolution.py:482` `def resolve(self, entities)` -- Resolve ``entities`` into canonical identities and links.
- `rank` (function) `estorides_core/entity_resolution.py:670` `def rank(rec)`
- `resolve_entities` (function) `estorides_core/entity_resolution.py:727` `def resolve_entities(entities)` -- Module-level convenience wrapper around :class:`EntityResolver`.

## estorides_core/entity_store.py
Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/sqlite_store.py`
Imported by: `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`
- `EntityStore.lookup` (method) `estorides_core/entity_store.py:66` `def lookup(self, etype, normalized, aliases)` -- Return an existing canonical id for any known form, or None.
- `EntityStore.upsert` (method) `estorides_core/entity_store.py:104` `def upsert(self, entity)` -- Persist (insert or update) a canonical entity and its aliases.
- `EntityStore.stats` (method) `estorides_core/entity_store.py:143` `def stats(self)` -- Return a one-glance summary of store size.
- `open_store` (function) `estorides_core/entity_store.py:155` `def open_store(path)` -- Open the store, returning None instead of raising on failure.

## estorides_core/event_bus.py
Imported by: `estorides_core/orchestrator.py`, `tests/test_event_bus.py`
- `EventBus.__init__` (method) `estorides_core/event_bus.py:27` `def __init__(self)` -- Create an empty bus with no subscribers.
- `EventBus.subscribe` (method) `estorides_core/event_bus.py:31` `def subscribe(self, event, handler)` -- Register handler for event and return it for unsubscription.
- `EventBus.unsubscribe` (method) `estorides_core/event_bus.py:41` `def unsubscribe(self, event, handler)` -- Remove handler from event and report whether it was present.
- `EventBus.publish` (method) `estorides_core/event_bus.py:50` `def publish(self, event, payload)` -- Deliver a copy of payload to each subscriber and count attempts.
- `EventBus.clear` (method) `estorides_core/event_bus.py:63` `def clear(self, event)` -- Remove subscribers for one event or for the whole bus.
- `EventBus.subscriber_count` (method) `estorides_core/event_bus.py:71` `def subscriber_count(self, event)` -- Return the number of handlers registered for event.
- `get_bus` (function) `estorides_core/event_bus.py:85` `def get_bus()` -- Return the process wide shared bus instance.

## estorides_core/feeds.py
Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
Imported by: `estorides_web.py`
- `FeedPoint.to_dict` (method) `estorides_core/feeds.py:69` `def to_dict(self)`
- `Feed.__init__` (method) `estorides_core/feeds.py:82` `def __init__(self)`
- `Feed.fetch` (method) `estorides_core/feeds.py:90` `def fetch(self)` -- Public entrypoint.
- `Feed.point` (method) `estorides_core/feeds.py:135` `def point(self, record)` -- Default: return (lat, lon) if both present.
- `list_feeds` (function) `estorides_core/feeds.py:313` `def list_feeds()` -- Return public feed descriptions for the /api/feeds endpoint.
- `get_feed` (function) `estorides_core/feeds.py:321` `def get_feed(name)`
- `fetch_all` (function) `estorides_core/feeds.py:325` `def fetch_all(bbox, use_cache)` -- Fetch every registered feed (optionally clipped to a bbox).

## estorides_core/fusion_analytics.py
Imported by: `estorides_web.py`, `tests/test_fusion_analytics.py`
- `FusionAnalytics.__init__` (method) `estorides_core/fusion_analytics.py:40` `def __init__(self, store)`
- `FusionAnalytics.entity_timeline` (method) `estorides_core/fusion_analytics.py:46` `def entity_timeline(self, eid)`
- `FusionAnalytics.entity_summary` (method) `estorides_core/fusion_analytics.py:132` `def entity_summary(self, eid)`
- `FusionAnalytics.source_stats` (method) `estorides_core/fusion_analytics.py:213` `def source_stats(self, source_name)`
- `FusionAnalytics.multi_source_consensus` (method) `estorides_core/fusion_analytics.py:290` `def multi_source_consensus(self, eid, key)`
- `FusionAnalytics.corroborated_properties` (method) `estorides_core/fusion_analytics.py:343` `def corroborated_properties(self, eid, min_sources)`
- `FusionAnalytics.entity_search` (method) `estorides_core/fusion_analytics.py:374` `def entity_search(self, term, etype)`
- `FusionAnalytics.top_changed` (method) `estorides_core/fusion_analytics.py:432` `def top_changed(self, days, limit)`
- `FusionAnalytics.source_corroboration_matrix` (method) `estorides_core/fusion_analytics.py:477` `def source_corroboration_matrix(self, limit)`

## estorides_core/fusion_store.py
Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/ids.py`, `estorides_core/reliability_scoring.py`, `estorides_core/sqlite_store.py`
Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`
- `normalize_value` (function) `estorides_core/fusion_store.py:73` `def normalize_value(etype, value)`
- `entity_id` (function) `estorides_core/fusion_store.py:177` `def entity_id(etype, value, normalized)` -- Deterministic, run-independent id for an entity.
- `FusionStore.register_sources` (method) `estorides_core/fusion_store.py:222` `def register_sources(self, sources)` -- Mirror the YAML source catalogue into the store.
- `FusionStore.add_observation` (method) `estorides_core/fusion_store.py:259` `def add_observation(self, observation)` -- Fuse a single source response into the cross-run observation log and bump the source's fetch/ok counters.
- `FusionStore.fuse_entity` (method) `estorides_core/fusion_store.py:300` `def fuse_entity(self, entity)` -- Fuse one entity into the canonical store and return its id.
- `FusionStore.fuse_entities` (method) `estorides_core/fusion_store.py:403` `def fuse_entities(self, entities)` -- Fuse a batch of entities, returning the list of fused ids.
- `FusionStore.fuse_properties` (method) `estorides_core/fusion_store.py:416` `def fuse_properties(self, eid, parsed, source)` -- Fuse the flat scalar attributes of a parsed observation onto an entity, attributed to ``source``.
- `FusionStore.fuse_relationship` (method) `estorides_core/fusion_store.py:462` `def fuse_relationship(self, src_type, src_value, relation, dst_type, dst_value)` -- Fuse one directed edge between two entities, attributed to source.
- `FusionStore.fuse_graph` (method) `estorides_core/fusion_store.py:532` `def fuse_graph(self, kg)` -- Mirror the analytic edges of a knowledge graph into the store.
- `FusionStore.get_entity` (method) `estorides_core/fusion_store.py:568` `def get_entity(self, eid)` -- Return one fused entity with its provenance, properties and edges.
- `FusionStore.search_entities` (method) `estorides_core/fusion_store.py:614` `def search_entities(self, term, etype)` -- Search fused entities by value substring and/or type.
- `FusionStore.corroborated_properties` (method) `estorides_core/fusion_store.py:657` `def corroborated_properties(self, eid, min_sources)` -- Return an entity's properties that at least ``min_sources`` distinct feeds independently asserted — the fusion...
- `FusionStore.list_sources` (method) `estorides_core/fusion_store.py:674` `def list_sources(self, limit)` -- Return the source catalogue with accumulated fetch/ok counters.
- `FusionStore.stats` (method) `estorides_core/fusion_store.py:692` `def stats(self)` -- One-glance dashboard of the fused store's size.
- `open_store` (function) `estorides_core/fusion_store.py:723` `def open_store(path)` -- Open the fusion store, returning None instead of raising on failure.

## estorides_core/graph_bundle.py
Depends on: `estorides_core/graph_force.py`
Imported by: `tests/properties/test_graph_bundle_properties.py`, `tests/test_graph_bundle.py`
- `hierarchical_edge_bundling` (function) `estorides_core/graph_bundle.py:171` `def hierarchical_edge_bundling(groups, edges, center, radius, beta, samples, group_gap, inner_ratio)` -- Hojas en un circulo por grupo; aristas por la jerarquia (Holten 2006).
- `fibonacci_sphere` (function) `estorides_core/graph_bundle.py:215` `def fibonacci_sphere(count)` -- Vectores unitarios casi uniformes en espiral de angulo dorado.
- `spherical_edge_bundling` (function) `estorides_core/graph_bundle.py:267` `def spherical_edge_bundling(groups, edges, radius, beta, samples, inner_ratio)` -- Hojas en caps esfericos por comunidad; aristas por la jerarquia.
- `bundle_settings` (function) `estorides_core/graph_bundle.py:324` `def bundle_settings()` -- Defaults de la pagina bundle (fuente unica para el JS).
- `build_bundle_payload` (function) `estorides_core/graph_bundle.py:359` `def build_bundle_payload(force_payload)` -- Deriva el payload bundle desde un payload force RAW.

## estorides_core/graph_force.py
Imported by: `estorides_core/graph_bundle.py`, `estorides_web.py`, `tests/test_graph_bundle.py`, `tests/test_graph_force3d.py`
- `family_color_from_name` (function) `estorides_core/graph_force.py:48` `def family_color_from_name(name, sat_base, sat_span, light_base, light_span)` -- Deriva un color HSL estable desde un label (djb2, como ReadMenator).
- `node_value` (function) `estorides_core/graph_force.py:65` `def node_value(symbols, degree, findings)` -- Escala log2 del tamano de nodo (minimo 1).
- `force_settings` (function) `estorides_core/graph_force.py:70` `def force_settings()` -- Valores SETTINGS de ReadMenator graph-force.html (fuente unica).
- `build_force_payload` (function) `estorides_core/graph_force.py:161` `def build_force_payload(nodes, edges, clusters, max_nodes, max_edges)` -- Convierte nodos/edges OSINT (`/api/graph`) al formato RAW force-graph.
- `build_ai_context` (function) `estorides_core/graph_force.py:353` `def build_ai_context(nodes, edges, clusters, budget_chars)` -- Contexto markdown extractivo con presupuesto para la IA local.

## estorides_core/graph_kuzu.py
Depends on: `estorides_core/config.py`
Imported by: `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`
- `KuzuGraphBackend.__init__` (method) `estorides_core/graph_kuzu.py:205` `def __init__(self, path)`
- `KuzuGraphBackend.upsert_entity` (method) `estorides_core/graph_kuzu.py:245` `def upsert_entity(self, ent_type, value, source)` -- Insert (or merge) an entity.
- `KuzuGraphBackend.upsert_relationship` (method) `estorides_core/graph_kuzu.py:295` `def upsert_relationship(self, src_type, src_value, rel, dst_type, dst_value)` -- Insert an edge between two entities.
- `KuzuGraphBackend.neighbors` (method) `estorides_core/graph_kuzu.py:346` `def neighbors(self, node_id, hops, relation, limit)` -- Return nodes reachable from `node_id` within `hops` edges.
- `KuzuGraphBackend.cypher` (method) `estorides_core/graph_kuzu.py:379` `def cypher(self, query, params)` -- Run a Cypher query and return rows as a list of dicts.
- `KuzuGraphBackend.stats` (method) `estorides_core/graph_kuzu.py:406` `def stats(self)` -- Return counts of every node label and edge rel type.
- `KuzuGraphBackend.close` (method) `estorides_core/graph_kuzu.py:436` `def close(self)`

## estorides_core/graph_rag_search.py
Imported by: `estorides_web.py`, `tests/test_graph_rag_search.py`
- `graph_rag_config_from_env` (function) `estorides_core/graph_rag_search.py:75` `def graph_rag_config_from_env()` -- Construye la config desde env; malformada → defaults (nunca raise).
- `tokenize` (function) `estorides_core/graph_rag_search.py:98` `def tokenize(text, min_len, stopwords)` -- Parte en tokens minusculos; camelCase se divide y se conserva entero.
- `Bm25Index.__init__` (method) `estorides_core/graph_rag_search.py:115` `def __init__(self, documents, k1, b)`
- `Bm25Index.scores` (method) `estorides_core/graph_rag_search.py:136` `def scores(self, query)` -- Un score BM25 por documento, en orden de corpus.
- `pagerank` (function) `estorides_core/graph_rag_search.py:176` `def pagerank(ids, edges, alpha, max_iter, tolerance)` -- PageRank dirigido y pesado; los scores suman 1 (determinista).
- `personalized_pagerank` (function) `estorides_core/graph_rag_search.py:207` `def personalized_pagerank(ids, edges, seeds, alpha, max_iter, tolerance)` -- PPR con teletransporte al seed; seeds ajenos se ignoran.
- `GraphRagIndex.to_dict` (method) `estorides_core/graph_rag_search.py:324` `def to_dict(self)`
- `GraphRagIndex.from_dict` (method) `estorides_core/graph_rag_search.py:334` `def from_dict(cls, data)`
- `rows` (function) `estorides_core/graph_rag_search.py:335` `def rows(name)`
- `meta` (function) `estorides_core/graph_rag_search.py:341` `def meta()`
- `build_index` (function) `estorides_core/graph_rag_search.py:382` `def build_index(nodes, edges, clusters, config)` -- Indice extractivo desde nodos/edges estilo `/api/graph` (puro).
- `where` (function) `estorides_core/graph_rag_search.py:446` `def where(cid)`
- `GraphRagSearcher.__init__` (method) `estorides_core/graph_rag_search.py:596` `def __init__(self, config, index)`
- `GraphRagSearcher.choose_mode` (method) `estorides_core/graph_rag_search.py:635` `def choose_mode(self, query)`
- `GraphRagSearcher.search` (method) `estorides_core/graph_rag_search.py:644` `def search(self, query, mode, budget_tokens)`
- `GraphRagSearcher.local_search` (method) `estorides_core/graph_rag_search.py:658` `def local_search(self, query, budget_tokens)`
- `GraphRagSearcher.global_search` (method) `estorides_core/graph_rag_search.py:754` `def global_search(self, query, budget_tokens)`
- `ask_context` (function) `estorides_core/graph_rag_search.py:857` `def ask_context(query, nodes, edges, clusters, budget_tokens, mode, config)` -- One-shot: build + search (el camino que usa la capa IA local).
- `graph_context_block` (function) `estorides_core/graph_rag_search.py:886` `def graph_context_block(query, nx_graph, cluster_of, budget_tokens, mode, config)` -- Bloque markdown para el prompt LLM desde un grafo networkx (duck-typing).

## estorides_core/hypothesis_engine.py
Depends on: `estorides_core/ids.py`, `estorides_core/reliability_scoring.py`
Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`
- `HypothesisGenerator.__call__` (method) `estorides_core/hypothesis_engine.py:213` `def __call__(self, observations, entities)`
- `generate_hypotheses` (function) `estorides_core/hypothesis_engine.py:613` `def generate_hypotheses(observations, entities, kg)` -- Generate typed, scored, auditable hypotheses for a run.

## estorides_core/ids.py
Imported by: `estorides_core/change_detection.py`, `estorides_core/entity_resolution.py`, `estorides_core/fusion_store.py`, `estorides_core/hypothesis_engine.py`, `estorides_core/recon_fusion.py`, `tests/test_ids.py`
- `stable_id` (function) `estorides_core/ids.py:21` `def stable_id(payload, length)` -- Deterministic hex id of `length` chars for a UTF-8 payload.

## estorides_core/intel_resolver.py
Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`, `tests/test_transforms.py`
- `_TTLCache.__init__` (method) `estorides_core/intel_resolver.py:121` `def __init__(self)`
- `_TTLCache.get` (method) `estorides_core/intel_resolver.py:127` `def get(self, kind, key)`
- `_TTLCache.put` (method) `estorides_core/intel_resolver.py:140` `def put(self, kind, key, value)`
- `_TTLCache.stats` (method) `estorides_core/intel_resolver.py:148` `def stats(self)`
- `EntityResolver.__init__` (method) `estorides_core/intel_resolver.py:165` `def __init__(self)`
- `EntityResolver.resolve` (method) `estorides_core/intel_resolver.py:174` `def resolve(self, ent_type, ent_id)`

## estorides_core/job_registry.py
Imported by: `estorides_core/discoverer.py`, `estorides_web.py`, `tests/test_job_registry.py`
- `BoundedJobRegistry.__init__` (method) `estorides_core/job_registry.py:49` `def __init__(self)`
- `BoundedJobRegistry.register` (method) `estorides_core/job_registry.py:60` `def register(self, key, value)` -- Insert (or replace) a job, evicting expired and overflow entries.
- `BoundedJobRegistry.get` (method) `estorides_core/job_registry.py:80` `def get(self, key)` -- Return the value for `key` or None.
- `BoundedJobRegistry.pop` (method) `estorides_core/job_registry.py:95` `def pop(self, key)` -- Remove and return the value for `key`, or None.
- `BoundedJobRegistry.keys` (method) `estorides_core/job_registry.py:101` `def keys(self)`
- `BoundedJobRegistry.values` (method) `estorides_core/job_registry.py:105` `def values(self)`
- `BoundedJobRegistry.evict_expired` (method) `estorides_core/job_registry.py:113` `def evict_expired(self)` -- Sweep and drop TTL-expired entries.

## estorides_core/knowledge_graph.py
Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`
- `KnowledgeGraph.__init__` (method) `estorides_core/knowledge_graph.py:91` `def __init__(self, name)`
- `KnowledgeGraph.add_entity` (method) `estorides_core/knowledge_graph.py:97` `def add_entity(self, entity)` -- Insert an entity.
- `KnowledgeGraph.add_observation` (method) `estorides_core/knowledge_graph.py:127` `def add_observation(self, source, entities)` -- Add every entity + every co-occurrence edge within the same response.
- `KnowledgeGraph.add_relationship` (method) `estorides_core/knowledge_graph.py:142` `def add_relationship(self, src_type, src_value, rel, dst_type, dst_value)`
- `KnowledgeGraph.export_graphml` (method) `estorides_core/knowledge_graph.py:164` `def export_graphml(self, path)`
- `KnowledgeGraph.export_json` (method) `estorides_core/knowledge_graph.py:183` `def export_json(self)`
- `KnowledgeGraph.export_lazyown` (method) `estorides_core/knowledge_graph.py:207` `def export_lazyown(self)` -- Emit the graph in LazyOwn intel vocabulary (JSON-serializable).
- `KnowledgeGraph.summary` (method) `estorides_core/knowledge_graph.py:243` `def summary(self)`
- `KnowledgeGraph.top_entities` (method) `estorides_core/knowledge_graph.py:261` `def top_entities(self, n, by)`
- `KnowledgeGraph.communities` (method) `estorides_core/knowledge_graph.py:281` `def communities(self, nodes)` -- Partition entity nodes into communities (clusters).
- `KnowledgeGraph.intel_level` (method) `estorides_core/knowledge_graph.py:312` `def intel_level(self, node_id, bridge_nodes)` -- Classify a node into the intelligence pipeline tier.
- `KnowledgeGraph.ego_subgraph` (method) `estorides_core/knowledge_graph.py:357` `def ego_subgraph(self, node_id, radius)`
- `KnowledgeGraph.neighbours` (method) `estorides_core/knowledge_graph.py:368` `def neighbours(self, node_id, relation)`

## estorides_core/lan_bundle.py
- `sanitize_stem` (function) `estorides_core/lan_bundle.py:27` `def sanitize_stem(stem)` -- Sanitize a file stem.
- `default_output_dir` (function) `estorides_core/lan_bundle.py:38` `def default_output_dir()` -- Resolve the LAN output directory from env or data default.
- `build_bundle` (function) `estorides_core/lan_bundle.py:47` `def build_bundle(devices)` -- Build all four payloads.
- `LanBundleResult.to_dict` (method) `estorides_core/lan_bundle.py:358` `def to_dict(self)`
- `write_bundle` (function) `estorides_core/lan_bundle.py:362` `def write_bundle(devices)` -- Write all four deliverables atomically.

## estorides_core/lan_inventory.py
Imported by: `tests/test_lan_bundle.py`
- `LanDevice.to_dict` (method) `estorides_core/lan_inventory.py:60` `def to_dict(self)`
- `normalize_mac` (function) `estorides_core/lan_inventory.py:64` `def normalize_mac(raw)` -- Normalize MAC to lowercase colon form, or None when invalid.
- `parse_arp_table` (function) `estorides_core/lan_inventory.py:91` `def parse_arp_table(text)` -- Parse `ip neigh` or /proc/net/arp text into sightings.
- `parse_dhcp_leases` (function) `estorides_core/lan_inventory.py:119` `def parse_dhcp_leases(text)` -- Parse dnsmasq lease lines into sightings.
- `parse_nmap_xml` (function) `estorides_core/lan_inventory.py:152` `def parse_nmap_xml(text)` -- Parse nmap -oX output into sightings.
- `parse_nmap_grepable` (function) `estorides_core/lan_inventory.py:214` `def parse_nmap_grepable(text)` -- Parse nmap -oG output into sightings.
- `parse_active_output` (function) `estorides_core/lan_inventory.py:252` `def parse_active_output(text, source)` -- Dispatch active-tool output by format, tagged with source.
- `merge_devices` (function) `estorides_core/lan_inventory.py:269` `def merge_devices(sightings)` -- Merge sightings by MAC, falling back to IP.
- `device_to_entities` (function) `estorides_core/lan_inventory.py:331` `def device_to_entities(device)` -- Convert a device into graph-ready entity dicts.
- `contact_for_tool` (function) `estorides_core/lan_inventory.py:352` `def contact_for_tool(tool)` -- Map a tool name to its contact class.

## estorides_core/lan_policy.py
- `LanPolicyDecision.to_dict` (method) `estorides_core/lan_policy.py:50` `def to_dict(self)`
- `requires_consent` (function) `estorides_core/lan_policy.py:54` `def requires_consent()` -- Return the canonical consent notice for the blocking modal.
- `max_contact_for` (function) `estorides_core/lan_policy.py:97` `def max_contact_for(allow_active, consent)` -- Return active only on the triple gate, else none.
- `evaluate` (function) `estorides_core/lan_policy.py:104` `def evaluate(request)` -- Evaluate a LAN policy request.

## estorides_core/lan_runner.py
Depends on: `estorides_core/tool_runner.py`
- `LanScanResult.to_dict` (method) `estorides_core/lan_runner.py:56` `def to_dict(self)`
- `read_arp_table` (function) `estorides_core/lan_runner.py:60` `def read_arp_table()` -- Read the local neighbor table.
- `read_dhcp_leases` (function) `estorides_core/lan_runner.py:81` `def read_dhcp_leases()` -- Read the first readable dnsmasq lease file.
- `run_active_scan` (function) `estorides_core/lan_runner.py:122` `def run_active_scan(scope_cidr)` -- Run gated active discovery.
- `scan` (function) `estorides_core/lan_runner.py:147` `def scan(scope_cidr)` -- Execute a LAN scan.

## estorides_core/lan_scope.py
- `parse_interface_addr` (function) `estorides_core/lan_scope.py:23` `def parse_interface_addr(raw)` -- Normalize one interface address to CIDR, or None when unsafe.
- `select_private_cidrs` (function) `estorides_core/lan_scope.py:63` `def select_private_cidrs(interfaces)` -- Keep private CIDRs only, sorted and deduped.
- `default_scope` (function) `estorides_core/lan_scope.py:79` `def default_scope(interfaces)` -- First private CIDR, or None when no private network exists.
- `parse_ip_addr_output` (function) `estorides_core/lan_scope.py:85` `def parse_ip_addr_output(text)` -- Parse `ip addr` output into address dicts.
- `read_local_interfaces` (function) `estorides_core/lan_scope.py:92` `def read_local_interfaces()` -- Read local interface addresses.

## estorides_core/lan_web.py
Imported by: `estorides_web.py`
- `LanWebVerdict.to_dict` (method) `estorides_core/lan_web.py:29` `def to_dict(self)`
- `LanWebVerdict.to_response` (method) `estorides_core/lan_web.py:32` `def to_response(self)` -- Return (body, status) for the Flask route.
- `is_lan_request` (function) `estorides_core/lan_web.py:50` `def is_lan_request(body, query)` -- True when a run targets the local network.
- `scope_payload` (function) `estorides_core/lan_web.py:80` `def scope_payload(interfaces)` -- Build the scope response from interface addresses.
- `guard` (function) `estorides_core/lan_web.py:92` `def guard(body)` -- Validate a run request body for LAN consent.

## estorides_core/mitre_attack.py
Imported by: `estorides_core/orchestrator.py`
- `map_observation` (function) `estorides_core/mitre_attack.py:170` `def map_observation(observation)` -- Return ATT&CK techniques associated with an observation.
- `map_observations` (function) `estorides_core/mitre_attack.py:213` `def map_observations(observations)` -- Bulk mapper.
- `all_techniques_for` (function) `estorides_core/mitre_attack.py:229` `def all_techniques_for(observations)` -- Aggregate: unique techniques across all observations, sorted by id.

## estorides_core/monitoring.py
Depends on: `estorides_core/config.py`, `estorides_core/sqlite_store.py`
Imported by: `estorides_cli.py`, `estorides_web.py`, `tests/test_cli_watch.py`, `tests/test_monitoring.py`
- `WatchTarget.to_dict` (method) `estorides_core/monitoring.py:110` `def to_dict(self)`
- `WatchTarget.from_dict` (method) `estorides_core/monitoring.py:126` `def from_dict(cls, d)`
- `WatchTarget.from_row` (method) `estorides_core/monitoring.py:142` `def from_row(cls, row)`
- `WatchStore.create_watch` (method) `estorides_core/monitoring.py:162` `def create_watch(self, watch)` -- Persist a new watch target.
- `WatchStore.get_watch` (method) `estorides_core/monitoring.py:177` `def get_watch(self, watch_id)`
- `WatchStore.update_watch` (method) `estorides_core/monitoring.py:186` `def update_watch(self, watch)`
- `WatchStore.delete_watch` (method) `estorides_core/monitoring.py:199` `def delete_watch(self, watch_id)`
- `WatchStore.list_watches` (method) `estorides_core/monitoring.py:203` `def list_watches(self, enabled_only)`
- `WatchStore.due_watches` (method) `estorides_core/monitoring.py:213` `def due_watches(self, now)` -- Return enabled watches whose next_run_at <= now.
- `WatchStore.record_run_start` (method) `estorides_core/monitoring.py:226` `def record_run_start(self, watch_id)` -- Record a watch run start, return history entry id.
- `WatchStore.record_run_complete` (method) `estorides_core/monitoring.py:236` `def record_run_complete(self, history_id, status, entity_count, obs_count, error, alert_sent)`
- `WatchStore.history` (method) `estorides_core/monitoring.py:249` `def history(self, watch_id, limit)`
- `WatchStore.stats` (method) `estorides_core/monitoring.py:266` `def stats(self)`
- `WatchScheduler.__init__` (method) `estorides_core/monitoring.py:287` `def __init__(self, store, runner, alerter)`
- `WatchScheduler.running` (method) `estorides_core/monitoring.py:300` `def running(self)`
- `WatchScheduler.has_runner` (method) `estorides_core/monitoring.py:304` `def has_runner(self)` -- True once an executor has been wired via set_runner().
- `WatchScheduler.start` (method) `estorides_core/monitoring.py:308` `def start(self)`
- `WatchScheduler.stop` (method) `estorides_core/monitoring.py:319` `def stop(self)`
- `WatchScheduler.set_runner` (method) `estorides_core/monitoring.py:325` `def set_runner(self, runner)` -- Set the orchestrator runner function (sync or async).
- `WatchScheduler.set_alerter` (method) `estorides_core/monitoring.py:329` `def set_alerter(self, alerter)` -- Set the alert dispatcher.

## estorides_core/observation_models.py
Depends on: `estorides_core/config.py`
Imported by: `tests/properties/test_observation_models_properties.py`, `tests/test_observation_models.py`
- `ObservationMeta.to_legacy_dict` (method) `estorides_core/observation_models.py:95` `def to_legacy_dict(self)`
- `Observation.to_legacy_dict` (method) `estorides_core/observation_models.py:128` `def to_legacy_dict(self)`
- `ObservedEntity.to_legacy_dict` (method) `estorides_core/observation_models.py:163` `def to_legacy_dict(self)`
- `RunResult.to_legacy_dict` (method) `estorides_core/observation_models.py:183` `def to_legacy_dict(self)`

## estorides_core/ontology.py
Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`
- `SanctionEntry.to_dict` (method) `estorides_core/ontology.py:79` `def to_dict(self)`
- `SanctionsIndex.__init__` (method) `estorides_core/ontology.py:115` `def __init__(self)`
- `SanctionsIndex.is_ready` (method) `estorides_core/ontology.py:131` `def is_ready(self)`
- `SanctionsIndex.entries` (method) `estorides_core/ontology.py:134` `def entries(self)` -- Return the current snapshot, loading if necessary.
- `SanctionsIndex.lookup` (method) `estorides_core/ontology.py:141` `def lookup(self, name)` -- Find sanction entries whose name or alias matches `name`.
- `SanctionsIndex.lookup_crypto` (method) `estorides_core/ontology.py:151` `def lookup_crypto(self, address)` -- Cross-check a BTC/ETH address against the SDN list.
- `SanctionsIndex.size` (method) `estorides_core/ontology.py:168` `def size(self)`
- `WikidataCache.__init__` (method) `estorides_core/ontology.py:276` `def __init__(self)`
- `WikidataCache.get` (method) `estorides_core/ontology.py:282` `def get(self, kind, value)`
- `WikidataCache.put` (method) `estorides_core/ontology.py:296` `def put(self, kind, value, payload)`
- `WikidataCache.stats` (method) `estorides_core/ontology.py:304` `def stats(self)`
- `WikidataCache.clear` (method) `estorides_core/ontology.py:308` `def clear(self)`
- `OntologyEngine.__init__` (method) `estorides_core/ontology.py:317` `def __init__(self)`
- `OntologyEngine.check_observation` (method) `estorides_core/ontology.py:321` `def check_observation(self, observation)` -- Run a single observation through the ontology.

## estorides_core/openapi.py
Imported by: `estorides_web.py`
- `build_openapi` (function) `estorides_core/openapi.py:14` `def build_openapi(app)` -- Build an OpenAPI 3.0 document from Flask routes.

## estorides_core/ops_observability.py
Depends on: `estorides_core/config.py`
Imported by: `estorides_web.py`, `tests/test_ops_observability.py`
- `health_payload` (function) `estorides_core/ops_observability.py:50` `def health_payload()` -- Return liveness body and status code.
- `ready_payload` (function) `estorides_core/ops_observability.py:55` `def ready_payload(source_count, sources_dir_ok)` -- Return readiness body and status code for registry state.
- `record_request` (function) `estorides_core/ops_observability.py:62` `def record_request(endpoint, status)` -- Count one HTTP response by normalized endpoint and status.
- `record_source` (function) `estorides_core/ops_observability.py:72` `def record_source(source, ok)` -- Count one source execution failure when ok is False.
- `reset_metrics` (function) `estorides_core/ops_observability.py:83` `def reset_metrics()` -- Clear all in memory counters for tests and process restart.
- `render_metrics` (function) `estorides_core/ops_observability.py:90` `def render_metrics()` -- Render counters in Prometheus exposition text format.
- `format_event` (function) `estorides_core/ops_observability.py:112` `def format_event(fields, as_json)` -- Format one log event as JSON when opted in else legacy plain text.
- `project_root` (function) `estorides_core/ops_observability.py:130` `def project_root()` -- Expose project root without hardcoding absolute paths in callers.

## estorides_core/orchestrator.py
Depends on: `estorides_core/async_client.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/event_bus.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/mitre_attack.py`, `estorides_core/ontology.py`, `estorides_core/pagination.py`, `estorides_core/parsers.py`, `estorides_core/recon_fusion.py`, `estorides_core/relationship_inference.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_llm/__init__.py`
Imported by: `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_web.py`, `tests/test_central_config.py`, `tests/test_keyless_sources.py`, `tests/test_opsec_contact.py`, `tests/test_source_routing.py`, `tests/test_system_app_sources.py`
- `pending_system_app_tasks` (function) `estorides_core/orchestrator.py:56` `def pending_system_app_tasks()` -- Number of slow CLI-tool runs still in flight (for the stream gate).
- `repl` (function) `estorides_core/orchestrator.py:122` `def repl(m)`
- `Orchestrator.__init__` (method) `estorides_core/orchestrator.py:169` `def __init__(self, registry, llm, kg)`
- `Orchestrator.run` (method) `estorides_core/orchestrator.py:190` `def run(self, query)` -- Run a full intelligence cycle.

## estorides_core/osiris_sources.py
Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- `fetch_bgp` (function) `estorides_core/osiris_sources.py:119` `def fetch_bgp(query)` -- Look up an IP or AS number against bgpview.io (free, no key).
- `fetch_mac` (function) `estorides_core/osiris_sources.py:185` `def fetch_mac(mac)` -- Look up a MAC address against macvendors.co (free, no key).
- `fetch_phone` (function) `estorides_core/osiris_sources.py:233` `def fetch_phone(number)` -- Best-effort phone geolocation.
- `fetch_github_user` (function) `estorides_core/osiris_sources.py:302` `def fetch_github_user(username)` -- Look up a GitHub user (keyless, rate-limited).
- `fetch_leaks` (function) `estorides_core/osiris_sources.py:356` `def fetch_leaks(email)` -- Breach analytics for `email` via xposedornot (free, no key).
- `fetch_cisa_kev` (function) `estorides_core/osiris_sources.py:400` `def fetch_cisa_kev(limit, days)` -- Recently-added CVEs from the CISA KEV feed (authoritative).
- `fetch_malware_c2` (function) `estorides_core/osiris_sources.py:452` `def fetch_malware_c2(limit)` -- Active botnet C2 (Feodo) + recent malware URLs (URLhaus).


Next: [API_p2.md](API_p2.md)
