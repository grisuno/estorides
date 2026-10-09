# API (page 1 of 3)
Pages: [API.md](API.md), [API_p2.md](API_p2.md), [API_p3.md](API_p3.md)

## estorides_cli.py
Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`
Imported by: `tests/test_cli_watch.py`
- `cmd_discover` (function) `estorides_cli.py:93` `def cmd_discover(args)` -- v1.2 — fanout the surface from a seed.
- `cmd_run` (function) `estorides_cli.py:205` `def cmd_run(args)`
- `cmd_scope` (function) `estorides_cli.py:282` `def cmd_scope(args)` -- Classify discovered assets against a program's scope rules.
- `cmd_graph_export` (function) `estorides_cli.py:328` `def cmd_graph_export(args)`
- `cmd_export_stix` (function) `estorides_cli.py:351` `def cmd_export_stix(args)`
- `cmd_export_misp` (function) `estorides_cli.py:361` `def cmd_export_misp(args)`
- `cmd_report` (function) `estorides_cli.py:371` `def cmd_report(args)` -- Render a Markdown report for a case.
- `cmd_diff` (function) `estorides_cli.py:412` `def cmd_diff(args)` -- Diff two cases.
- `cmd_status` (function) `estorides_cli.py:440` `def cmd_status(_)`
- `cmd_fusion` (function) `estorides_cli.py:447` `def cmd_fusion(args)` -- Query the cross-run fusion datastore.
- `cmd_watch_add` (function) `estorides_cli.py:490` `def cmd_watch_add(args)` -- Add a new recurring watch target.
- `cmd_watch_list` (function) `estorides_cli.py:554` `def cmd_watch_list(args)` -- List all watch targets.
- `cmd_watch_remove` (function) `estorides_cli.py:574` `def cmd_watch_remove(args)` -- Delete a watch target.
- `cmd_watch_enable` (function) `estorides_cli.py:586` `def cmd_watch_enable(args)`
- `cmd_watch_disable` (function) `estorides_cli.py:599` `def cmd_watch_disable(args)`
- `cmd_watch_history` (function) `estorides_cli.py:611` `def cmd_watch_history(args)`
- `cmd_alerts_test` (function) `estorides_cli.py:632` `def cmd_alerts_test(args)`
- `cmd_alerts_channels` (function) `estorides_cli.py:644` `def cmd_alerts_channels(args)`
- `cmd_scheduler_start` (function) `estorides_cli.py:656` `def cmd_scheduler_start(args)`
- `cmd_scheduler_stop` (function) `estorides_cli.py:666` `def cmd_scheduler_stop(args)`
- `cmd_scheduler_status` (function) `estorides_cli.py:676` `def cmd_scheduler_status(args)`
- `cmd_serve` (function) `estorides_cli.py:684` `def cmd_serve(args)`
- `build_parser` (function) `estorides_cli.py:701` `def build_parser()`
- `main` (function) `estorides_cli.py:857` `def main(argv)`

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
- `TheHarvesterResult.run_nmap` (method) `estorides_core/active_recon.py:213` `def run_nmap(target, args)`
- `TheHarvesterResult.run_nikto` (method) `estorides_core/active_recon.py:243` `def run_nikto(target, args)`
- `TheHarvesterResult.run_sqlmap` (method) `estorides_core/active_recon.py:269` `def run_sqlmap(target, args)`
- `TheHarvesterResult.run_dnsrecon` (method) `estorides_core/active_recon.py:295` `def run_dnsrecon(target, args)`
- `TheHarvesterResult.run_theHarvester` (method) `estorides_core/active_recon.py:325` `def run_theHarvester(target, args)`

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
- `AsyncClient.sync_fetch` (method) `estorides_core/async_client.py:400` `def sync_fetch(method, url)`

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
- `ChangeReport.detect_changes` (method) `estorides_core/change_detection.py:284` `def detect_changes(snapshot_before, snapshot_after)` -- Diff two snapshots.

## estorides_core/cloud_asset_discovery.py
Imported by: `estorides_core/recon_pipeline.py`, `tests/test_cloud_asset_discovery.py`
- `CloudAsset.to_dict` (method) `estorides_core/cloud_asset_discovery.py:45` `def to_dict(self)`
- `CloudAssetDiscoveryResult.to_dict` (method) `estorides_core/cloud_asset_discovery.py:56` `def to_dict(self)`
- `CloudAssetDiscoveryResult.generate_bucket_names` (method) `estorides_core/cloud_asset_discovery.py:65` `def generate_bucket_names(domain)`
- `CloudAssetDiscoveryResult.assess_bucket` (method) `estorides_core/cloud_asset_discovery.py:84` `def assess_bucket(url, method)`

## estorides_core/code_exposure.py
Imported by: `estorides_core/recon_pipeline.py`, `tests/test_code_exposure.py`
- `CodeFinding.to_dict` (method) `estorides_core/code_exposure.py:57` `def to_dict(self)`
- `SeveritySummary.to_dict` (method) `estorides_core/code_exposure.py:69` `def to_dict(self)`
- `CodeExposureResult.to_dict` (method) `estorides_core/code_exposure.py:81` `def to_dict(self)`
- `CodeExposureResult.validate_aws_key` (method) `estorides_core/code_exposure.py:91` `def validate_aws_key(key)`
- `CodeExposureResult.classify_finding` (method) `estorides_core/code_exposure.py:99` `def classify_finding(content, source, file_path)`
- `CodeExposureResult.analyse_findings` (method) `estorides_core/code_exposure.py:189` `def analyse_findings(findings, rate_limited)`

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
- `RetryConfig.retry_delay` (method) `estorides_core/config.py:672` `def retry_delay(attempt)` -- Return the backoff sleep for a 1-indexed attempt.

## estorides_core/discoverer.py
Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
Imported by: `estorides_cli.py`, `estorides_web.py`, `static/js/estorides.js`
- `DiscoverJob.stop` (method) `estorides_core/discoverer.py:78` `def stop(self)`
- `DiscoverJob.should_stop` (method) `estorides_core/discoverer.py:81` `def should_stop(self)`
- `DiscoverJob.push_event` (method) `estorides_core/discoverer.py:84` `def push_event(self, ev)` -- Append an event and keep the buffer bounded.
- `_DiscoverJobSink.__init__` (method) `estorides_core/discoverer.py:103` `def __init__(self, job)`
- `_DiscoverJobSink.emit` (method) `estorides_core/discoverer.py:106` `def emit(self, event)`
- `_DiscoverJobSink.create_discover_job` (method) `estorides_core/discoverer.py:194` `def create_discover_job(seed_type, seed_value)` -- Create and register a discovery job synchronously.
- `_DiscoverJobSink.start_discover` (method) `estorides_core/discoverer.py:252` `def start_discover(seed_type, seed_value)` -- Create a discovery job and schedule its worker on the current loop.
- `_DiscoverJobSink.start_discover_threadsafe` (method) `estorides_core/discoverer.py:285` `def start_discover_threadsafe(loop, seed_type, seed_value)` -- Create the job in the calling thread, fire its worker on `loop`.
- `_DiscoverJobSink.list_jobs` (method) `estorides_core/discoverer.py:349` `def list_jobs(limit)` -- Snapshot of the recent jobs for the /api/discover/jobs endpoint.

## estorides_core/entity_extraction.py
Depends on: `estorides_core/config.py`
Imported by: `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_extraction.py`, `tests/test_entity_resolution.py`, `tests/test_query_intent.py`, `tests/test_socmint.py`, `tests/test_structured_extraction.py`
- `Entity.to_dict` (method) `estorides_core/entity_extraction.py:34` `def to_dict(self)`
- `Entity.normalize_query` (method) `estorides_core/entity_extraction.py:57` `def normalize_query(query)` -- Return the routing form of raw operator input.
- `Entity.detect_query_type` (method) `estorides_core/entity_extraction.py:100` `def detect_query_type(query)` -- Return the detected type of a free-form query.
- `Entity.extract_from_text` (method) `estorides_core/entity_extraction.py:146` `def extract_from_text(text, source)` -- Find every recognised entity in a raw text blob.
- `Entity.extract_from_json` (method) `estorides_core/entity_extraction.py:210` `def extract_from_json(payload, source)` -- Pull entities out of a JSON-like structure.
- `Entity.extract_structured` (method) `estorides_core/entity_extraction.py:330` `def extract_structured(payload, source)` -- Extract human selectors (email, username, person, org, phone) by key.
- `Entity.visit` (method) `estorides_core/entity_extraction.py:344` `def visit(node, key)`
- `Entity.merge` (method) `estorides_core/entity_extraction.py:382` `def merge()` -- Deduplicate by (type, value) and merge sources / contexts.
- `Entity.find` (method) `estorides_core/entity_extraction.py:499` `def find(x, parent)`
- `Entity.union` (method) `estorides_core/entity_extraction.py:505` `def union(a, b, parent)`
- `Entity.norm` (method) `estorides_core/entity_extraction.py:510` `def norm(v)`

## estorides_core/entity_resolution.py
Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/ids.py`, `estorides_core/transliteration.py`
Imported by: `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`
- `jaro` (function) `estorides_core/entity_resolution.py:83` `def jaro(s1, s2)` -- Return the Jaro similarity of two strings in ``[0, 1]``.
- `jaro_winkler` (function) `estorides_core/entity_resolution.py:126` `def jaro_winkler(s1, s2, prefix_weight)` -- Jaro-Winkler similarity: Jaro with a shared-prefix bonus.
- `normalize_value` (function) `estorides_core/entity_resolution.py:206` `def normalize_value(etype, value)` -- Return the canonical normalised form of an entity value.
- `canonical_id` (function) `estorides_core/entity_resolution.py:246` `def canonical_id(etype, normalized)` -- Stable, content-addressed id for a normalised entity.
- `blocking_keys` (function) `estorides_core/entity_resolution.py:257` `def blocking_keys(etype, normalized, value)` -- Return the blocking keys that bucket an entity for comparison.
- `MatchScore.score_pair` (method) `estorides_core/entity_resolution.py:302` `def score_pair(etype, a_value, b_value, a_norm, b_norm)` -- Score how likely two same-type entities denote the same object.
- `CanonicalEntity.to_dict` (method) `estorides_core/entity_resolution.py:357` `def to_dict(self)`
- `CanonicalEntity.to_entity` (method) `estorides_core/entity_resolution.py:373` `def to_entity(self)` -- Project back onto the legacy :class:`Entity` shape.
- `SameAsLink.to_dict` (method) `estorides_core/entity_resolution.py:409` `def to_dict(self)`
- `ResolutionResult.to_dict` (method) `estorides_core/entity_resolution.py:425` `def to_dict(self)`
- `_UnionFind.__init__` (method) `estorides_core/entity_resolution.py:435` `def __init__(self, n)`
- `_UnionFind.find` (method) `estorides_core/entity_resolution.py:438` `def find(self, x)`
- `_UnionFind.union` (method) `estorides_core/entity_resolution.py:444` `def union(self, a, b)`
- `EntityResolver.__init__` (method) `estorides_core/entity_resolution.py:469` `def __init__(self)`
- `EntityResolver.resolve` (method) `estorides_core/entity_resolution.py:482` `def resolve(self, entities)` -- Resolve ``entities`` into canonical identities and links.
- `EntityResolver.rank` (method) `estorides_core/entity_resolution.py:670` `def rank(rec)`
- `EntityResolver.resolve_entities` (method) `estorides_core/entity_resolution.py:727` `def resolve_entities(entities)` -- Module-level convenience wrapper around :class:`EntityResolver`.

## estorides_core/entity_store.py
Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/sqlite_store.py`
Imported by: `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`
- `EntityStore.lookup` (method) `estorides_core/entity_store.py:66` `def lookup(self, etype, normalized, aliases)` -- Return an existing canonical id for any known form, or None.
- `EntityStore.upsert` (method) `estorides_core/entity_store.py:104` `def upsert(self, entity)` -- Persist (insert or update) a canonical entity and its aliases.
- `EntityStore.stats` (method) `estorides_core/entity_store.py:143` `def stats(self)` -- Return a one-glance summary of store size.
- `EntityStore.open_store` (method) `estorides_core/entity_store.py:155` `def open_store(path)` -- Open the store, returning None instead of raising on failure.

## estorides_core/event_bus.py
Imported by: `estorides_core/orchestrator.py`, `tests/test_event_bus.py`
- `EventBus.__init__` (method) `estorides_core/event_bus.py:27` `def __init__(self)` -- Create an empty bus with no subscribers.
- `EventBus.subscribe` (method) `estorides_core/event_bus.py:31` `def subscribe(self, event, handler)` -- Register handler for event and return it for unsubscription.
- `EventBus.unsubscribe` (method) `estorides_core/event_bus.py:41` `def unsubscribe(self, event, handler)` -- Remove handler from event and report whether it was present.
- `EventBus.publish` (method) `estorides_core/event_bus.py:50` `def publish(self, event, payload)` -- Deliver a copy of payload to each subscriber and count attempts.
- `EventBus.clear` (method) `estorides_core/event_bus.py:63` `def clear(self, event)` -- Remove subscribers for one event or for the whole bus.
- `EventBus.subscriber_count` (method) `estorides_core/event_bus.py:71` `def subscriber_count(self, event)` -- Return the number of handlers registered for event.
- `EventBus.get_bus` (method) `estorides_core/event_bus.py:85` `def get_bus()` -- Return the process wide shared bus instance.

## estorides_core/feeds.py
Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
Imported by: `estorides_web.py`
- `FeedPoint.to_dict` (method) `estorides_core/feeds.py:69` `def to_dict(self)`
- `Feed.__init__` (method) `estorides_core/feeds.py:82` `def __init__(self)`
- `Feed.fetch` (method) `estorides_core/feeds.py:90` `def fetch(self)` -- Public entrypoint.
- `Feed.point` (method) `estorides_core/feeds.py:135` `def point(self, record)` -- Default: return (lat, lon) if both present.
- `NewsFeed.list_feeds` (method) `estorides_core/feeds.py:313` `def list_feeds()` -- Return public feed descriptions for the /api/feeds endpoint.
- `NewsFeed.get_feed` (method) `estorides_core/feeds.py:321` `def get_feed(name)`
- `NewsFeed.fetch_all` (method) `estorides_core/feeds.py:325` `def fetch_all(bbox, use_cache)` -- Fetch every registered feed (optionally clipped to a bbox).

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
- `normalize_value` (method) `estorides_core/fusion_store.py:73` `def normalize_value(etype, value)`
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
- `FusionStore.open_store` (method) `estorides_core/fusion_store.py:723` `def open_store(path)` -- Open the fusion store, returning None instead of raising on failure.

## estorides_core/graph_force.py
Imported by: `estorides_web.py`, `tests/test_graph_force3d.py`
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

## estorides_core/hypothesis_engine.py
Depends on: `estorides_core/ids.py`, `estorides_core/reliability_scoring.py`
Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`
- `HypothesisGenerator.__call__` (method) `estorides_core/hypothesis_engine.py:213` `def __call__(self, observations, entities)`
- `HypothesisGenerator.generate_hypotheses` (method) `estorides_core/hypothesis_engine.py:613` `def generate_hypotheses(observations, entities, kg)` -- Generate typed, scored, auditable hypotheses for a run.

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
- `KnowledgeGraph.summary` (method) `estorides_core/knowledge_graph.py:197` `def summary(self)`
- `KnowledgeGraph.top_entities` (method) `estorides_core/knowledge_graph.py:215` `def top_entities(self, n, by)`
- `KnowledgeGraph.communities` (method) `estorides_core/knowledge_graph.py:235` `def communities(self, nodes)` -- Partition entity nodes into communities (clusters).
- `KnowledgeGraph.intel_level` (method) `estorides_core/knowledge_graph.py:266` `def intel_level(self, node_id, bridge_nodes)` -- Classify a node into the intelligence pipeline tier.
- `KnowledgeGraph.ego_subgraph` (method) `estorides_core/knowledge_graph.py:311` `def ego_subgraph(self, node_id, radius)`
- `KnowledgeGraph.neighbours` (method) `estorides_core/knowledge_graph.py:322` `def neighbours(self, node_id, relation)`

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
- `OpsConfig.health_payload` (method) `estorides_core/ops_observability.py:50` `def health_payload()` -- Return liveness body and status code.
- `OpsConfig.ready_payload` (method) `estorides_core/ops_observability.py:55` `def ready_payload(source_count, sources_dir_ok)` -- Return readiness body and status code for registry state.
- `OpsConfig.record_request` (method) `estorides_core/ops_observability.py:62` `def record_request(endpoint, status)` -- Count one HTTP response by normalized endpoint and status.
- `OpsConfig.record_source` (method) `estorides_core/ops_observability.py:72` `def record_source(source, ok)` -- Count one source execution failure when ok is False.
- `OpsConfig.reset_metrics` (method) `estorides_core/ops_observability.py:83` `def reset_metrics()` -- Clear all in memory counters for tests and process restart.
- `OpsConfig.render_metrics` (method) `estorides_core/ops_observability.py:90` `def render_metrics()` -- Render counters in Prometheus exposition text format.
- `OpsConfig.format_event` (method) `estorides_core/ops_observability.py:112` `def format_event(fields, as_json)` -- Format one log event as JSON when opted in else legacy plain text.
- `OpsConfig.project_root` (method) `estorides_core/ops_observability.py:130` `def project_root()` -- Expose project root without hardcoding absolute paths in callers.

## estorides_core/orchestrator.py
Depends on: `estorides_core/async_client.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/event_bus.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/mitre_attack.py`, `estorides_core/ontology.py`, `estorides_core/pagination.py`, `estorides_core/parsers.py`, `estorides_core/recon_fusion.py`, `estorides_core/relationship_inference.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_llm/__init__.py`
Imported by: `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_web.py`, `tests/test_central_config.py`, `tests/test_keyless_sources.py`, `tests/test_opsec_contact.py`, `tests/test_source_routing.py`, `tests/test_system_app_sources.py`
- `pending_system_app_tasks` (function) `estorides_core/orchestrator.py:56` `def pending_system_app_tasks()` -- Number of slow CLI-tool runs still in flight (for the stream gate).
- `repl` (method) `estorides_core/orchestrator.py:122` `def repl(m)`
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

## estorides_core/pagination.py
Imported by: `estorides_core/orchestrator.py`, `tests/test_pagination.py`
- `PaginationConfig.from_dict` (method) `estorides_core/pagination.py:38` `def from_dict(raw)`
- `PaginationConfig.enabled` (method) `estorides_core/pagination.py:54` `def enabled(self)`
- `PaginationConfig.needs_page_size` (method) `estorides_core/pagination.py:58` `def needs_page_size(self)`
- `PaginationConfig.build_page_params` (method) `estorides_core/pagination.py:62` `def build_page_params(cfg, page_num)` -- Build URL params dict for a given page number.
- `PaginationConfig.extract_cursor` (method) `estorides_core/pagination.py:78` `def extract_cursor(data, cfg)` -- Extract the next-page cursor from a parsed response body.
- `PaginationConfig.count_results` (method) `estorides_core/pagination.py:99` `def count_results(data, cfg)` -- Count results in a parsed response page.

## estorides_core/parsers.py
Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_parsers_properties.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_keyless_sources.py`, `tests/test_socmint.py`
- `parse_dns_json` (function) `estorides_core/parsers.py:62` `def parse_dns_json(payload)` -- Google/Cloudflare DNS-over-HTTPS response.
- `parse_crtsh_json` (function) `estorides_core/parsers.py:78` `def parse_crtsh_json(payload)` -- CT log response.
- `parse_rdap` (function) `estorides_core/parsers.py:96` `def parse_rdap(payload)` -- RDAP (RFC 7483) domain object.
- `parse_ipapi` (function) `estorides_core/parsers.py:176` `def parse_ipapi(payload)` -- ip-api.com response.
- `parse_ipinfo` (function) `estorides_core/parsers.py:202` `def parse_ipinfo(payload)`
- `parse_ipapi_co` (function) `estorides_core/parsers.py:217` `def parse_ipapi_co(payload)`
- `parse_shodan_internetdb` (function) `estorides_core/parsers.py:227` `def parse_shodan_internetdb(payload)` -- internetdb.shodan.io — IP service summary.
- `parse_greynoise` (function) `estorides_core/parsers.py:241` `def parse_greynoise(payload)`
- `parse_ipwhois` (function) `estorides_core/parsers.py:256` `def parse_ipwhois(payload)`
- `parse_abuseipdb` (function) `estorides_core/parsers.py:274` `def parse_abuseipdb(payload)`
- `parse_vt_ip` (function) `estorides_core/parsers.py:304` `def parse_vt_ip(payload)` -- VirusTotal v3 — IP address object.
- `parse_vt_domain` (function) `estorides_core/parsers.py:325` `def parse_vt_domain(payload)` -- VirusTotal v3 — domain object.
- `parse_vt_file` (function) `estorides_core/parsers.py:352` `def parse_vt_file(payload)` -- VirusTotal v3 — file object.
- `parse_bgpview` (function) `estorides_core/parsers.py:376` `def parse_bgpview(payload)` -- BGPView IP/ASN response (keyless).
- `parse_cisa_kev` (function) `estorides_core/parsers.py:408` `def parse_cisa_kev(payload)` -- CISA KEV catalog (keyless).
- `parse_ripe_stat` (function) `estorides_core/parsers.py:427` `def parse_ripe_stat(payload)`
- `parse_nominatim` (function) `estorides_core/parsers.py:438` `def parse_nominatim(payload)`
- `parse_urlscan` (function) `estorides_core/parsers.py:456` `def parse_urlscan(payload)`
- `parse_wayback_cdx` (function) `estorides_core/parsers.py:478` `def parse_wayback_cdx(payload)` -- CDX returns a list where the first row is the header.
- `parse_wayback_avail` (function) `estorides_core/parsers.py:493` `def parse_wayback_avail(payload)`
- `parse_threatfox` (function) `estorides_core/parsers.py:503` `def parse_threatfox(payload)`
- `parse_urlhaus` (function) `estorides_core/parsers.py:512` `def parse_urlhaus(payload)`
- `parse_urlhaus_payloads` (function) `estorides_core/parsers.py:521` `def parse_urlhaus_payloads(payload)`
- `parse_malwarebazaar` (function) `estorides_core/parsers.py:530` `def parse_malwarebazaar(payload)`
- `parse_otx` (function) `estorides_core/parsers.py:539` `def parse_otx(payload)`
- `parse_hibp_breach` (function) `estorides_core/parsers.py:564` `def parse_hibp_breach(payload)`
- `parse_hibp_paste` (function) `estorides_core/parsers.py:582` `def parse_hibp_paste(payload)`
- `parse_phonebook` (function) `estorides_core/parsers.py:598` `def parse_phonebook(payload)`
- `parse_wikipedia` (function) `estorides_core/parsers.py:619` `def parse_wikipedia(payload)`
- `parse_wikidata` (function) `estorides_core/parsers.py:628` `def parse_wikidata(payload)`
- `parse_openalex` (function) `estorides_core/parsers.py:640` `def parse_openalex(payload)`
- `parse_crossref` (function) `estorides_core/parsers.py:665` `def parse_crossref(payload)`
- `parse_arxiv` (function) `estorides_core/parsers.py:685` `def parse_arxiv(payload)` -- arXiv returns Atom XML; we expect callers to have converted to a dict.
- `parse_nvd_cve` (function) `estorides_core/parsers.py:706` `def parse_nvd_cve(payload)`
- `parse_github_advisories` (function) `estorides_core/parsers.py:727` `def parse_github_advisories(payload)`
- `parse_blockchain_btc` (function) `estorides_core/parsers.py:752` `def parse_blockchain_btc(payload)`
- `parse_blockstream` (function) `estorides_core/parsers.py:769` `def parse_blockstream(payload)`
- `parse_ethplorer` (function) `estorides_core/parsers.py:785` `def parse_ethplorer(payload)`
- `parse_microlink` (function) `estorides_core/parsers.py:802` `def parse_microlink(payload)`
- `parse_github_user` (function) `estorides_core/parsers.py:822` `def parse_github_user(payload)`
- `parse_github_search` (function) `estorides_core/parsers.py:842` `def parse_github_search(payload)`
- `parse_reddit` (function) `estorides_core/parsers.py:857` `def parse_reddit(payload)`
- `parse_mastodon` (function) `estorides_core/parsers.py:887` `def parse_mastodon(payload)`
- `parse_keybase` (function) `estorides_core/parsers.py:903` `def parse_keybase(payload)`
- `parse_hackernews` (function) `estorides_core/parsers.py:932` `def parse_hackernews(payload)`
- `parse_reddit_search` (function) `estorides_core/parsers.py:944` `def parse_reddit_search(payload)`
- `parse_dev_to` (function) `estorides_core/parsers.py:958` `def parse_dev_to(payload)`
- `parse_text_lines` (function) `estorides_core/parsers.py:973` `def parse_text_lines(payload)` -- Generic: split raw_text by newlines, drop empties.
- `parse_raw_text` (function) `estorides_core/parsers.py:984` `def parse_raw_text(payload)`
- `parse_http_headers` (function) `estorides_core/parsers.py:992` `def parse_http_headers(payload)` -- hackertarget returns text; expect a one-line-per-header response.
- `parse_whois_text` (function) `estorides_core/parsers.py:1008` `def parse_whois_text(payload)`
- `parse_twitter_user` (function) `estorides_core/parsers.py:1026` `def parse_twitter_user(payload)` -- Twitter/X API v2 user by username.
- `parse_youtube_user` (function) `estorides_core/parsers.py:1062` `def parse_youtube_user(payload)` -- YouTube Data API v3 channel by handle.
- `parse_twitch_user` (function) `estorides_core/parsers.py:1099` `def parse_twitch_user(payload)` -- Twitch Helix API user by login.
- `parse_discord_discovery` (function) `estorides_core/parsers.py:1132` `def parse_discord_discovery(payload)` -- Discord server discovery via discords.com API.
- `get_parser` (function) `estorides_core/parsers.py:1251` `def get_parser(name)` -- Return the parser function for `name`, or a passthrough lambda.
- `register_parser` (function) `estorides_core/parsers.py:1264` `def register_parser(name, description)` -- Decorator: register `func` as a parser under `name`.
- `deco` (function) `estorides_core/parsers.py:1272` `def deco(func)`
- `list_parsers` (function) `estorides_core/parsers.py:1280` `def list_parsers()` -- Return (name, description) tuples for every registered parser.

## estorides_core/pdns_monitor.py
Imported by: `estorides_core/recon_pipeline.py`, `tests/test_pdns_monitor.py`
- `HistoricalSubdomain.to_dict` (method) `estorides_core/pdns_monitor.py:22` `def to_dict(self)`
- `IPRecord.to_dict` (method) `estorides_core/pdns_monitor.py:35` `def to_dict(self)`
- `CertRecord.to_dict` (method) `estorides_core/pdns_monitor.py:50` `def to_dict(self)`
- `PDNSResult.to_dict` (method) `estorides_core/pdns_monitor.py:62` `def to_dict(self)`
- `PDNSResult.classify_subdomain_status` (method) `estorides_core/pdns_monitor.py:72` `def classify_subdomain_status(fqdn, resolved_ips)`
- `PDNSResult.extract_sans_from_cert` (method) `estorides_core/pdns_monitor.py:76` `def extract_sans_from_cert(cert)`
- `PDNSResult.analyse_pdns_data` (method) `estorides_core/pdns_monitor.py:80` `def analyse_pdns_data(subdomains, ip_history, new_certs)`


Next: [API_p2.md](API_p2.md)
