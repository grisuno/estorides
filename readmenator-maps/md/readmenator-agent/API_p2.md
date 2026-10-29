# API (page 2 of 3)
Previous: [API.md](API.md)

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

## estorides_core/pagination.py
Imported by: `estorides_core/orchestrator.py`, `tests/test_pagination.py`
- `PaginationConfig.from_dict` (method) `estorides_core/pagination.py:38` `def from_dict(raw)`
- `PaginationConfig.enabled` (method) `estorides_core/pagination.py:54` `def enabled(self)`
- `PaginationConfig.needs_page_size` (method) `estorides_core/pagination.py:58` `def needs_page_size(self)`
- `build_page_params` (function) `estorides_core/pagination.py:62` `def build_page_params(cfg, page_num)` -- Build URL params dict for a given page number.
- `extract_cursor` (function) `estorides_core/pagination.py:78` `def extract_cursor(data, cfg)` -- Extract the next-page cursor from a parsed response body.
- `count_results` (function) `estorides_core/pagination.py:99` `def count_results(data, cfg)` -- Count results in a parsed response page.

## estorides_core/parsers.py
Depends on: `estorides_core/aerospace.py`, `estorides_core/aviation.py`
Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_parsers_properties.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_aerospace.py`, `tests/test_keyless_sources.py`, `tests/test_socmint.py`
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
- `parse_celestrak_tle` (function) `estorides_core/parsers.py:1168` `def parse_celestrak_tle(payload)` -- CelesTrak GP three-line TLE catalog (text or ``{"raw_text": ...}``).
- `parse_opensky_states` (function) `estorides_core/parsers.py:1176` `def parse_opensky_states(payload)` -- OpenSky Network state vectors -> common aircraft records.
- `parse_adsblol_aircraft` (function) `estorides_core/parsers.py:1184` `def parse_adsblol_aircraft(payload)` -- adsb.lol v2 aircraft snapshot -> common aircraft records.
- `parse_opensky_track` (function) `estorides_core/parsers.py:1192` `def parse_opensky_track(payload)` -- OpenSky Network aircraft track with waypoints.
- `parse_adsbdb` (function) `estorides_core/parsers.py:1199` `def parse_adsbdb(payload)` -- adsbdb aircraft or callsign flight route.
- `parse_launch_library` (function) `estorides_core/parsers.py:1206` `def parse_launch_library(payload)` -- Launch Library 2 launches with pad coordinates when present.
- `parse_hexdb_aircraft` (function) `estorides_core/parsers.py:1214` `def parse_hexdb_aircraft(payload)` -- hexdb.io aircraft record by ICAO address (registration, type, owner).
- `parse_hexdb_route` (function) `estorides_core/parsers.py:1222` `def parse_hexdb_route(payload)` -- hexdb.io flight route by callsign (origin and destination).
- `get_parser` (function) `estorides_core/parsers.py:1322` `def get_parser(name)` -- Return the parser function for `name`, or a passthrough lambda.
- `register_parser` (function) `estorides_core/parsers.py:1335` `def register_parser(name, description)` -- Decorator: register `func` as a parser under `name`.
- `deco` (function) `estorides_core/parsers.py:1343` `def deco(func)`
- `list_parsers` (function) `estorides_core/parsers.py:1351` `def list_parsers()` -- Return (name, description) tuples for every registered parser.

## estorides_core/pdns_monitor.py
Imported by: `estorides_core/recon_pipeline.py`, `tests/test_pdns_monitor.py`
- `HistoricalSubdomain.to_dict` (method) `estorides_core/pdns_monitor.py:22` `def to_dict(self)`
- `IPRecord.to_dict` (method) `estorides_core/pdns_monitor.py:35` `def to_dict(self)`
- `CertRecord.to_dict` (method) `estorides_core/pdns_monitor.py:50` `def to_dict(self)`
- `PDNSResult.to_dict` (method) `estorides_core/pdns_monitor.py:62` `def to_dict(self)`
- `classify_subdomain_status` (function) `estorides_core/pdns_monitor.py:72` `def classify_subdomain_status(fqdn, resolved_ips)`
- `extract_sans_from_cert` (function) `estorides_core/pdns_monitor.py:76` `def extract_sans_from_cert(cert)`
- `analyse_pdns_data` (function) `estorides_core/pdns_monitor.py:80` `def analyse_pdns_data(subdomains, ip_history, new_certs)`

## estorides_core/people_intel.py
Imported by: `estorides_core/recon_pipeline.py`, `tests/test_people_intel.py`
- `BreachRecord.to_dict` (method) `estorides_core/people_intel.py:22` `def to_dict(self)`
- `Employee.to_dict` (method) `estorides_core/people_intel.py:40` `def to_dict(self)`
- `BreachContext.to_dict` (method) `estorides_core/people_intel.py:62` `def to_dict(self)`
- `PeopleIntelResult.to_dict` (method) `estorides_core/people_intel.py:75` `def to_dict(self)`
- `infer_email_pattern` (function) `estorides_core/people_intel.py:98` `def infer_email_pattern(emails)`
- `correlate_breaches` (function) `estorides_core/people_intel.py:153` `def correlate_breaches(employees)`
- `analyse_employees` (function) `estorides_core/people_intel.py:176` `def analyse_employees(employees, domain)`

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
- `register_inferer` (function) `estorides_core/relationship_inference.py:63` `def register_inferer(source_name)` -- Decorator: register `func` as the inferer for `source_name`.
- `deco` (function) `estorides_core/relationship_inference.py:70` `def deco(func)`
- `infer_relationship` (function) `estorides_core/relationship_inference.py:78` `def infer_relationship(observation, query, kg)` -- Dispatch an observation to its inferer (if any).

## estorides_core/reliability_scoring.py
Imported by: `estorides_core/change_detection.py`, `estorides_core/fusion_store.py`, `estorides_core/hypothesis_engine.py`, `estorides_core/recon_fusion.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/test_change_detection.py`, `tests/test_hypothesis_engine.py`, `tests/test_reliability_scoring.py`
- `compute_confidence` (function) `estorides_core/reliability_scoring.py:312` `def compute_confidence(inp)` -- Compute the audit-trailed confidence score for one observation.
- `merge_confidence` (function) `estorides_core/reliability_scoring.py:350` `def merge_confidence(existing, new_observation)` -- Merge a new observation's confidence into an existing entity score.
- `reliability_from_name` (function) `estorides_core/reliability_scoring.py:400` `def reliability_from_name(source_name)` -- Look up the reliability for a source by name; never raises.
- `source_type_from_name` (function) `estorides_core/reliability_scoring.py:415` `def source_type_from_name(source_name)` -- Look up the source type hierarchy for a source by name; never raises.
- `reliability_weight` (function) `estorides_core/reliability_scoring.py:430` `def reliability_weight(source_name, overrides)` -- Numeric reliability weight for a source name; never raises.
- `reliability_weight_for_letter` (function) `estorides_core/reliability_scoring.py:452` `def reliability_weight_for_letter(letter)` -- Numeric weight for a reliability letter (A-F); never raises.

## estorides_core/scope.py
Imported by: `estorides_cli.py`, `static/js/estorides.js`, `tests/test_scope.py`
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
- `parse_rule` (function) `estorides_core/scope.py:211` `def parse_rule(line)` -- Parse one rule line into a ScopeRule, or None for blank/comment/invalid.
- `parse_rules` (function) `estorides_core/scope.py:223` `def parse_rules(lines)` -- Parse many rule lines, skipping blanks, comments and invalid entries.
- `ScopeMatcher.__init__` (method) `estorides_core/scope.py:242` `def __init__(self, in_scope, out_of_scope)`
- `ScopeMatcher.in_rules` (method) `estorides_core/scope.py:251` `def in_rules(self)`
- `ScopeMatcher.out_rules` (method) `estorides_core/scope.py:255` `def out_rules(self)`
- `ScopeMatcher.classify` (method) `estorides_core/scope.py:258` `def classify(self, raw_asset)` -- Return IN_SCOPE, OUT_OF_SCOPE or UNKNOWN for a single asset.
- `ScopeMatcher.partition` (method) `estorides_core/scope.py:269` `def partition(self, assets)` -- Bucket many assets, returning sorted, de-duplicated lists.
- `load_rules_file` (function) `estorides_core/scope.py:285` `def load_rules_file(path)` -- Build a matcher from a rules file, honouring the out-of-scope divider.
- `load_assets` (function) `estorides_core/scope.py:303` `def load_assets(path)` -- Read assets from a file: a discover surface JSON or a flat host list.
- `ScopeReport.hosts` (method) `estorides_core/scope.py:352` `def hosts(self)` -- In-scope hostnames (everything in-scope that is not an IP).
- `ScopeReport.ips` (method) `estorides_core/scope.py:357` `def ips(self)` -- In-scope bare IP addresses.
- `ScopeReport.to_dict` (method) `estorides_core/scope.py:361` `def to_dict(self)`
- `build_report` (function) `estorides_core/scope.py:371` `def build_report(matcher, assets)` -- Classify `assets` with `matcher` and return a :class:`ScopeReport`.
- `write_flat_lists` (function) `estorides_core/scope.py:381` `def write_flat_lists(report, out_dir)` -- Write newline-delimited flat lists for piping into active tooling.

## estorides_core/search_telemetry.py
Depends on: `estorides_core/config.py`
Imported by: `estorides_web.py`, `tests/properties/test_search_telemetry_properties.py`, `tests/test_csp_safe_styles.py`, `tests/test_search_telemetry.py`, `tests/test_ui_professional.py`
- `disallowed_brands_in` (function) `estorides_core/search_telemetry.py:75` `def disallowed_brands_in(text)` -- Return the third-party brand tokens found in ``text``.
- `emoji_in` (function) `estorides_core/search_telemetry.py:89` `def emoji_in(text)` -- Return the emoji glyphs found in ``text``, de-duplicated in order.
- `percent_encoded_emoji_in` (function) `estorides_core/search_telemetry.py:103` `def percent_encoded_emoji_in(text)` -- Return percent-encoded supplementary-plane emoji sequences in ``text``.
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
- `compute_health` (function) `estorides_core/source_health_monitoring.py:235` `def compute_health(inp, config)` -- Compute the health assessment for a single source.
- `build_dashboard` (function) `estorides_core/source_health_monitoring.py:295` `def build_dashboard(records, config)` -- Build a health dashboard from per-source health inputs.

## estorides_core/source_loader.py
Depends on: `estorides_core/config.py`
Imported by: `estorides_core/orchestrator.py`, `tests/test_aerospace.py`, `tests/test_monitoring.py`, `tests/test_opsec_contact.py`, `tests/test_socmint.py`, `tests/test_source_loader.py`, `tests/test_system_app_sources.py`
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
- `DictMixin.to_dict` (method) `estorides_core/sqlite_store.py:112` `def to_dict(self)`

## estorides_core/ssrf_guard.py
Imported by: `estorides_core/alerter.py`, `estorides_core/async_client.py`, `estorides_core/feeds.py`, `estorides_core/intel_resolver.py`, `estorides_core/ontology.py`, `estorides_core/osiris_sources.py`, `tests/test_security_remediation.py`
- `check_url` (function) `estorides_core/ssrf_guard.py:194` `def check_url(url)` -- Validate a URL for outbound fetch.
- `assert_safe` (function) `estorides_core/ssrf_guard.py:262` `def assert_safe(url)` -- Raise SSRFError if `url` is not safe to fetch.

## estorides_core/supply_chain.py
Imported by: `estorides_core/recon_pipeline.py`, `tests/test_supply_chain.py`
- `ThirdParty.to_dict` (method) `estorides_core/supply_chain.py:61` `def to_dict(self)`
- `SharedInfra.to_dict` (method) `estorides_core/supply_chain.py:73` `def to_dict(self)`
- `Relationship.to_dict` (method) `estorides_core/supply_chain.py:84` `def to_dict(self)`
- `SupplyChainResult.to_dict` (method) `estorides_core/supply_chain.py:96` `def to_dict(self)`
- `detect_mx_provider` (function) `estorides_core/supply_chain.py:106` `def detect_mx_provider(mx_records)`
- `detect_ns_provider` (function) `estorides_core/supply_chain.py:114` `def detect_ns_provider(ns_records)`
- `detect_cdn` (function) `estorides_core/supply_chain.py:122` `def detect_cdn(cname)`
- `analyse_third_parties` (function) `estorides_core/supply_chain.py:129` `def analyse_third_parties(third_parties, subsidiaries)`
- `detect_shared_infrastructure` (function) `estorides_core/supply_chain.py:140` `def detect_shared_infrastructure(asn)`

## estorides_core/system_app_sources.py
Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`
- `SystemAppResult.to_dict` (method) `estorides_core/system_app_sources.py:76` `def to_dict(self)`
- `is_system_app` (function) `estorides_core/system_app_sources.py:81` `def is_system_app(source)` -- True when a source dict is a system_app (or has a binary tool).
- `tool_available` (function) `estorides_core/system_app_sources.py:91` `def tool_available(binary)` -- Resolve a binary on the filesystem (shutil.which).
- `render_args` (function) `estorides_core/system_app_sources.py:96` `def render_args(args, query, outdir)` -- Substitute ``{query}``/``{outdir}`` placeholders in an args template.
- `repl` (function) `estorides_core/system_app_sources.py:109` `def repl(m)`
- `parser` (function) `estorides_core/system_app_sources.py:165` `def parser(payload)`
- `parse_amass_json` (function) `estorides_core/system_app_sources.py:193` `def parse_amass_json(payload)` -- amass ``-json`` output: one JSON object per line (DNS + infra).
- `parse_maigret_json` (function) `estorides_core/system_app_sources.py:225` `def parse_maigret_json(payload)` -- maigret ``--json simple``: one object keyed by site name.
- `parse_phoneinfoga_json` (function) `estorides_core/system_app_sources.py:247` `def parse_phoneinfoga_json(payload)` -- phoneinfoga v2 ``scan``: a single JSON object (possibly after logs).
- `parse_sherlock_text` (function) `estorides_core/system_app_sources.py:260` `def parse_sherlock_text(payload)`
- `parse_holehe_text` (function) `estorides_core/system_app_sources.py:265` `def parse_holehe_text(payload)`
- `parse_wafw00f_text` (function) `estorides_core/system_app_sources.py:270` `def parse_wafw00f_text(payload)`
- `parse_sublist3r_lines` (function) `estorides_core/system_app_sources.py:275` `def parse_sublist3r_lines(payload)`
- `parse_dnsrecon_text` (function) `estorides_core/system_app_sources.py:280` `def parse_dnsrecon_text(payload)`
- `parse_dnsenum_text` (function) `estorides_core/system_app_sources.py:285` `def parse_dnsenum_text(payload)`
- `parse_fierce_text` (function) `estorides_core/system_app_sources.py:292` `def parse_fierce_text(payload)`
- `parse_dmitry_text` (function) `estorides_core/system_app_sources.py:297` `def parse_dmitry_text(payload)`
- `parse_urlcrazy_text` (function) `estorides_core/system_app_sources.py:302` `def parse_urlcrazy_text(payload)`
- `parse_metagoofil_text` (function) `estorides_core/system_app_sources.py:307` `def parse_metagoofil_text(payload)`
- `parse_whatweb_text` (function) `estorides_core/system_app_sources.py:312` `def parse_whatweb_text(payload)`
- `parse_theharvester_text` (function) `estorides_core/system_app_sources.py:317` `def parse_theharvester_text(payload)`
- `parse_usufy_text` (function) `estorides_core/system_app_sources.py:322` `def parse_usufy_text(payload)`
- `parse_mailfy_text` (function) `estorides_core/system_app_sources.py:327` `def parse_mailfy_text(payload)`
- `parse_phonefy_text` (function) `estorides_core/system_app_sources.py:332` `def parse_phonefy_text(payload)`
- `parse_searchfy_text` (function) `estorides_core/system_app_sources.py:337` `def parse_searchfy_text(payload)`
- `parse_tool_output` (function) `estorides_core/system_app_sources.py:365` `def parse_tool_output(source_name, parser_name, data)` -- Parse tool output with the declared parser; never raises.
- `execute` (function) `estorides_core/system_app_sources.py:396` `def execute(source, query)` -- Execute one system_app source through the tool_runner sandbox.
- `fail` (function) `estorides_core/system_app_sources.py:418` `def fail(code, message)`

## estorides_core/tech_fingerprint.py
Imported by: `estorides_core/recon_pipeline.py`, `tests/test_tech_fingerprint.py`
- `Tech.to_dict` (method) `estorides_core/tech_fingerprint.py:97` `def to_dict(self)`
- `TechFingerprintResult.to_dict` (method) `estorides_core/tech_fingerprint.py:107` `def to_dict(self)`
- `fingerprint` (function) `estorides_core/tech_fingerprint.py:115` `def fingerprint(headers, html, cookies, status)`

## estorides_core/tool_install.py
Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
Imported by: `estorides_web_tools.py`, `tests/test_central_config.py`, `tests/test_tool_doctor.py`, `tests/test_tool_install.py`
- `InstallRecipe.has_apt` (method) `estorides_core/tool_install.py:95` `def has_apt(self)`
- `InstallRecipe.has_git` (method) `estorides_core/tool_install.py:98` `def has_git(self)`
- `InstallResult.to_dict` (method) `estorides_core/tool_install.py:113` `def to_dict(self)`
- `is_valid_recipe_name` (function) `estorides_core/tool_install.py:169` `def is_valid_recipe_name(name)` -- True when ``name`` is a safe recipe/tool identifier (no separators).
- `is_valid_binary` (function) `estorides_core/tool_install.py:174` `def is_valid_binary(name)` -- True when ``name`` is a plausible bare binary name (no path).
- `load_recipe` (function) `estorides_core/tool_install.py:210` `def load_recipe(name)` -- Load a tool recipe from ``tool_recipes/<name>.yaml`` (or ``None``).
- `recipe_available` (function) `estorides_core/tool_install.py:254` `def recipe_available(name)` -- True when a recipe exists for ``name`` (the UI gates the button on this).
- `tool_available` (function) `estorides_core/tool_install.py:259` `def tool_available(binary)` -- True when the binary resolves on PATH (mirrors system_app_sources).
- `list_recipes` (function) `estorides_core/tool_install.py:270` `def list_recipes()` -- Names of all tool recipe files in ``tool_recipes/`` (sorted).
- `ToolStatus.to_dict` (method) `estorides_core/tool_install.py:287` `def to_dict(self)`
- `doctor` (function) `estorides_core/tool_install.py:321` `def doctor(sources_dir)` -- Read-only readiness report over system_app binaries + recipes.
- `install_tool` (function) `estorides_core/tool_install.py:414` `def install_tool(tool_name)` -- Install a missing tool from its recipe (if any).
- `main` (function) `estorides_core/tool_install.py:516` `def main(argv)` -- Minimal CLI: ``python -m estorides_core.tool_install <tool> [--force]``.

## estorides_core/tool_runner.py
Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
Imported by: `estorides_core/active_recon.py`, `estorides_core/lan_runner.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/properties/test_tool_runner_properties.py`, `tests/test_active_recon.py`, `tests/test_lan_runner.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`
- `ToolResult.to_dict` (method) `estorides_core/tool_runner.py:51` `def to_dict(self)`
- `ToolResult.from_failure` (method) `estorides_core/tool_runner.py:59` `def from_failure(cls, tool_name, error_code, error_message, duration_s, exit_code, stdout, stderr, parsed_entities)`
- `ToolErrorResult.to_dict` (method) `estorides_core/tool_runner.py:93` `def to_dict(self)`
- `run_tool` (function) `estorides_core/tool_runner.py:156` `def run_tool(tool_name, args, target, timeout, max_output_bytes, cwd)`

## estorides_core/transforms.py
Depends on: `estorides_core/config.py`, `estorides_core/intel_resolver.py`
Imported by: `estorides_web.py`, `tests/test_transforms.py`
- `Transform.summary` (method) `estorides_core/transforms.py:85` `def summary(self)`
- `run` (function) `estorides_core/transforms.py:124` `def run(ent_type, value)`
- `TransformRegistry.__init__` (method) `estorides_core/transforms.py:230` `def __init__(self)`
- `TransformRegistry.register` (method) `estorides_core/transforms.py:233` `def register(self, t)`
- `TransformRegistry.for_type` (method) `estorides_core/transforms.py:236` `def for_type(self, ent_type)`
- `TransformRegistry.run` (method) `estorides_core/transforms.py:248` `def run(self, transform_id, ent_type, value)`
- `TransformRegistry.load_yaml_dir` (method) `estorides_core/transforms.py:282` `def load_yaml_dir(self, directory)` -- Register every transform declared in ``*.yaml`` under `directory`.
- `run` (function) `estorides_core/transforms.py:337` `def run(ent_type, value)`
- `sub` (function) `estorides_core/transforms.py:340` `def sub(s, depth)`
- `iter_sse_events` (function) `estorides_core/transforms.py:408` `def iter_sse_events(transform_id, ent_type, value, runner)` -- Yield ``(kind, payload)`` tuples for the SSE stream endpoint.

## estorides_core/transliteration.py
Imported by: `estorides_core/entity_resolution.py`, `tests/test_entity_resolution.py`
- `to_latin` (function) `estorides_core/transliteration.py:87` `def to_latin(text)` -- Return a lowercased, diacritic-free Latin transliteration.
- `consonant_skeleton` (function) `estorides_core/transliteration.py:112` `def consonant_skeleton(text)` -- Return the Latin transliteration with vowels and spaces removed.
- `is_non_latin` (function) `estorides_core/transliteration.py:139` `def is_non_latin(text)` -- True if any character is outside the Basic Latin / Latin-1 range.

## estorides_core/validation.py
Depends on: `estorides_core/entity_extraction.py`
Imported by: `estorides_cli.py`, `estorides_web.py`, `tests/test_tool_runner.py`
- `QueryValidationError.__init__` (method) `estorides_core/validation.py:57` `def __init__(self, reason, message)`
- `validate_query` (function) `estorides_core/validation.py:85` `def validate_query(raw)` -- Validate and normalise a user query string.

## estorides_core/vuln_correlation.py
Imported by: `estorides_core/recon_pipeline.py`, `tests/test_vuln_correlation.py`
- `DefaultCred.to_dict` (method) `estorides_core/vuln_correlation.py:19` `def to_dict(self)`
- `VulnEntry.to_dict` (method) `estorides_core/vuln_correlation.py:38` `def to_dict(self)`
- `VulnCorrelationResult.to_dict` (method) `estorides_core/vuln_correlation.py:52` `def to_dict(self)`
- `lookup_cve_for_tech` (function) `estorides_core/vuln_correlation.py:169` `def lookup_cve_for_tech(tech_name, version)`
- `correlate_technologies` (function) `estorides_core/vuln_correlation.py:202` `def correlate_technologies(technologies)`
- `compute_attack_readiness` (function) `estorides_core/vuln_correlation.py:228` `def compute_attack_readiness(vulnerabilities)`

## estorides_core/web_security.py
Imported by: `estorides_web.py`, `estorides_web_tools.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_hardening.py`, `tests/test_map_basemap.py`, `tests/test_security_remediation.py`, `tests/test_web_helpers.py`
- `build_https_url` (function) `estorides_core/web_security.py:58` `def build_https_url(public_host, path, query_string)` -- Build a safe HTTPS redirect target from a trusted host and client path.
- `WebSecurityConfig.is_cors_enabled` (method) `estorides_core/web_security.py:128` `def is_cors_enabled(self)`
- `WebSecurityConfig.is_origin_allowed` (method) `estorides_core/web_security.py:132` `def is_origin_allowed(self)` -- CORS is opt-in; this is the runtime check used by the after_request hook.
- `load_security_config` (function) `estorides_core/web_security.py:144` `def load_security_config()` -- Resolve the security policy from env vars.
- `install_security` (function) `estorides_core/web_security.py:169` `def install_security(app, cfg)` -- Wire security middleware into a Flask app.
- `make_auth_gate` (function) `estorides_core/web_security.py:321` `def make_auth_gate()` -- Build the auth gate from the current environment.
- `AuthGate.enabled` (method) `estorides_core/web_security.py:351` `def enabled(self)`
- `AuthGate.check` (method) `estorides_core/web_security.py:354` `def check(self)`
- `AuthGate.auth_meta_for_index` (method) `estorides_core/web_security.py:362` `def auth_meta_for_index(self)` -- Token to embed in `index.html` so the UI can auto-authenticate.
- `AuthGate.issue_session_cookie_kwargs` (method) `estorides_core/web_security.py:371` `def issue_session_cookie_kwargs(self)` -- Arguments for `set_cookie` to install the session cookie.
- `require_auth` (function) `estorides_core/web_security.py:388` `def require_auth(view)` -- Decorator: enforce the bearer-token gate on a view.
- `wrapper` (function) `estorides_core/web_security.py:402` `def wrapper()`
- `install_auth_gate` (function) `estorides_core/web_security.py:421` `def install_auth_gate(app, gate)` -- Attach the gate to a Flask app and a module-level slot.
- `auto_generated_token` (function) `estorides_core/web_security.py:444` `def auto_generated_token()` -- Return the auto-generated token (None if user set ESTORIDES_AUTH_TOKEN manually).

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
- `redact_sensitive` (function) `estorides_export/recon_report.py:61` `def redact_sensitive(text)`
- `build_subdomain_tree` (function) `estorides_export/recon_report.py:67` `def build_subdomain_tree(subdomains)`
- `build_executive_summary` (function) `estorides_export/recon_report.py:92` `def build_executive_summary(critical_findings, total_targets, domain, classification)`
- `generate_report` (function) `estorides_export/recon_report.py:115` `def generate_report(query, target_scoring, metadata)`

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
- `register` (function) `estorides_llm/manager.py:97` `def register(name)` -- Decorator: register a backend under `name`.
- `deco` (function) `estorides_llm/manager.py:105` `def deco(backend_or_cls)`
- `OllamaBackend.get_status` (method) `estorides_llm/manager.py:124` `def get_status()` -- Return available ollama models and reachability status.
- `OllamaBackend.stream_generate` (method) `estorides_llm/manager.py:188` `def stream_generate(self, prompt, context, model, temperature, request_timeout)` -- Stream an ollama response as (kind, text) chunks.
- `OllamaBackend.__call__` (method) `estorides_llm/manager.py:227` `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- `_OpenAICompatibleBackend.__call__` (method) `estorides_llm/manager.py:274` `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- `AnthropicBackend.__call__` (method) `estorides_llm/manager.py:319` `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- `LLMManager.__init__` (method) `estorides_llm/manager.py:357` `def __init__(self)`
- `LLMManager.generate` (method) `estorides_llm/manager.py:373` `def generate(self, prompt)` -- Try each backend in priority order; return the first that succeeds.
- `LLMManager.get_ollama_status` (method) `estorides_llm/manager.py:414` `def get_ollama_status(self)` -- Return ollama reachability and available models.
- `LLMManager.stream` (method) `estorides_llm/manager.py:422` `def stream(self, prompt)` -- Stream an analysis from a specific ollama model.


Next: [API_p3.md](API_p3.md)
