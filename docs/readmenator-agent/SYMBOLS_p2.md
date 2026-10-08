# Symbols (page 2 of 6)
Previous: [SYMBOLS.md](SYMBOLS.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `ready_payload` | method | `estorides_core/ops_observability.py:55` | `def ready_payload(source_count, sources_dir_ok)` |
| `record_request` | method | `estorides_core/ops_observability.py:62` | `def record_request(endpoint, status)` |
| `record_source` | method | `estorides_core/ops_observability.py:72` | `def record_source(source, ok)` |
| `render_metrics` | method | `estorides_core/ops_observability.py:90` | `def render_metrics()` |
| `reset_metrics` | method | `estorides_core/ops_observability.py:83` | `def reset_metrics()` |
| `Orchestrator` | class | `estorides_core/orchestrator.py:168` | `class Orchestrator` |
| `__init__` | method | `estorides_core/orchestrator.py:169` | `def __init__(self, registry, llm, kg)` |
| `_domain_from_query` | function | `estorides_core/orchestrator.py:158` | `def _domain_from_query(q)` |
| `_execute_source` | method | `estorides_core/orchestrator.py:707` | `def _execute_source(self, client, source, query, on_done, on_result)` |
| `_expand_query_type` | function | `estorides_core/orchestrator.py:152` | `def _expand_query_type(query_type)` |
| `_extract_cursor` | method | `estorides_core/orchestrator.py:953` | `def _extract_cursor(data, cfg)` |
| `_infer_relationships` | method | `estorides_core/orchestrator.py:958` | `def _infer_relationships(self, observations, query)` |
| `_normalise_results` | method | `estorides_core/orchestrator.py:724` | `def _normalise_results(self, raw_results, targets)` |
| `_resolve_auth` | function | `estorides_core/orchestrator.py:127` | `def _resolve_auth(source)` |
| `_run_http_source` | method | `estorides_core/orchestrator.py:841` | `def _run_http_source(self, client, source, query, on_done, on_result)` |
| `_run_system_app` | method | `estorides_core/orchestrator.py:774` | `def _run_system_app(self, source, query, on_done, on_result)` |
| `_safe_format` | function | `estorides_core/orchestrator.py:115` | `def _safe_format(template)` |
| `_select_sources` | method | `estorides_core/orchestrator.py:671` | `def _select_sources(self, names)` |
| `_source_of` | method | `estorides_core/orchestrator.py:764` | `def _source_of(item, fallback, raw)` |
| `_write_dataset` | method | `estorides_core/orchestrator.py:971` | `def _write_dataset(self, query, observations, entities, analysis)` |
| `pending_system_app_tasks` | function | `estorides_core/orchestrator.py:56` | `def pending_system_app_tasks()` |
| `repl` | method | `estorides_core/orchestrator.py:122` | `def repl(m)` |
| `run` | method | `estorides_core/orchestrator.py:190` | `def run(self, query)` |
| `_cached_get` | function | `estorides_core/osiris_sources.py:81` | `def _cached_get(url)` |
| `fetch_bgp` | function | `estorides_core/osiris_sources.py:119` | `def fetch_bgp(query)` |
| `fetch_cisa_kev` | function | `estorides_core/osiris_sources.py:400` | `def fetch_cisa_kev(limit, days)` |
| `fetch_github_user` | function | `estorides_core/osiris_sources.py:302` | `def fetch_github_user(username)` |
| `fetch_leaks` | function | `estorides_core/osiris_sources.py:356` | `def fetch_leaks(email)` |
| `fetch_mac` | function | `estorides_core/osiris_sources.py:185` | `def fetch_mac(mac)` |
| `fetch_malware_c2` | function | `estorides_core/osiris_sources.py:452` | `def fetch_malware_c2(limit)` |
| `fetch_phone` | function | `estorides_core/osiris_sources.py:233` | `def fetch_phone(number)` |
| `PaginationConfig` | class | `estorides_core/pagination.py:19` | `class PaginationConfig` |
| `build_page_params` | method | `estorides_core/pagination.py:62` | `def build_page_params(cfg, page_num)` |
| `count_results` | method | `estorides_core/pagination.py:99` | `def count_results(data, cfg)` |
| `enabled` | method | `estorides_core/pagination.py:54` | `def enabled(self)` |
| `extract_cursor` | method | `estorides_core/pagination.py:78` | `def extract_cursor(data, cfg)` |
| `from_dict` | method | `estorides_core/pagination.py:38` | `def from_dict(raw)` |
| `needs_page_size` | method | `estorides_core/pagination.py:58` | `def needs_page_size(self)` |
| `_d` | function | `estorides_core/parsers.py:31` | `def _d(obj)` |
| `_first_dict` | function | `estorides_core/parsers.py:40` | `def _first_dict(items)` |
| `_list` | function | `estorides_core/parsers.py:47` | `def _list(obj)` |
| `_normalise_discord_server` | function | `estorides_core/parsers.py:1152` | `def _normalise_discord_server(raw)` |
| `_text` | function | `estorides_core/parsers.py:56` | `def _text(obj)` |
| `_vt_stats` | function | `estorides_core/parsers.py:290` | `def _vt_stats(attrs)` |
| `deco` | function | `estorides_core/parsers.py:1272` | `def deco(func)` |
| `get_parser` | function | `estorides_core/parsers.py:1251` | `def get_parser(name)` |
| `list_parsers` | function | `estorides_core/parsers.py:1280` | `def list_parsers()` |
| `parse_abuseipdb` | function | `estorides_core/parsers.py:274` | `def parse_abuseipdb(payload)` |
| `parse_arxiv` | function | `estorides_core/parsers.py:685` | `def parse_arxiv(payload)` |
| `parse_bgpview` | function | `estorides_core/parsers.py:376` | `def parse_bgpview(payload)` |
| `parse_blockchain_btc` | function | `estorides_core/parsers.py:752` | `def parse_blockchain_btc(payload)` |
| `parse_blockstream` | function | `estorides_core/parsers.py:769` | `def parse_blockstream(payload)` |
| `parse_cisa_kev` | function | `estorides_core/parsers.py:408` | `def parse_cisa_kev(payload)` |
| `parse_crossref` | function | `estorides_core/parsers.py:665` | `def parse_crossref(payload)` |
| `parse_crtsh_json` | function | `estorides_core/parsers.py:78` | `def parse_crtsh_json(payload)` |
| `parse_dev_to` | function | `estorides_core/parsers.py:958` | `def parse_dev_to(payload)` |
| `parse_discord_discovery` | function | `estorides_core/parsers.py:1132` | `def parse_discord_discovery(payload)` |
| `parse_dns_json` | function | `estorides_core/parsers.py:62` | `def parse_dns_json(payload)` |
| `parse_ethplorer` | function | `estorides_core/parsers.py:785` | `def parse_ethplorer(payload)` |
| `parse_github_advisories` | function | `estorides_core/parsers.py:727` | `def parse_github_advisories(payload)` |
| `parse_github_search` | function | `estorides_core/parsers.py:842` | `def parse_github_search(payload)` |
| `parse_github_user` | function | `estorides_core/parsers.py:822` | `def parse_github_user(payload)` |
| `parse_greynoise` | function | `estorides_core/parsers.py:241` | `def parse_greynoise(payload)` |
| `parse_hackernews` | function | `estorides_core/parsers.py:932` | `def parse_hackernews(payload)` |
| `parse_hibp_breach` | function | `estorides_core/parsers.py:564` | `def parse_hibp_breach(payload)` |
| `parse_hibp_paste` | function | `estorides_core/parsers.py:582` | `def parse_hibp_paste(payload)` |
| `parse_http_headers` | function | `estorides_core/parsers.py:992` | `def parse_http_headers(payload)` |
| `parse_ipapi` | function | `estorides_core/parsers.py:176` | `def parse_ipapi(payload)` |
| `parse_ipapi_co` | function | `estorides_core/parsers.py:217` | `def parse_ipapi_co(payload)` |
| `parse_ipinfo` | function | `estorides_core/parsers.py:202` | `def parse_ipinfo(payload)` |
| `parse_ipwhois` | function | `estorides_core/parsers.py:256` | `def parse_ipwhois(payload)` |
| `parse_keybase` | function | `estorides_core/parsers.py:903` | `def parse_keybase(payload)` |
| `parse_malwarebazaar` | function | `estorides_core/parsers.py:530` | `def parse_malwarebazaar(payload)` |
| `parse_mastodon` | function | `estorides_core/parsers.py:887` | `def parse_mastodon(payload)` |
| `parse_microlink` | function | `estorides_core/parsers.py:802` | `def parse_microlink(payload)` |
| `parse_nominatim` | function | `estorides_core/parsers.py:438` | `def parse_nominatim(payload)` |
| `parse_nvd_cve` | function | `estorides_core/parsers.py:706` | `def parse_nvd_cve(payload)` |
| `parse_openalex` | function | `estorides_core/parsers.py:640` | `def parse_openalex(payload)` |
| `parse_otx` | function | `estorides_core/parsers.py:539` | `def parse_otx(payload)` |
| `parse_phonebook` | function | `estorides_core/parsers.py:598` | `def parse_phonebook(payload)` |
| `parse_raw_text` | function | `estorides_core/parsers.py:984` | `def parse_raw_text(payload)` |
| `parse_rdap` | function | `estorides_core/parsers.py:96` | `def parse_rdap(payload)` |
| `parse_reddit` | function | `estorides_core/parsers.py:857` | `def parse_reddit(payload)` |
| `parse_reddit_search` | function | `estorides_core/parsers.py:944` | `def parse_reddit_search(payload)` |
| `parse_ripe_stat` | function | `estorides_core/parsers.py:427` | `def parse_ripe_stat(payload)` |
| `parse_shodan_internetdb` | function | `estorides_core/parsers.py:227` | `def parse_shodan_internetdb(payload)` |
| `parse_text_lines` | function | `estorides_core/parsers.py:973` | `def parse_text_lines(payload)` |
| `parse_threatfox` | function | `estorides_core/parsers.py:503` | `def parse_threatfox(payload)` |
| `parse_twitch_user` | function | `estorides_core/parsers.py:1099` | `def parse_twitch_user(payload)` |
| `parse_twitter_user` | function | `estorides_core/parsers.py:1026` | `def parse_twitter_user(payload)` |
| `parse_urlhaus` | function | `estorides_core/parsers.py:512` | `def parse_urlhaus(payload)` |
| `parse_urlhaus_payloads` | function | `estorides_core/parsers.py:521` | `def parse_urlhaus_payloads(payload)` |
| `parse_urlscan` | function | `estorides_core/parsers.py:456` | `def parse_urlscan(payload)` |
| `parse_vt_domain` | function | `estorides_core/parsers.py:325` | `def parse_vt_domain(payload)` |
| `parse_vt_file` | function | `estorides_core/parsers.py:352` | `def parse_vt_file(payload)` |
| `parse_vt_ip` | function | `estorides_core/parsers.py:304` | `def parse_vt_ip(payload)` |
| `parse_wayback_avail` | function | `estorides_core/parsers.py:493` | `def parse_wayback_avail(payload)` |
| `parse_wayback_cdx` | function | `estorides_core/parsers.py:478` | `def parse_wayback_cdx(payload)` |
| `parse_whois_text` | function | `estorides_core/parsers.py:1008` | `def parse_whois_text(payload)` |
| `parse_wikidata` | function | `estorides_core/parsers.py:628` | `def parse_wikidata(payload)` |
| `parse_wikipedia` | function | `estorides_core/parsers.py:619` | `def parse_wikipedia(payload)` |
| `parse_youtube_user` | function | `estorides_core/parsers.py:1062` | `def parse_youtube_user(payload)` |
| `register_parser` | function | `estorides_core/parsers.py:1264` | `def register_parser(name, description)` |
| `CertRecord` | class | `estorides_core/pdns_monitor.py:40` | `class CertRecord` |
| `HistoricalSubdomain` | class | `estorides_core/pdns_monitor.py:13` | `class HistoricalSubdomain` |
| `IPRecord` | class | `estorides_core/pdns_monitor.py:27` | `class IPRecord` |
| `PDNSResult` | class | `estorides_core/pdns_monitor.py:55` | `class PDNSResult` |
| `analyse_pdns_data` | method | `estorides_core/pdns_monitor.py:80` | `def analyse_pdns_data(subdomains, ip_history, new_certs)` |
| `classify_subdomain_status` | method | `estorides_core/pdns_monitor.py:72` | `def classify_subdomain_status(fqdn, resolved_ips)` |
| `extract_sans_from_cert` | method | `estorides_core/pdns_monitor.py:76` | `def extract_sans_from_cert(cert)` |
| `to_dict` | method | `estorides_core/pdns_monitor.py:22` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/pdns_monitor.py:35` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/pdns_monitor.py:50` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/pdns_monitor.py:62` | `def to_dict(self)` |
| `BreachContext` | class | `estorides_core/people_intel.py:56` | `class BreachContext` |
| `BreachRecord` | class | `estorides_core/people_intel.py:15` | `class BreachRecord` |
| `Employee` | class | `estorides_core/people_intel.py:29` | `class Employee` |
| `PeopleIntelResult` | class | `estorides_core/people_intel.py:67` | `class PeopleIntelResult` |
| `_match_pattern` | method | `estorides_core/people_intel.py:136` | `def _match_pattern(local)` |
| `_severity_from_breaches` | method | `estorides_core/people_intel.py:143` | `def _severity_from_breaches(breaches)` |
| `analyse_employees` | method | `estorides_core/people_intel.py:176` | `def analyse_employees(employees, domain)` |
| `correlate_breaches` | method | `estorides_core/people_intel.py:153` | `def correlate_breaches(employees)` |
| `infer_email_pattern` | method | `estorides_core/people_intel.py:98` | `def infer_email_pattern(emails)` |
| `to_dict` | method | `estorides_core/people_intel.py:22` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/people_intel.py:40` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/people_intel.py:62` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/people_intel.py:75` | `def to_dict(self)` |
| `BufferedEventSink` | class | `estorides_core/pivot_engine.py:77` | `class BufferedEventSink` |
| `EntityRunner` | class | `estorides_core/pivot_engine.py:113` | `class EntityRunner(Protocol)` |
| `EventSink` | class | `estorides_core/pivot_engine.py:59` | `class EventSink(Protocol)` |
| `ListEventSink` | class | `estorides_core/pivot_engine.py:67` | `class ListEventSink` |
| `PivotBudget` | class | `estorides_core/pivot_engine.py:139` | `class PivotBudget` |
| `PivotEngine` | class | `estorides_core/pivot_engine.py:195` | `class PivotEngine` |
| `PivotEvent` | class | `estorides_core/pivot_engine.py:47` | `class PivotEvent` |
| `PivotLead` | class | `estorides_core/pivot_engine.py:172` | `class PivotLead` |
| `PivotResult` | class | `estorides_core/pivot_engine.py:184` | `class PivotResult` |
| `__init__` | method | `estorides_core/pivot_engine.py:70` | `def __init__(self)` |
| `__init__` | method | `estorides_core/pivot_engine.py:87` | `def __init__(self, capacity)` |
| `__init__` | method | `estorides_core/pivot_engine.py:198` | `def __init__(self, runner, sink)` |
| `_emit` | method | `estorides_core/pivot_engine.py:246` | `def _emit(self, event_type)` |
| `_expand_lead` | method | `estorides_core/pivot_engine.py:341` | `def _expand_lead(self, lead, frontier, budget)` |
| `_heap_push` | method | `estorides_core/pivot_engine.py:255` | `def _heap_push(heap, counter, lead)` |
| `_ingest_children` | method | `estorides_core/pivot_engine.py:411` | `def _ingest_children(self, parent, result, frontier, budget)` |
| `_on_source_done` | method | `estorides_core/pivot_engine.py:356` | `def _on_source_done(name, ok, status, elapsed_ms)` |
| `_on_source_result` | method | `estorides_core/pivot_engine.py:366` | `def _on_source_result(observation)` |
| `emit` | method | `estorides_core/pivot_engine.py:62` | `def emit(self, event)` |
| `emit` | method | `estorides_core/pivot_engine.py:73` | `def emit(self, event)` |
| `emit` | method | `estorides_core/pivot_engine.py:94` | `def emit(self, event)` |
| `exhausted` | method | `estorides_core/pivot_engine.py:159` | `def exhausted(self)` |
| `run` | method | `estorides_core/pivot_engine.py:120` | `def run(self, query)` |
| `run` | method | `estorides_core/pivot_engine.py:264` | `def run(self, seed_type, seed_value)` |
| `time_left` | method | `estorides_core/pivot_engine.py:155` | `def time_left(self)` |
| `FusionResult` | class | `estorides_core/recon_fusion.py:84` | `class FusionResult` |
| `GroupedEntity` | class | `estorides_core/recon_fusion.py:46` | `class GroupedEntity` |
| `ReconFusionEngine` | class | `estorides_core/recon_fusion.py:160` | `class ReconFusionEngine` |
| `RelevanceTier` | class | `estorides_core/recon_fusion.py:27` | `class RelevanceTier(str, Enum)` |
| `__init__` | method | `estorides_core/recon_fusion.py:166` | `def __init__(self, config)` |
| `_assign_tier` | method | `estorides_core/recon_fusion.py:386` | `def _assign_tier(self, source_count, avg_reliability, direct_match)` |
| `_canonical_id` | method | `estorides_core/recon_fusion.py:112` | `def _canonical_id(etype, value)` |
| `_classify_groups` | method | `estorides_core/recon_fusion.py:321` | `def _classify_groups(self, groups, query)` |
| `_corroboration_factor` | method | `estorides_core/recon_fusion.py:117` | `def _corroboration_factor(source_count)` |
| `_deduplicate` | method | `estorides_core/recon_fusion.py:219` | `def _deduplicate(self, observations)` |
| `_direct_match_query` | method | `estorides_core/recon_fusion.py:132` | `def _direct_match_query(value, query)` |
| `_extract_key_findings` | method | `estorides_core/recon_fusion.py:137` | `def _extract_key_findings(observations)` |
| `_freshness_factor` | method | `estorides_core/recon_fusion.py:124` | `def _freshness_factor(age_hours, max_hours)` |
| `_group_by_entity` | method | `estorides_core/recon_fusion.py:237` | `def _group_by_entity(self, observations, entities)` |
| `_normalize_value` | method | `estorides_core/recon_fusion.py:107` | `def _normalize_value(etype, value)` |
| `classify` | method | `estorides_core/recon_fusion.py:169` | `def classify(self, query, query_type, observations, entities)` |
| `ordered` | method | `estorides_core/recon_fusion.py:40` | `def ordered(cls)` |
| `to_dict` | method | `estorides_core/recon_fusion.py:64` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/recon_fusion.py:95` | `def to_dict(self)` |
| `run_passive_recon` | function | `estorides_core/recon_pipeline.py:22` | `def run_passive_recon(query, headers, html, cookies, employees, code_findings, third_parties, pdns_subdomains...` |
| `RelationshipInferer` | class | `estorides_core/relationship_inference.py:36` | `class RelationshipInferer(Protocol)` |
| `__call__` | method | `estorides_core/relationship_inference.py:51` | `def __call__(self, observation, query, kg)` |
| `_infer_abuseipdb` | method | `estorides_core/relationship_inference.py:143` | `def _infer_abuseipdb(observation, query, kg)` |
| `_infer_crtsh` | method | `estorides_core/relationship_inference.py:114` | `def _infer_crtsh(observation, query, kg)` |
| `_infer_dns` | method | `estorides_core/relationship_inference.py:105` | `def _infer_dns(observation, query, kg)` |
| `_infer_greynoise` | method | `estorides_core/relationship_inference.py:134` | `def _infer_greynoise(observation, query, kg)` |
| `_infer_ipapi` | method | `estorides_core/relationship_inference.py:186` | `def _infer_ipapi(observation, query, kg)` |
| `_infer_nvd` | method | `estorides_core/relationship_inference.py:208` | `def _infer_nvd(observation, query, kg)` |
| `_infer_otx` | method | `estorides_core/relationship_inference.py:195` | `def _infer_otx(observation, query, kg)` |
| `_infer_phonebook` | method | `estorides_core/relationship_inference.py:175` | `def _infer_phonebook(observation, query, kg)` |
| `_infer_shodan` | method | `estorides_core/relationship_inference.py:122` | `def _infer_shodan(observation, query, kg)` |
| `_infer_urlscan` | method | `estorides_core/relationship_inference.py:163` | `def _infer_urlscan(observation, query, kg)` |
| `_infer_whois` | method | `estorides_core/relationship_inference.py:152` | `def _infer_whois(observation, query, kg)` |
| `deco` | method | `estorides_core/relationship_inference.py:70` | `def deco(func)` |
| `infer_relationship` | method | `estorides_core/relationship_inference.py:78` | `def infer_relationship(observation, query, kg)` |
| `register_inferer` | method | `estorides_core/relationship_inference.py:63` | `def register_inferer(source_name)` |
| `ConfidenceInput` | class | `estorides_core/reliability_scoring.py:243` | `class ConfidenceInput` |
| `ConfidenceResult` | class | `estorides_core/reliability_scoring.py:263` | `class ConfidenceResult` |
| `Credibility` | class | `estorides_core/reliability_scoring.py:48` | `class Credibility(int, Enum)` |
| `SourceReliability` | class | `estorides_core/reliability_scoring.py:37` | `class SourceReliability(str, Enum)` |
| `SourceType` | class | `estorides_core/reliability_scoring.py:59` | `class SourceType(str, Enum)` |
| `__post_init__` | method | `estorides_core/reliability_scoring.py:253` | `def __post_init__(self)` |
| `_clamp01` | method | `estorides_core/reliability_scoring.py:302` | `def _clamp01(value)` |
| `_corroboration_weight` | method | `estorides_core/reliability_scoring.py:280` | `def _corroboration_weight(n)` |
| `_freshness_weight` | method | `estorides_core/reliability_scoring.py:287` | `def _freshness_weight(age_seconds, half_life_days)` |
| `_validate_score` | method | `estorides_core/reliability_scoring.py:297` | `def _validate_score(value, field_name)` |
| `compute_confidence` | method | `estorides_core/reliability_scoring.py:312` | `def compute_confidence(inp)` |
| `merge_confidence` | method | `estorides_core/reliability_scoring.py:350` | `def merge_confidence(existing, new_observation)` |
| `reliability_from_name` | method | `estorides_core/reliability_scoring.py:400` | `def reliability_from_name(source_name)` |
| `reliability_weight` | method | `estorides_core/reliability_scoring.py:430` | `def reliability_weight(source_name, overrides)` |
| `reliability_weight_for_letter` | method | `estorides_core/reliability_scoring.py:452` | `def reliability_weight_for_letter(letter)` |
| `source_type_from_name` | method | `estorides_core/reliability_scoring.py:415` | `def source_type_from_name(source_name)` |
| `CidrRule` | class | `estorides_core/scope.py:130` | `class CidrRule(ScopeRule)` |
| `ExactHostRule` | class | `estorides_core/scope.py:117` | `class ExactHostRule(ScopeRule)` |
| `RegexRule` | class | `estorides_core/scope.py:148` | `class RegexRule(ScopeRule)` |
| `ScopeMatcher` | class | `estorides_core/scope.py:234` | `class ScopeMatcher` |
| `ScopeReport` | class | `estorides_core/scope.py:344` | `class ScopeReport` |
| `ScopeRule` | class | `estorides_core/scope.py:89` | `class ScopeRule(ABC)` |
| `WildcardRule` | class | `estorides_core/scope.py:102` | `class WildcardRule(ScopeRule)` |
| `__init__` | method | `estorides_core/scope.py:242` | `def __init__(self, in_scope, out_of_scope)` |
| `_assets_from_json` | method | `estorides_core/scope.py:322` | `def _assets_from_json(doc)` |
| `_cidr_factory` | method | `estorides_core/scope.py:179` | `def _cidr_factory(text)` |
| `_exact_host_factory` | method | `estorides_core/scope.py:195` | `def _exact_host_factory(text)` |
| `_ip_factory` | method | `estorides_core/scope.py:188` | `def _ip_factory(text)` |
| `_regex_factory` | method | `estorides_core/scope.py:168` | `def _regex_factory(text)` |
| `_wildcard_factory` | method | `estorides_core/scope.py:161` | `def _wildcard_factory(text)` |
| `build_report` | method | `estorides_core/scope.py:371` | `def build_report(matcher, assets)` |
| `classify` | method | `estorides_core/scope.py:258` | `def classify(self, raw_asset)` |
| `describe` | method | `estorides_core/scope.py:97` | `def describe(self)` |
| `describe` | method | `estorides_core/scope.py:112` | `def describe(self)` |
| `describe` | method | `estorides_core/scope.py:125` | `def describe(self)` |
| `describe` | method | `estorides_core/scope.py:143` | `def describe(self)` |
| `describe` | method | `estorides_core/scope.py:156` | `def describe(self)` |
| `hosts` | method | `estorides_core/scope.py:352` | `def hosts(self)` |
| `in_rules` | method | `estorides_core/scope.py:251` | `def in_rules(self)` |
| `ips` | method | `estorides_core/scope.py:357` | `def ips(self)` |
| `is_ip` | function | `estorides_core/scope.py:79` | `def is_ip(asset)` |
| `load_assets` | method | `estorides_core/scope.py:303` | `def load_assets(path)` |
| `load_rules_file` | method | `estorides_core/scope.py:285` | `def load_rules_file(path)` |
| `matches` | method | `estorides_core/scope.py:93` | `def matches(self, asset)` |
| `matches` | method | `estorides_core/scope.py:107` | `def matches(self, asset)` |
| `matches` | method | `estorides_core/scope.py:122` | `def matches(self, asset)` |
| `matches` | method | `estorides_core/scope.py:135` | `def matches(self, asset)` |
| `matches` | method | `estorides_core/scope.py:153` | `def matches(self, asset)` |
| `normalise_asset` | function | `estorides_core/scope.py:52` | `def normalise_asset(raw)` |
| `out_rules` | method | `estorides_core/scope.py:255` | `def out_rules(self)` |
| `parse_rule` | method | `estorides_core/scope.py:211` | `def parse_rule(line)` |
| `parse_rules` | method | `estorides_core/scope.py:223` | `def parse_rules(lines)` |
| `partition` | method | `estorides_core/scope.py:269` | `def partition(self, assets)` |
| `to_dict` | method | `estorides_core/scope.py:361` | `def to_dict(self)` |
| `write_flat_lists` | method | `estorides_core/scope.py:381` | `def write_flat_lists(report, out_dir)` |
| `InvalidTelemetryConfigError` | class | `estorides_core/search_telemetry.py:45` | `class InvalidTelemetryConfigError(SearchTelemetryError, ValueError)` |
| `KeyboardShortcut` | class | `estorides_core/search_telemetry.py:117` | `class KeyboardShortcut` |
| `ProgressView` | class | `estorides_core/search_telemetry.py:146` | `class ProgressView` |
| `SearchPhase` | class | `estorides_core/search_telemetry.py:133` | `class SearchPhase` |
| `SearchTelemetry` | class | `estorides_core/search_telemetry.py:217` | `class SearchTelemetry` |
| `SearchTelemetryError` | class | `estorides_core/search_telemetry.py:37` | `class SearchTelemetryError(Exception)` |
| `SplashTip` | class | `estorides_core/search_telemetry.py:125` | `class SplashTip` |
| `TelemetryConfig` | class | `estorides_core/search_telemetry.py:177` | `class TelemetryConfig` |
| `UnknownPhaseError` | class | `estorides_core/search_telemetry.py:41` | `class UnknownPhaseError(SearchTelemetryError, KeyError)` |
| `__init__` | method | `estorides_core/search_telemetry.py:223` | `def __init__(self, config)` |
| `__post_init__` | method | `estorides_core/search_telemetry.py:191` | `def __post_init__(self)` |
| `_assert_clean` | method | `estorides_core/search_telemetry.py:167` | `def _assert_clean(label)` |
| `_default_config` | method | `estorides_core/search_telemetry.py:309` | `def _default_config()` |
| `context` | method | `estorides_core/search_telemetry.py:288` | `def context(self)` |
| `disallowed_brands_in` | method | `estorides_core/search_telemetry.py:75` | `def disallowed_brands_in(text)` |
| `emoji_in` | method | `estorides_core/search_telemetry.py:89` | `def emoji_in(text)` |
| `percent_encoded_emoji_in` | method | `estorides_core/search_telemetry.py:103` | `def percent_encoded_emoji_in(text)` |
| `phase` | method | `estorides_core/search_telemetry.py:241` | `def phase(self, key)` |
| `phases` | method | `estorides_core/search_telemetry.py:237` | `def phases(self)` |
| `progress` | method | `estorides_core/search_telemetry.py:249` | `def progress(self, completed, total, phase_key)` |
| `shortcuts` | method | `estorides_core/search_telemetry.py:229` | `def shortcuts(self)` |
| `tips` | method | `estorides_core/search_telemetry.py:233` | `def tips(self)` |
| `PlatformInfo` | class | `estorides_core/socmint.py:32` | `class PlatformInfo` |
| `ProfileMatch` | class | `estorides_core/socmint.py:81` | `class ProfileMatch` |
| `SocialMediaInferer` | class | `estorides_core/socmint.py:203` | `class SocialMediaInferer` |
| `SocialMediaProfile` | class | `estorides_core/socmint.py:105` | `class SocialMediaProfile` |
| `__init__` | method | `estorides_core/socmint.py:214` | `def __init__(self)` |
| `_confidence_for_platform_matches` | method | `estorides_core/socmint.py:185` | `def _confidence_for_platform_matches(platform_count, has_verified, has_keybase)` |
| `_extract_profile_urls` | method | `estorides_core/socmint.py:164` | `def _extract_profile_urls(text)` |
| `discover_from_text` | method | `estorides_core/socmint.py:311` | `def discover_from_text(self, text)` |
| `platform_list` | method | `estorides_core/socmint.py:344` | `def platform_list(self)` |
| `resolve` | method | `estorides_core/socmint.py:218` | `def resolve(self, username, platforms)` |
| `to_dict` | method | `estorides_core/socmint.py:92` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/socmint.py:119` | `def to_dict(self)` |
| `DashboardSummary` | class | `estorides_core/source_health_monitoring.py:160` | `class DashboardSummary` |
| `HealthDashboard` | class | `estorides_core/source_health_monitoring.py:173` | `class HealthDashboard` |
| `SourceHealthConfig` | class | `estorides_core/source_health_monitoring.py:42` | `class SourceHealthConfig` |
| `SourceHealthInput` | class | `estorides_core/source_health_monitoring.py:98` | `class SourceHealthInput` |
| `SourceHealthResult` | class | `estorides_core/source_health_monitoring.py:134` | `class SourceHealthResult` |
| `SourceHealthStatus` | class | `estorides_core/source_health_monitoring.py:31` | `class SourceHealthStatus(str, Enum)` |
| `__post_init__` | method | `estorides_core/source_health_monitoring.py:58` | `def __post_init__(self)` |
| `__post_init__` | method | `estorides_core/source_health_monitoring.py:112` | `def __post_init__(self)` |
| `_clamp01` | method | `estorides_core/source_health_monitoring.py:202` | `def _clamp01(value)` |
| `_classify` | method | `estorides_core/source_health_monitoring.py:210` | `def _classify(success_rate, avg_latency_ms, freshness_hours, fetch_count, config)` |
| `build_dashboard` | method | `estorides_core/source_health_monitoring.py:295` | `def build_dashboard(records, config)` |
| `compute_health` | method | `estorides_core/source_health_monitoring.py:235` | `def compute_health(inp, config)` |
| `to_dict` | method | `estorides_core/source_health_monitoring.py:146` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/source_health_monitoring.py:184` | `def to_dict(self)` |
| `Source` | class | `estorides_core/source_loader.py:22` | `class Source(dict)` |
| `SourceRegistry` | class | `estorides_core/source_loader.py:38` | `class SourceRegistry` |
| `__getattr__` | method | `estorides_core/source_loader.py:31` | `def __getattr__(self, key)` |
| `__init__` | method | `estorides_core/source_loader.py:28` | `def __init__(self, data)` |
| `__init__` | method | `estorides_core/source_loader.py:41` | `def __init__(self, sources_dir)` |
| `_category_dir_name` | method | `estorides_core/source_loader.py:237` | `def _category_dir_name(self, category)` |
| `_find_source_file` | method | `estorides_core/source_loader.py:259` | `def _find_source_file(self, name)` |
| `_load_file` | method | `estorides_core/source_loader.py:71` | `def _load_file(self, path)` |
| `_normalise` | method | `estorides_core/source_loader.py:111` | `def _normalise(self, raw)` |
| `_source_path` | method | `estorides_core/source_loader.py:253` | `def _source_path(self, name, category)` |
| `all` | method | `estorides_core/source_loader.py:203` | `def all(self)` |
| `by_category` | method | `estorides_core/source_loader.py:206` | `def by_category(self, category)` |
| `categories` | method | `estorides_core/source_loader.py:209` | `def categories(self)` |
| `delete_source_file` | method | `estorides_core/source_loader.py:342` | `def delete_source_file(self, name)` |
| `filter` | method | `estorides_core/source_loader.py:215` | `def filter(self)` |
| `get` | method | `estorides_core/source_loader.py:200` | `def get(self, name)` |
| `load` | method | `estorides_core/source_loader.py:47` | `def load(self)` |
| `names` | method | `estorides_core/source_loader.py:212` | `def names(self)` |
| `summary` | method | `estorides_core/source_loader.py:351` | `def summary(self)` |
| `write_source_file` | method | `estorides_core/source_loader.py:272` | `def write_source_file(self, data)` |
| `DictMixin` | class | `estorides_core/sqlite_store.py:90` | `class DictMixin` |
| `SqliteStore` | class | `estorides_core/sqlite_store.py:34` | `class SqliteStore` |
| `__init__` | method | `estorides_core/sqlite_store.py:50` | `def __init__(self, path)` |
| `_init_schema` | method | `estorides_core/sqlite_store.py:66` | `def _init_schema(self)` |
| `_tx` | method | `estorides_core/sqlite_store.py:72` | `def _tx(self)` |
| `close` | method | `estorides_core/sqlite_store.py:82` | `def close(self)` |
| `to_dict` | method | `estorides_core/sqlite_store.py:93` | `def to_dict(self)` |
| `GuardResult` | class | `estorides_core/ssrf_guard.py:99` | `class GuardResult` |
| `SSRFError` | class | `estorides_core/ssrf_guard.py:269` | `class SSRFError(ValueError)` |
| `__bool__` | method | `estorides_core/ssrf_guard.py:105` | `def __bool__(self)` |
| `_is_blocked_v4` | method | `estorides_core/ssrf_guard.py:110` | `def _is_blocked_v4(ip)` |
| `_is_blocked_v6` | method | `estorides_core/ssrf_guard.py:114` | `def _is_blocked_v6(addr)` |
| `_is_host_in_blocked_literal` | method | `estorides_core/ssrf_guard.py:134` | `def _is_host_in_blocked_literal(host)` |
| `_load_allowlist` | method | `estorides_core/ssrf_guard.py:189` | `def _load_allowlist()` |
| `_matches_allowlist` | method | `estorides_core/ssrf_guard.py:172` | `def _matches_allowlist(host, allowlist)` |
| `_normalise_host` | method | `estorides_core/ssrf_guard.py:126` | `def _normalise_host(host)` |
| `_resolve` | method | `estorides_core/ssrf_guard.py:155` | `def _resolve(host)` |
| `assert_safe` | method | `estorides_core/ssrf_guard.py:262` | `def assert_safe(url)` |
| `check_url` | method | `estorides_core/ssrf_guard.py:194` | `def check_url(url)` |
| `Relationship` | class | `estorides_core/supply_chain.py:78` | `class Relationship` |
| `SharedInfra` | class | `estorides_core/supply_chain.py:66` | `class SharedInfra` |
| `SupplyChainResult` | class | `estorides_core/supply_chain.py:89` | `class SupplyChainResult` |
| `ThirdParty` | class | `estorides_core/supply_chain.py:54` | `class ThirdParty` |
| `analyse_third_parties` | method | `estorides_core/supply_chain.py:129` | `def analyse_third_parties(third_parties, subsidiaries)` |
| `detect_cdn` | method | `estorides_core/supply_chain.py:122` | `def detect_cdn(cname)` |
| `detect_mx_provider` | method | `estorides_core/supply_chain.py:106` | `def detect_mx_provider(mx_records)` |
| `detect_ns_provider` | method | `estorides_core/supply_chain.py:114` | `def detect_ns_provider(ns_records)` |
| `detect_shared_infrastructure` | method | `estorides_core/supply_chain.py:140` | `def detect_shared_infrastructure(asn)` |
| `to_dict` | method | `estorides_core/supply_chain.py:61` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/supply_chain.py:73` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/supply_chain.py:84` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/supply_chain.py:96` | `def to_dict(self)` |
| `SystemAppResult` | class | `estorides_core/system_app_sources.py:57` | `class SystemAppResult` |
| `_line_filter_parser` | method | `estorides_core/system_app_sources.py:150` | `def _line_filter_parser()` |
| `_loads_lenient` | method | `estorides_core/system_app_sources.py:131` | `def _loads_lenient(text)` |
| `_read_capped` | method | `estorides_core/system_app_sources.py:121` | `def _read_capped(path, cap)` |
| `execute` | method | `estorides_core/system_app_sources.py:396` | `def execute(source, query)` |
| `fail` | method | `estorides_core/system_app_sources.py:418` | `def fail(code, message)` |
| `is_system_app` | method | `estorides_core/system_app_sources.py:81` | `def is_system_app(source)` |
| `parse_amass_json` | method | `estorides_core/system_app_sources.py:193` | `def parse_amass_json(payload)` |
| `parse_dmitry_text` | method | `estorides_core/system_app_sources.py:297` | `def parse_dmitry_text(payload)` |
| `parse_dnsenum_text` | method | `estorides_core/system_app_sources.py:285` | `def parse_dnsenum_text(payload)` |
| `parse_dnsrecon_text` | method | `estorides_core/system_app_sources.py:280` | `def parse_dnsrecon_text(payload)` |
| `parse_fierce_text` | method | `estorides_core/system_app_sources.py:292` | `def parse_fierce_text(payload)` |
| `parse_holehe_text` | method | `estorides_core/system_app_sources.py:265` | `def parse_holehe_text(payload)` |
| `parse_maigret_json` | method | `estorides_core/system_app_sources.py:225` | `def parse_maigret_json(payload)` |
| `parse_mailfy_text` | method | `estorides_core/system_app_sources.py:327` | `def parse_mailfy_text(payload)` |
| `parse_metagoofil_text` | method | `estorides_core/system_app_sources.py:307` | `def parse_metagoofil_text(payload)` |
| `parse_phonefy_text` | method | `estorides_core/system_app_sources.py:332` | `def parse_phonefy_text(payload)` |
| `parse_phoneinfoga_json` | method | `estorides_core/system_app_sources.py:247` | `def parse_phoneinfoga_json(payload)` |
| `parse_searchfy_text` | method | `estorides_core/system_app_sources.py:337` | `def parse_searchfy_text(payload)` |
| `parse_sherlock_text` | method | `estorides_core/system_app_sources.py:260` | `def parse_sherlock_text(payload)` |
| `parse_sublist3r_lines` | method | `estorides_core/system_app_sources.py:275` | `def parse_sublist3r_lines(payload)` |
| `parse_theharvester_text` | method | `estorides_core/system_app_sources.py:317` | `def parse_theharvester_text(payload)` |
| `parse_tool_output` | method | `estorides_core/system_app_sources.py:365` | `def parse_tool_output(source_name, parser_name, data)` |
| `parse_urlcrazy_text` | method | `estorides_core/system_app_sources.py:302` | `def parse_urlcrazy_text(payload)` |
| `parse_usufy_text` | method | `estorides_core/system_app_sources.py:322` | `def parse_usufy_text(payload)` |
| `parse_wafw00f_text` | method | `estorides_core/system_app_sources.py:270` | `def parse_wafw00f_text(payload)` |
| `parse_whatweb_text` | method | `estorides_core/system_app_sources.py:312` | `def parse_whatweb_text(payload)` |
| `parser` | method | `estorides_core/system_app_sources.py:165` | `def parser(payload)` |
| `render_args` | method | `estorides_core/system_app_sources.py:96` | `def render_args(args, query, outdir)` |
| `repl` | method | `estorides_core/system_app_sources.py:109` | `def repl(m)` |
| `to_dict` | method | `estorides_core/system_app_sources.py:76` | `def to_dict(self)` |
| `tool_available` | method | `estorides_core/system_app_sources.py:91` | `def tool_available(binary)` |
| `Tech` | class | `estorides_core/tech_fingerprint.py:89` | `class Tech` |
| `TechFingerprintResult` | class | `estorides_core/tech_fingerprint.py:102` | `class TechFingerprintResult` |
| `_add` | method | `estorides_core/tech_fingerprint.py:129` | `def _add(name, category, version, source, confidence)` |
| `fingerprint` | method | `estorides_core/tech_fingerprint.py:115` | `def fingerprint(headers, html, cookies, status)` |
| `to_dict` | method | `estorides_core/tech_fingerprint.py:97` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/tech_fingerprint.py:107` | `def to_dict(self)` |
| `InstallRecipe` | class | `estorides_core/tool_install.py:81` | `class InstallRecipe` |
| `InstallResult` | class | `estorides_core/tool_install.py:103` | `class InstallResult` |
| `ToolStatus` | class | `estorides_core/tool_install.py:278` | `class ToolStatus` |
| `_check_shell_command` | method | `estorides_core/tool_install.py:148` | `def _check_shell_command(command)` |
| `_elevate` | method | `estorides_core/tool_install.py:117` | `def _elevate(cmd)` |
| `_install_apt` | method | `estorides_core/tool_install.py:358` | `def _install_apt(recipe)` |
| `_install_git` | method | `estorides_core/tool_install.py:375` | `def _install_git(recipe)` |
| `_needs_elevation` | method | `estorides_core/tool_install.py:154` | `def _needs_elevation(command)` |
| `_recipe_path` | method | `estorides_core/tool_install.py:193` | `def _recipe_path(name)` |
| `_recipe_table` | method | `estorides_core/tool_install.py:179` | `def _recipe_table()` |
| `_run` | method | `estorides_core/tool_install.py:132` | `def _run(cmd)` |
| `_system_app_binaries` | method | `estorides_core/tool_install.py:297` | `def _system_app_binaries(sources_dir)` |
| `_tools_root` | method | `estorides_core/tool_install.py:371` | `def _tools_root()` |
| `_verify` | method | `estorides_core/tool_install.py:506` | `def _verify(binary)` |
| `doctor` | method | `estorides_core/tool_install.py:321` | `def doctor(sources_dir)` |
| `has_apt` | method | `estorides_core/tool_install.py:95` | `def has_apt(self)` |
| `has_git` | method | `estorides_core/tool_install.py:98` | `def has_git(self)` |
| `install_tool` | method | `estorides_core/tool_install.py:414` | `def install_tool(tool_name)` |
| `is_valid_binary` | method | `estorides_core/tool_install.py:174` | `def is_valid_binary(name)` |
| `is_valid_recipe_name` | method | `estorides_core/tool_install.py:169` | `def is_valid_recipe_name(name)` |
| `list_recipes` | method | `estorides_core/tool_install.py:270` | `def list_recipes()` |
| `load_recipe` | method | `estorides_core/tool_install.py:210` | `def load_recipe(name)` |
| `main` | method | `estorides_core/tool_install.py:516` | `def main(argv)` |
| `recipe_available` | method | `estorides_core/tool_install.py:254` | `def recipe_available(name)` |
| `to_dict` | method | `estorides_core/tool_install.py:113` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/tool_install.py:287` | `def to_dict(self)` |
| `tool_available` | method | `estorides_core/tool_install.py:259` | `def tool_available(binary)` |
| `ToolError` | class | `estorides_core/tool_runner.py:17` | `class ToolError(Exception)` |
| `ToolErrorResult` | class | `estorides_core/tool_runner.py:86` | `class ToolErrorResult` |
| `ToolInjectionError` | class | `estorides_core/tool_runner.py:25` | `class ToolInjectionError(ToolError)` |
| `ToolNotAllowedError` | class | `estorides_core/tool_runner.py:21` | `class ToolNotAllowedError(ToolError)` |
| `ToolNotFoundError` | class | `estorides_core/tool_runner.py:29` | `class ToolNotFoundError(ToolError)` |
| `ToolResult` | class | `estorides_core/tool_runner.py:38` | `class ToolResult` |
| `ToolTimeoutError` | class | `estorides_core/tool_runner.py:33` | `class ToolTimeoutError(ToolError)` |
| `_check_allowlist` | method | `estorides_core/tool_runner.py:114` | `def _check_allowlist(tool_name)` |
| `_check_injection` | method | `estorides_core/tool_runner.py:97` | `def _check_injection(args)` |
| `_parse_entities_generic` | method | `estorides_core/tool_runner.py:121` | `def _parse_entities_generic(stdout, tool_name)` |
| `_resolve_binary` | method | `estorides_core/tool_runner.py:107` | `def _resolve_binary(tool_name)` |
| `from_failure` | method | `estorides_core/tool_runner.py:59` | `def from_failure(cls, tool_name, error_code, error_message, duration_s, exit_code, stdout, stderr, parsed_entities)` |
| `run_tool` | method | `estorides_core/tool_runner.py:156` | `def run_tool(tool_name, args, target, timeout, max_output_bytes, cwd)` |
| `to_dict` | method | `estorides_core/tool_runner.py:51` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/tool_runner.py:93` | `def to_dict(self)` |
| `Transform` | class | `estorides_core/transforms.py:71` | `class Transform` |
| `TransformRegistry` | class | `estorides_core/transforms.py:225` | `class TransformRegistry` |
| `_T` | method | `estorides_core/transforms.py:441` | `def _T(id, label, tier, applies, runner, description, output_types, cost)` |
| `__init__` | method | `estorides_core/transforms.py:228` | `def __init__(self)` |
| `_empty` | method | `estorides_core/transforms.py:96` | `def _empty(root_type, value)` |
| `_filter_runner` | method | `estorides_core/transforms.py:121` | `def _filter_runner(relations)` |
| `_norm` | method | `estorides_core/transforms.py:130` | `def _norm(s)` |
| `_osiris` | method | `estorides_core/transforms.py:135` | `def _osiris()` |
| `_resolver_filtered` | method | `estorides_core/transforms.py:100` | `def _resolver_filtered(ent_type, value, relations)` |
| `_run_bgp` | method | `estorides_core/transforms.py:143` | `def _run_bgp(ent_type, value)` |
| `_run_github` | method | `estorides_core/transforms.py:194` | `def _run_github(ent_type, value)` |
| `_run_leaks` | method | `estorides_core/transforms.py:169` | `def _run_leaks(ent_type, value)` |
| `_static_runner` | method | `estorides_core/transforms.py:332` | `def _static_runner(nodes_tpl, links_tpl)` |
| `_str_list` | method | `estorides_core/transforms.py:322` | `def _str_list(raw)` |
| `_transform_from_yaml` | method | `estorides_core/transforms.py:362` | `def _transform_from_yaml(raw, origin)` |
| `for_type` | method | `estorides_core/transforms.py:234` | `def for_type(self, ent_type)` |
| `iter_sse_events` | method | `estorides_core/transforms.py:406` | `def iter_sse_events(transform_id, ent_type, value, runner)` |
| `load_yaml_dir` | method | `estorides_core/transforms.py:280` | `def load_yaml_dir(self, directory)` |
| `register` | method | `estorides_core/transforms.py:231` | `def register(self, t)` |
| `run` | method | `estorides_core/transforms.py:122` | `def run(ent_type, value)` |
| `run` | method | `estorides_core/transforms.py:246` | `def run(self, transform_id, ent_type, value)` |
| `run` | method | `estorides_core/transforms.py:335` | `def run(ent_type, value)` |
| `sub` | method | `estorides_core/transforms.py:338` | `def sub(s, depth)` |
| `summary` | method | `estorides_core/transforms.py:83` | `def summary(self)` |
| `_strip_diacritics` | function | `estorides_core/transliteration.py:76` | `def _strip_diacritics(text)` |
| `consonant_skeleton` | function | `estorides_core/transliteration.py:112` | `def consonant_skeleton(text)` |
| `is_non_latin` | function | `estorides_core/transliteration.py:139` | `def is_non_latin(text)` |
| `to_latin` | function | `estorides_core/transliteration.py:87` | `def to_latin(text)` |
| `Query` | class | `estorides_core/validation.py:63` | `class Query` |
| `QueryValidationError` | class | `estorides_core/validation.py:55` | `class QueryValidationError(ValueError)` |
| `__init__` | method | `estorides_core/validation.py:57` | `def __init__(self, reason, message)` |
| `__str__` | method | `estorides_core/validation.py:69` | `def __str__(self)` |
| `_strip_and_collapse` | method | `estorides_core/validation.py:73` | `def _strip_and_collapse(text)` |
| `validate_query` | method | `estorides_core/validation.py:85` | `def validate_query(raw)` |
| `DefaultCred` | class | `estorides_core/vuln_correlation.py:14` | `class DefaultCred` |
| `VulnCorrelationResult` | class | `estorides_core/vuln_correlation.py:43` | `class VulnCorrelationResult` |
| `VulnEntry` | class | `estorides_core/vuln_correlation.py:24` | `class VulnEntry` |
| `_parsed_version` | method | `estorides_core/vuln_correlation.py:141` | `def _parsed_version(version)` |
| `_version_in_range` | method | `estorides_core/vuln_correlation.py:153` | `def _version_in_range(version, v_start, v_end)` |
| `compute_attack_readiness` | method | `estorides_core/vuln_correlation.py:228` | `def compute_attack_readiness(vulnerabilities)` |
| `correlate_technologies` | method | `estorides_core/vuln_correlation.py:202` | `def correlate_technologies(technologies)` |
| `lookup_cve_for_tech` | method | `estorides_core/vuln_correlation.py:169` | `def lookup_cve_for_tech(tech_name, version)` |
| `to_dict` | method | `estorides_core/vuln_correlation.py:19` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/vuln_correlation.py:38` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/vuln_correlation.py:52` | `def to_dict(self)` |
| `AuthGate` | class | `estorides_core/web_security.py:341` | `class AuthGate` |
| `WebSecurityConfig` | class | `estorides_core/web_security.py:87` | `class WebSecurityConfig` |
| `_cors_preflight` | method | `estorides_core/web_security.py:250` | `def _cors_preflight()` |
| `_current_gate` | method | `estorides_core/web_security.py:440` | `def _current_gate()` |
| `_env_str` | method | `estorides_core/web_security.py:137` | `def _env_str(name, default)` |
| `_extract_bearer_token` | method | `estorides_core/web_security.py:286` | `def _extract_bearer_token()` |
| `_redirect_to_https` | method | `estorides_core/web_security.py:203` | `def _redirect_to_https()` |
| `_security_headers` | method | `estorides_core/web_security.py:217` | `def _security_headers(resp)` |
| `auth_meta_for_index` | method | `estorides_core/web_security.py:362` | `def auth_meta_for_index(self)` |
| `auto_generated_token` | method | `estorides_core/web_security.py:444` | `def auto_generated_token()` |
| `build_https_url` | function | `estorides_core/web_security.py:58` | `def build_https_url(public_host, path, query_string)` |
| `check` | method | `estorides_core/web_security.py:354` | `def check(self)` |
| `enabled` | method | `estorides_core/web_security.py:351` | `def enabled(self)` |
| `install_auth_gate` | method | `estorides_core/web_security.py:421` | `def install_auth_gate(app, gate)` |
| `install_security` | method | `estorides_core/web_security.py:169` | `def install_security(app, cfg)` |
| `is_cors_enabled` | method | `estorides_core/web_security.py:128` | `def is_cors_enabled(self)` |
| `is_origin_allowed` | method | `estorides_core/web_security.py:132` | `def is_origin_allowed(self)` |
| `issue_session_cookie_kwargs` | method | `estorides_core/web_security.py:371` | `def issue_session_cookie_kwargs(self)` |
| `load_security_config` | method | `estorides_core/web_security.py:144` | `def load_security_config()` |
| `make_auth_gate` | method | `estorides_core/web_security.py:321` | `def make_auth_gate()` |
| `require_auth` | method | `estorides_core/web_security.py:388` | `def require_auth(view)` |
| `wrapper` | method | `estorides_core/web_security.py:402` | `def wrapper()` |
| `_have_age` | function | `estorides_export/encryption.py:47` | `def _have_age()` |
| `encrypt_file` | function | `estorides_export/encryption.py:51` | `def encrypt_file(plaintext_path, recipient_pubkey)` |
| `export_misp_encrypted` | function | `estorides_export/encryption.py:128` | `def export_misp_encrypted(kg, recipient_pubkey, path)` |

Next: [SYMBOLS_p3.md](SYMBOLS_p3.md)
