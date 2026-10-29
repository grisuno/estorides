# Symbols (page 2 of 8)
Previous: [SYMBOLS.md](SYMBOLS.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `meta` | function | `estorides_core/graph_rag_search.py:341` | `def meta()` |
| `pagerank` | function | `estorides_core/graph_rag_search.py:176` | `def pagerank(ids, edges, alpha, max_iter, tolerance)` |
| `personalized_pagerank` | function | `estorides_core/graph_rag_search.py:207` | `def personalized_pagerank(ids, edges, seeds, alpha, max_iter, tolerance)` |
| `rows` | function | `estorides_core/graph_rag_search.py:335` | `def rows(name)` |
| `scores` | method | `estorides_core/graph_rag_search.py:136` | `def scores(self, query)` |
| `search` | method | `estorides_core/graph_rag_search.py:644` | `def search(self, query, mode, budget_tokens)` |
| `to_dict` | method | `estorides_core/graph_rag_search.py:324` | `def to_dict(self)` |
| `tokenize` | function | `estorides_core/graph_rag_search.py:98` | `def tokenize(text, min_len, stopwords)` |
| `where` | function | `estorides_core/graph_rag_search.py:446` | `def where(cid)` |
| `EntityRef` | class | `estorides_core/hypothesis_engine.py:57` | `class EntityRef` |
| `Evidence` | class | `estorides_core/hypothesis_engine.py:65` | `class Evidence` |
| `Hypothesis` | class | `estorides_core/hypothesis_engine.py:76` | `class Hypothesis` |
| `HypothesisGenerator` | class | `estorides_core/hypothesis_engine.py:210` | `class HypothesisGenerator(Protocol)` |
| `__call__` | method | `estorides_core/hypothesis_engine.py:213` | `def __call__(self, observations, entities)` |
| `_asn_shared_infra` | function | `estorides_core/hypothesis_engine.py:524` | `def _asn_shared_infra(observations, entities)` |
| `_clip_claim` | function | `estorides_core/hypothesis_engine.py:201` | `def _clip_claim(template)` |
| `_confidence` | function | `estorides_core/hypothesis_engine.py:180` | `def _confidence(supporting, contradicting)` |
| `_domain_belongsto_actor` | function | `estorides_core/hypothesis_engine.py:220` | `def _domain_belongsto_actor(observations, entities)` |
| `_domains_in_obs` | function | `estorides_core/hypothesis_engine.py:312` | `def _domains_in_obs(obs)` |
| `_email_aliases_person` | function | `estorides_core/hypothesis_engine.py:333` | `def _email_aliases_person(observations, entities)` |
| `_entity_lookup` | function | `estorides_core/hypothesis_engine.py:127` | `def _entity_lookup(entities)` |
| `_extract_asn` | function | `estorides_core/hypothesis_engine.py:588` | `def _extract_asn(parsed)` |
| `_extract_email` | function | `estorides_core/hypothesis_engine.py:393` | `def _extract_email(parsed)` |
| `_extract_ips` | function | `estorides_core/hypothesis_engine.py:496` | `def _extract_ips(parsed)` |
| `_extract_person_name` | function | `estorides_core/hypothesis_engine.py:404` | `def _extract_person_name(parsed)` |
| `_hypothesis_id` | function | `estorides_core/hypothesis_engine.py:148` | `def _hypothesis_id(htype, entity_refs, supporting)` |
| `_ip_shared_infra` | function | `estorides_core/hypothesis_engine.py:415` | `def _ip_shared_infra(observations, entities)` |
| `_is_mapping` | function | `estorides_core/hypothesis_engine.py:123` | `def _is_mapping(value)` |
| `_looks_like_ipv4` | function | `estorides_core/hypothesis_engine.py:511` | `def _looks_like_ipv4(s)` |
| `_score` | function | `estorides_core/hypothesis_engine.py:166` | `def _score(supporting, contradicting)` |
| `_truncate` | function | `estorides_core/hypothesis_engine.py:113` | `def _truncate(value)` |
| `generate_hypotheses` | function | `estorides_core/hypothesis_engine.py:613` | `def generate_hypotheses(observations, entities, kg)` |
| `stable_id` | function | `estorides_core/ids.py:21` | `def stable_id(payload, length)` |
| `EntityResolver` | class | `estorides_core/intel_resolver.py:156` | `class EntityResolver` |
| `_TTLCache` | class | `estorides_core/intel_resolver.py:120` | `class _TTLCache` |
| `__init__` | method | `estorides_core/intel_resolver.py:121` | `def __init__(self)` |
| `__init__` | method | `estorides_core/intel_resolver.py:165` | `def __init__(self)` |
| `_escape_sparql` | function | `estorides_core/intel_resolver.py:801` | `def _escape_sparql(s)` |
| `_is_valid_ipv4` | function | `estorides_core/intel_resolver.py:793` | `def _is_valid_ipv4(s)` |
| `_norm` | function | `estorides_core/intel_resolver.py:789` | `def _norm(s)` |
| `_resolve_btc` | method | `estorides_core/intel_resolver.py:750` | `def _resolve_btc(self, addr)` |
| `_resolve_company` | method | `estorides_core/intel_resolver.py:510` | `def _resolve_company(self, name)` |
| `_resolve_country` | method | `estorides_core/intel_resolver.py:638` | `def _resolve_country(self, name)` |
| `_resolve_crypto` | method | `estorides_core/intel_resolver.py:756` | `def _resolve_crypto(self, addr, kind)` |
| `_resolve_cve` | method | `estorides_core/intel_resolver.py:678` | `def _resolve_cve(self, cve_id)` |
| `_resolve_domain` | method | `estorides_core/intel_resolver.py:412` | `def _resolve_domain(self, domain)` |
| `_resolve_eth` | method | `estorides_core/intel_resolver.py:753` | `def _resolve_eth(self, addr)` |
| `_resolve_file` | method | `estorides_core/intel_resolver.py:473` | `def _resolve_file(self, file_hash)` |
| `_resolve_ip` | method | `estorides_core/intel_resolver.py:306` | `def _resolve_ip(self, ip)` |
| `_resolve_person` | method | `estorides_core/intel_resolver.py:569` | `def _resolve_person(self, name)` |
| `_run_sparql` | function | `estorides_core/intel_resolver.py:90` | `def _run_sparql(query)` |
| `_val` | function | `estorides_core/intel_resolver.py:111` | `def _val(row, key)` |
| `_vt_add_relationship` | method | `estorides_core/intel_resolver.py:245` | `def _vt_add_relationship(self, path)` |
| `_vt_flag_malicious` | method | `estorides_core/intel_resolver.py:290` | `def _vt_flag_malicious(self, path, node, sources)` |
| `_vt_get` | method | `estorides_core/intel_resolver.py:214` | `def _vt_get(self, path, limit)` |
| `get` | method | `estorides_core/intel_resolver.py:127` | `def get(self, kind, key)` |
| `put` | method | `estorides_core/intel_resolver.py:140` | `def put(self, kind, key, value)` |
| `resolve` | method | `estorides_core/intel_resolver.py:174` | `def resolve(self, ent_type, ent_id)` |
| `stats` | method | `estorides_core/intel_resolver.py:148` | `def stats(self)` |
| `BoundedJobRegistry` | class | `estorides_core/job_registry.py:40` | `class BoundedJobRegistry` |
| `__init__` | method | `estorides_core/job_registry.py:49` | `def __init__(self)` |
| `__len__` | method | `estorides_core/job_registry.py:109` | `def __len__(self)` |
| `_evict_expired_locked` | method | `estorides_core/job_registry.py:119` | `def _evict_expired_locked(self, now)` |
| `evict_expired` | method | `estorides_core/job_registry.py:113` | `def evict_expired(self)` |
| `get` | method | `estorides_core/job_registry.py:80` | `def get(self, key)` |
| `keys` | method | `estorides_core/job_registry.py:101` | `def keys(self)` |
| `pop` | method | `estorides_core/job_registry.py:95` | `def pop(self, key)` |
| `register` | method | `estorides_core/job_registry.py:60` | `def register(self, key, value)` |
| `values` | method | `estorides_core/job_registry.py:105` | `def values(self)` |
| `KnowledgeGraph` | class | `estorides_core/knowledge_graph.py:90` | `class KnowledgeGraph` |
| `__init__` | method | `estorides_core/knowledge_graph.py:91` | `def __init__(self, name)` |
| `_node_color` | method | `estorides_core/knowledge_graph.py:397` | `def _node_color(self, ent_type)` |
| `_node_id` | method | `estorides_core/knowledge_graph.py:384` | `def _node_id(self, kind, value)` |
| `_node_sources` | function | `estorides_core/knowledge_graph.py:73` | `def _node_sources(node)` |
| `_source_node` | method | `estorides_core/knowledge_graph.py:387` | `def _source_node(self, source)` |
| `add_entity` | method | `estorides_core/knowledge_graph.py:97` | `def add_entity(self, entity)` |
| `add_observation` | method | `estorides_core/knowledge_graph.py:127` | `def add_observation(self, source, entities)` |
| `add_relationship` | method | `estorides_core/knowledge_graph.py:142` | `def add_relationship(self, src_type, src_value, rel, dst_type, dst_value)` |
| `communities` | method | `estorides_core/knowledge_graph.py:281` | `def communities(self, nodes)` |
| `ego_subgraph` | method | `estorides_core/knowledge_graph.py:357` | `def ego_subgraph(self, node_id, radius)` |
| `export_graphml` | method | `estorides_core/knowledge_graph.py:164` | `def export_graphml(self, path)` |
| `export_json` | method | `estorides_core/knowledge_graph.py:183` | `def export_json(self)` |
| `export_lazyown` | method | `estorides_core/knowledge_graph.py:207` | `def export_lazyown(self)` |
| `intel_level` | method | `estorides_core/knowledge_graph.py:312` | `def intel_level(self, node_id, bridge_nodes)` |
| `neighbours` | method | `estorides_core/knowledge_graph.py:368` | `def neighbours(self, node_id, relation)` |
| `summary` | method | `estorides_core/knowledge_graph.py:243` | `def summary(self)` |
| `top_entities` | method | `estorides_core/knowledge_graph.py:261` | `def top_entities(self, n, by)` |
| `LanBundleResult` | class | `estorides_core/lan_bundle.py:351` | `class LanBundleResult` |
| `_fmt_ts` | function | `estorides_core/lan_bundle.py:331` | `def _fmt_ts(ts)` |
| `_stix_ref` | function | `estorides_core/lan_bundle.py:341` | `def _stix_ref(node_id, id_map)` |
| `build_bundle` | function | `estorides_core/lan_bundle.py:48` | `def build_bundle(devices)` |
| `default_output_dir` | function | `estorides_core/lan_bundle.py:40` | `def default_output_dir()` |
| `sanitize_stem` | function | `estorides_core/lan_bundle.py:29` | `def sanitize_stem(stem)` |
| `to_dict` | method | `estorides_core/lan_bundle.py:359` | `def to_dict(self)` |
| `write_bundle` | function | `estorides_core/lan_bundle.py:363` | `def write_bundle(devices)` |
| `LanDevice` | class | `estorides_core/lan_inventory.py:51` | `class LanDevice` |
| `_valid_lan_ip` | function | `estorides_core/lan_inventory.py:77` | `def _valid_lan_ip(raw)` |
| `contact_for_tool` | function | `estorides_core/lan_inventory.py:352` | `def contact_for_tool(tool)` |
| `device_to_entities` | function | `estorides_core/lan_inventory.py:331` | `def device_to_entities(device)` |
| `merge_devices` | function | `estorides_core/lan_inventory.py:269` | `def merge_devices(sightings)` |
| `normalize_mac` | function | `estorides_core/lan_inventory.py:64` | `def normalize_mac(raw)` |
| `parse_active_output` | function | `estorides_core/lan_inventory.py:252` | `def parse_active_output(text, source)` |
| `parse_arp_table` | function | `estorides_core/lan_inventory.py:91` | `def parse_arp_table(text)` |
| `parse_dhcp_leases` | function | `estorides_core/lan_inventory.py:119` | `def parse_dhcp_leases(text)` |
| `parse_nmap_grepable` | function | `estorides_core/lan_inventory.py:214` | `def parse_nmap_grepable(text)` |
| `parse_nmap_xml` | function | `estorides_core/lan_inventory.py:152` | `def parse_nmap_xml(text)` |
| `to_dict` | method | `estorides_core/lan_inventory.py:60` | `def to_dict(self)` |
| `LanPolicyDecision` | class | `estorides_core/lan_policy.py:40` | `class LanPolicyDecision` |
| `LanPolicyRequest` | class | `estorides_core/lan_policy.py:30` | `class LanPolicyRequest` |
| `_env_ceiling` | function | `estorides_core/lan_policy.py:59` | `def _env_ceiling()` |
| `_normalize_scope` | function | `estorides_core/lan_policy.py:70` | `def _normalize_scope(raw)` |
| `_strict_bool` | function | `estorides_core/lan_policy.py:66` | `def _strict_bool(value)` |
| `evaluate` | function | `estorides_core/lan_policy.py:104` | `def evaluate(request)` |
| `max_contact_for` | function | `estorides_core/lan_policy.py:97` | `def max_contact_for(allow_active, consent)` |
| `requires_consent` | function | `estorides_core/lan_policy.py:54` | `def requires_consent()` |
| `to_dict` | method | `estorides_core/lan_policy.py:50` | `def to_dict(self)` |
| `LanScanResult` | class | `estorides_core/lan_runner.py:41` | `class LanScanResult` |
| `_attempt` | function | `estorides_core/lan_runner.py:99` | `def _attempt(runner, tool, args, scope_cidr, timeout)` |
| `_default_runner` | function | `estorides_core/lan_runner.py:93` | `def _default_runner()` |
| `read_arp_table` | function | `estorides_core/lan_runner.py:60` | `def read_arp_table()` |
| `read_dhcp_leases` | function | `estorides_core/lan_runner.py:81` | `def read_dhcp_leases()` |
| `run_active_scan` | function | `estorides_core/lan_runner.py:122` | `def run_active_scan(scope_cidr)` |
| `scan` | function | `estorides_core/lan_runner.py:147` | `def scan(scope_cidr)` |
| `to_dict` | method | `estorides_core/lan_runner.py:56` | `def to_dict(self)` |
| `default_scope` | function | `estorides_core/lan_scope.py:79` | `def default_scope(interfaces)` |
| `parse_interface_addr` | function | `estorides_core/lan_scope.py:23` | `def parse_interface_addr(raw)` |
| `parse_ip_addr_output` | function | `estorides_core/lan_scope.py:85` | `def parse_ip_addr_output(text)` |
| `read_local_interfaces` | function | `estorides_core/lan_scope.py:92` | `def read_local_interfaces()` |
| `select_private_cidrs` | function | `estorides_core/lan_scope.py:63` | `def select_private_cidrs(interfaces)` |
| `LanWebVerdict` | class | `estorides_core/lan_web.py:18` | `class LanWebVerdict` |
| `guard` | function | `estorides_core/lan_web.py:92` | `def guard(body)` |
| `is_lan_request` | function | `estorides_core/lan_web.py:50` | `def is_lan_request(body, query)` |
| `scope_payload` | function | `estorides_core/lan_web.py:80` | `def scope_payload(interfaces)` |
| `to_dict` | method | `estorides_core/lan_web.py:29` | `def to_dict(self)` |
| `to_response` | method | `estorides_core/lan_web.py:32` | `def to_response(self)` |
| `_scan_keywords` | function | `estorides_core/mitre_attack.py:156` | `def _scan_keywords(text)` |
| `all_techniques_for` | function | `estorides_core/mitre_attack.py:229` | `def all_techniques_for(observations)` |
| `map_observation` | function | `estorides_core/mitre_attack.py:170` | `def map_observation(observation)` |
| `map_observations` | function | `estorides_core/mitre_attack.py:213` | `def map_observations(observations)` |
| `WatchScheduler` | class | `estorides_core/monitoring.py:280` | `class WatchScheduler` |
| `WatchStore` | class | `estorides_core/monitoring.py:155` | `class WatchStore(SqliteStore)` |
| `WatchTarget` | class | `estorides_core/monitoring.py:91` | `class WatchTarget` |
| `__init__` | method | `estorides_core/monitoring.py:287` | `def __init__(self, store, runner, alerter)` |
| `__post_init__` | method | `estorides_core/monitoring.py:106` | `def __post_init__(self)` |
| `_execute_watch` | method | `estorides_core/monitoring.py:344` | `def _execute_watch(self, watch)` |
| `_loop` | method | `estorides_core/monitoring.py:333` | `def _loop(self)` |
| `create_watch` | method | `estorides_core/monitoring.py:162` | `def create_watch(self, watch)` |
| `delete_watch` | method | `estorides_core/monitoring.py:199` | `def delete_watch(self, watch_id)` |
| `due_watches` | method | `estorides_core/monitoring.py:213` | `def due_watches(self, now)` |
| `from_dict` | method | `estorides_core/monitoring.py:126` | `def from_dict(cls, d)` |
| `from_row` | method | `estorides_core/monitoring.py:142` | `def from_row(cls, row)` |
| `get_watch` | method | `estorides_core/monitoring.py:177` | `def get_watch(self, watch_id)` |
| `has_runner` | method | `estorides_core/monitoring.py:304` | `def has_runner(self)` |
| `history` | method | `estorides_core/monitoring.py:249` | `def history(self, watch_id, limit)` |
| `list_watches` | method | `estorides_core/monitoring.py:203` | `def list_watches(self, enabled_only)` |
| `record_run_complete` | method | `estorides_core/monitoring.py:236` | `def record_run_complete(self, history_id, status, entity_count, obs_count, error, alert_sent)` |
| `record_run_start` | method | `estorides_core/monitoring.py:226` | `def record_run_start(self, watch_id)` |
| `running` | method | `estorides_core/monitoring.py:300` | `def running(self)` |
| `set_alerter` | method | `estorides_core/monitoring.py:329` | `def set_alerter(self, alerter)` |
| `set_runner` | method | `estorides_core/monitoring.py:325` | `def set_runner(self, runner)` |
| `start` | method | `estorides_core/monitoring.py:308` | `def start(self)` |
| `stats` | method | `estorides_core/monitoring.py:266` | `def stats(self)` |
| `stop` | method | `estorides_core/monitoring.py:319` | `def stop(self)` |
| `to_dict` | method | `estorides_core/monitoring.py:110` | `def to_dict(self)` |
| `update_watch` | method | `estorides_core/monitoring.py:186` | `def update_watch(self, watch)` |
| `Observation` | class | `estorides_core/observation_models.py:109` | `class Observation(_StrictModel)` |
| `ObservationMeta` | class | `estorides_core/observation_models.py:72` | `class ObservationMeta(_StrictModel)` |
| `ObservedEntity` | class | `estorides_core/observation_models.py:147` | `class ObservedEntity(_StrictModel)` |
| `RunResult` | class | `estorides_core/observation_models.py:175` | `class RunResult(_StrictModel)` |
| `_StrictModel` | class | `estorides_core/observation_models.py:66` | `class _StrictModel(BaseModel)` |
| `_bound_url` | method | `estorides_core/observation_models.py:87` | `def _bound_url(cls, value)` |
| `_check_json_safe` | function | `estorides_core/observation_models.py:44` | `def _check_json_safe(value)` |
| `_json_safe` | method | `estorides_core/observation_models.py:125` | `def _json_safe(cls, value)` |
| `_json_safe` | method | `estorides_core/observation_models.py:160` | `def _json_safe(cls, value)` |
| `_upper_method` | method | `estorides_core/observation_models.py:92` | `def _upper_method(cls, value)` |
| `to_legacy_dict` | method | `estorides_core/observation_models.py:95` | `def to_legacy_dict(self)` |
| `to_legacy_dict` | method | `estorides_core/observation_models.py:128` | `def to_legacy_dict(self)` |
| `to_legacy_dict` | method | `estorides_core/observation_models.py:163` | `def to_legacy_dict(self)` |
| `to_legacy_dict` | method | `estorides_core/observation_models.py:183` | `def to_legacy_dict(self)` |
| `OntologyEngine` | class | `estorides_core/ontology.py:314` | `class OntologyEngine` |
| `SanctionEntry` | class | `estorides_core/ontology.py:70` | `class SanctionEntry` |
| `SanctionsIndex` | class | `estorides_core/ontology.py:96` | `class SanctionsIndex` |
| `WikidataCache` | class | `estorides_core/ontology.py:268` | `class WikidataCache` |
| `__init__` | method | `estorides_core/ontology.py:115` | `def __init__(self)` |
| `__init__` | method | `estorides_core/ontology.py:276` | `def __init__(self)` |
| `__init__` | method | `estorides_core/ontology.py:317` | `def __init__(self)` |
| `_candidate_fields` | method | `estorides_core/ontology.py:359` | `def _candidate_fields(source, parsed)` |
| `_download` | method | `estorides_core/ontology.py:201` | `def _download(self)` |
| `_index` | method | `estorides_core/ontology.py:255` | `def _index(self, entries)` |
| `_normalise_name` | function | `estorides_core/ontology.py:84` | `def _normalise_name(s)` |
| `_parse` | method | `estorides_core/ontology.py:226` | `def _parse(self, text)` |
| `_persist` | method | `estorides_core/ontology.py:213` | `def _persist(self, text)` |
| `_refresh` | method | `estorides_core/ontology.py:172` | `def _refresh(self)` |
| `check_observation` | method | `estorides_core/ontology.py:321` | `def check_observation(self, observation)` |
| `clear` | method | `estorides_core/ontology.py:308` | `def clear(self)` |
| `entries` | method | `estorides_core/ontology.py:134` | `def entries(self)` |
| `get` | method | `estorides_core/ontology.py:282` | `def get(self, kind, value)` |
| `is_ready` | method | `estorides_core/ontology.py:131` | `def is_ready(self)` |
| `lookup` | method | `estorides_core/ontology.py:141` | `def lookup(self, name)` |
| `lookup_crypto` | method | `estorides_core/ontology.py:151` | `def lookup_crypto(self, address)` |
| `put` | method | `estorides_core/ontology.py:296` | `def put(self, kind, value, payload)` |
| `size` | method | `estorides_core/ontology.py:168` | `def size(self)` |
| `stats` | method | `estorides_core/ontology.py:304` | `def stats(self)` |
| `to_dict` | method | `estorides_core/ontology.py:79` | `def to_dict(self)` |
| `build_openapi` | function | `estorides_core/openapi.py:14` | `def build_openapi(app)` |
| `OpsConfig` | class | `estorides_core/ops_observability.py:28` | `class OpsConfig` |
| `_clean_label` | function | `estorides_core/ops_observability.py:43` | `def _clean_label(value)` |
| `format_event` | function | `estorides_core/ops_observability.py:112` | `def format_event(fields, as_json)` |
| `health_payload` | function | `estorides_core/ops_observability.py:50` | `def health_payload()` |
| `project_root` | function | `estorides_core/ops_observability.py:130` | `def project_root()` |
| `ready_payload` | function | `estorides_core/ops_observability.py:55` | `def ready_payload(source_count, sources_dir_ok)` |
| `record_request` | function | `estorides_core/ops_observability.py:62` | `def record_request(endpoint, status)` |
| `record_source` | function | `estorides_core/ops_observability.py:72` | `def record_source(source, ok)` |
| `render_metrics` | function | `estorides_core/ops_observability.py:90` | `def render_metrics()` |
| `reset_metrics` | function | `estorides_core/ops_observability.py:83` | `def reset_metrics()` |
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
| `repl` | function | `estorides_core/orchestrator.py:122` | `def repl(m)` |
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
| `build_page_params` | function | `estorides_core/pagination.py:62` | `def build_page_params(cfg, page_num)` |
| `count_results` | function | `estorides_core/pagination.py:99` | `def count_results(data, cfg)` |
| `enabled` | method | `estorides_core/pagination.py:54` | `def enabled(self)` |
| `extract_cursor` | function | `estorides_core/pagination.py:78` | `def extract_cursor(data, cfg)` |
| `from_dict` | method | `estorides_core/pagination.py:38` | `def from_dict(raw)` |
| `needs_page_size` | method | `estorides_core/pagination.py:58` | `def needs_page_size(self)` |
| `_d` | function | `estorides_core/parsers.py:31` | `def _d(obj)` |
| `_first_dict` | function | `estorides_core/parsers.py:40` | `def _first_dict(items)` |
| `_list` | function | `estorides_core/parsers.py:47` | `def _list(obj)` |
| `_normalise_discord_server` | function | `estorides_core/parsers.py:1152` | `def _normalise_discord_server(raw)` |
| `_text` | function | `estorides_core/parsers.py:56` | `def _text(obj)` |
| `_vt_stats` | function | `estorides_core/parsers.py:290` | `def _vt_stats(attrs)` |
| `deco` | function | `estorides_core/parsers.py:1343` | `def deco(func)` |
| `get_parser` | function | `estorides_core/parsers.py:1322` | `def get_parser(name)` |
| `list_parsers` | function | `estorides_core/parsers.py:1351` | `def list_parsers()` |
| `parse_abuseipdb` | function | `estorides_core/parsers.py:274` | `def parse_abuseipdb(payload)` |
| `parse_adsbdb` | function | `estorides_core/parsers.py:1199` | `def parse_adsbdb(payload)` |
| `parse_adsblol_aircraft` | function | `estorides_core/parsers.py:1184` | `def parse_adsblol_aircraft(payload)` |
| `parse_arxiv` | function | `estorides_core/parsers.py:685` | `def parse_arxiv(payload)` |
| `parse_bgpview` | function | `estorides_core/parsers.py:376` | `def parse_bgpview(payload)` |
| `parse_blockchain_btc` | function | `estorides_core/parsers.py:752` | `def parse_blockchain_btc(payload)` |
| `parse_blockstream` | function | `estorides_core/parsers.py:769` | `def parse_blockstream(payload)` |
| `parse_celestrak_tle` | function | `estorides_core/parsers.py:1168` | `def parse_celestrak_tle(payload)` |
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
| `parse_hexdb_aircraft` | function | `estorides_core/parsers.py:1214` | `def parse_hexdb_aircraft(payload)` |
| `parse_hexdb_route` | function | `estorides_core/parsers.py:1222` | `def parse_hexdb_route(payload)` |
| `parse_hibp_breach` | function | `estorides_core/parsers.py:564` | `def parse_hibp_breach(payload)` |
| `parse_hibp_paste` | function | `estorides_core/parsers.py:582` | `def parse_hibp_paste(payload)` |
| `parse_http_headers` | function | `estorides_core/parsers.py:992` | `def parse_http_headers(payload)` |
| `parse_ipapi` | function | `estorides_core/parsers.py:176` | `def parse_ipapi(payload)` |
| `parse_ipapi_co` | function | `estorides_core/parsers.py:217` | `def parse_ipapi_co(payload)` |
| `parse_ipinfo` | function | `estorides_core/parsers.py:202` | `def parse_ipinfo(payload)` |
| `parse_ipwhois` | function | `estorides_core/parsers.py:256` | `def parse_ipwhois(payload)` |
| `parse_keybase` | function | `estorides_core/parsers.py:903` | `def parse_keybase(payload)` |
| `parse_launch_library` | function | `estorides_core/parsers.py:1206` | `def parse_launch_library(payload)` |
| `parse_malwarebazaar` | function | `estorides_core/parsers.py:530` | `def parse_malwarebazaar(payload)` |
| `parse_mastodon` | function | `estorides_core/parsers.py:887` | `def parse_mastodon(payload)` |
| `parse_microlink` | function | `estorides_core/parsers.py:802` | `def parse_microlink(payload)` |
| `parse_nominatim` | function | `estorides_core/parsers.py:438` | `def parse_nominatim(payload)` |
| `parse_nvd_cve` | function | `estorides_core/parsers.py:706` | `def parse_nvd_cve(payload)` |
| `parse_openalex` | function | `estorides_core/parsers.py:640` | `def parse_openalex(payload)` |
| `parse_opensky_states` | function | `estorides_core/parsers.py:1176` | `def parse_opensky_states(payload)` |
| `parse_opensky_track` | function | `estorides_core/parsers.py:1192` | `def parse_opensky_track(payload)` |
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
| `register_parser` | function | `estorides_core/parsers.py:1335` | `def register_parser(name, description)` |
| `CertRecord` | class | `estorides_core/pdns_monitor.py:40` | `class CertRecord` |
| `HistoricalSubdomain` | class | `estorides_core/pdns_monitor.py:13` | `class HistoricalSubdomain` |
| `IPRecord` | class | `estorides_core/pdns_monitor.py:27` | `class IPRecord` |
| `PDNSResult` | class | `estorides_core/pdns_monitor.py:55` | `class PDNSResult` |
| `analyse_pdns_data` | function | `estorides_core/pdns_monitor.py:80` | `def analyse_pdns_data(subdomains, ip_history, new_certs)` |
| `classify_subdomain_status` | function | `estorides_core/pdns_monitor.py:72` | `def classify_subdomain_status(fqdn, resolved_ips)` |
| `extract_sans_from_cert` | function | `estorides_core/pdns_monitor.py:76` | `def extract_sans_from_cert(cert)` |
| `to_dict` | method | `estorides_core/pdns_monitor.py:22` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/pdns_monitor.py:35` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/pdns_monitor.py:50` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/pdns_monitor.py:62` | `def to_dict(self)` |
| `BreachContext` | class | `estorides_core/people_intel.py:56` | `class BreachContext` |
| `BreachRecord` | class | `estorides_core/people_intel.py:15` | `class BreachRecord` |
| `Employee` | class | `estorides_core/people_intel.py:29` | `class Employee` |
| `PeopleIntelResult` | class | `estorides_core/people_intel.py:67` | `class PeopleIntelResult` |
| `_match_pattern` | function | `estorides_core/people_intel.py:136` | `def _match_pattern(local)` |
| `_severity_from_breaches` | function | `estorides_core/people_intel.py:143` | `def _severity_from_breaches(breaches)` |
| `analyse_employees` | function | `estorides_core/people_intel.py:176` | `def analyse_employees(employees, domain)` |
| `correlate_breaches` | function | `estorides_core/people_intel.py:153` | `def correlate_breaches(employees)` |
| `infer_email_pattern` | function | `estorides_core/people_intel.py:98` | `def infer_email_pattern(emails)` |
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
| `_on_source_done` | function | `estorides_core/pivot_engine.py:356` | `def _on_source_done(name, ok, status, elapsed_ms)` |
| `_on_source_result` | function | `estorides_core/pivot_engine.py:366` | `def _on_source_result(observation)` |
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
| `_canonical_id` | function | `estorides_core/recon_fusion.py:112` | `def _canonical_id(etype, value)` |
| `_classify_groups` | method | `estorides_core/recon_fusion.py:321` | `def _classify_groups(self, groups, query)` |
| `_corroboration_factor` | function | `estorides_core/recon_fusion.py:117` | `def _corroboration_factor(source_count)` |
| `_deduplicate` | method | `estorides_core/recon_fusion.py:219` | `def _deduplicate(self, observations)` |
| `_direct_match_query` | function | `estorides_core/recon_fusion.py:132` | `def _direct_match_query(value, query)` |
| `_extract_key_findings` | function | `estorides_core/recon_fusion.py:137` | `def _extract_key_findings(observations)` |
| `_freshness_factor` | function | `estorides_core/recon_fusion.py:124` | `def _freshness_factor(age_hours, max_hours)` |
| `_group_by_entity` | method | `estorides_core/recon_fusion.py:237` | `def _group_by_entity(self, observations, entities)` |
| `_normalize_value` | function | `estorides_core/recon_fusion.py:107` | `def _normalize_value(etype, value)` |
| `classify` | method | `estorides_core/recon_fusion.py:169` | `def classify(self, query, query_type, observations, entities)` |
| `ordered` | method | `estorides_core/recon_fusion.py:40` | `def ordered(cls)` |
| `to_dict` | method | `estorides_core/recon_fusion.py:64` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/recon_fusion.py:95` | `def to_dict(self)` |
| `run_passive_recon` | function | `estorides_core/recon_pipeline.py:22` | `def run_passive_recon(query, headers, html, cookies, employees, code_findings, third_parties, pdns_subdomains...` |
| `RelationshipInferer` | class | `estorides_core/relationship_inference.py:36` | `class RelationshipInferer(Protocol)` |
| `__call__` | method | `estorides_core/relationship_inference.py:51` | `def __call__(self, observation, query, kg)` |
| `_infer_abuseipdb` | function | `estorides_core/relationship_inference.py:143` | `def _infer_abuseipdb(observation, query, kg)` |
| `_infer_crtsh` | function | `estorides_core/relationship_inference.py:114` | `def _infer_crtsh(observation, query, kg)` |
| `_infer_dns` | function | `estorides_core/relationship_inference.py:105` | `def _infer_dns(observation, query, kg)` |
| `_infer_greynoise` | function | `estorides_core/relationship_inference.py:134` | `def _infer_greynoise(observation, query, kg)` |
| `_infer_ipapi` | function | `estorides_core/relationship_inference.py:186` | `def _infer_ipapi(observation, query, kg)` |
| `_infer_nvd` | function | `estorides_core/relationship_inference.py:208` | `def _infer_nvd(observation, query, kg)` |
| `_infer_otx` | function | `estorides_core/relationship_inference.py:195` | `def _infer_otx(observation, query, kg)` |
| `_infer_phonebook` | function | `estorides_core/relationship_inference.py:175` | `def _infer_phonebook(observation, query, kg)` |
| `_infer_shodan` | function | `estorides_core/relationship_inference.py:122` | `def _infer_shodan(observation, query, kg)` |
| `_infer_urlscan` | function | `estorides_core/relationship_inference.py:163` | `def _infer_urlscan(observation, query, kg)` |
| `_infer_whois` | function | `estorides_core/relationship_inference.py:152` | `def _infer_whois(observation, query, kg)` |
| `deco` | function | `estorides_core/relationship_inference.py:70` | `def deco(func)` |
| `infer_relationship` | function | `estorides_core/relationship_inference.py:78` | `def infer_relationship(observation, query, kg)` |
| `register_inferer` | function | `estorides_core/relationship_inference.py:63` | `def register_inferer(source_name)` |
| `ConfidenceInput` | class | `estorides_core/reliability_scoring.py:243` | `class ConfidenceInput` |
| `ConfidenceResult` | class | `estorides_core/reliability_scoring.py:263` | `class ConfidenceResult` |
| `Credibility` | class | `estorides_core/reliability_scoring.py:48` | `class Credibility(int, Enum)` |
| `SourceReliability` | class | `estorides_core/reliability_scoring.py:37` | `class SourceReliability(str, Enum)` |
| `SourceType` | class | `estorides_core/reliability_scoring.py:59` | `class SourceType(str, Enum)` |
| `__post_init__` | method | `estorides_core/reliability_scoring.py:253` | `def __post_init__(self)` |
| `_clamp01` | function | `estorides_core/reliability_scoring.py:302` | `def _clamp01(value)` |
| `_corroboration_weight` | function | `estorides_core/reliability_scoring.py:280` | `def _corroboration_weight(n)` |
| `_freshness_weight` | function | `estorides_core/reliability_scoring.py:287` | `def _freshness_weight(age_seconds, half_life_days)` |
| `_validate_score` | function | `estorides_core/reliability_scoring.py:297` | `def _validate_score(value, field_name)` |
| `compute_confidence` | function | `estorides_core/reliability_scoring.py:312` | `def compute_confidence(inp)` |
| `merge_confidence` | function | `estorides_core/reliability_scoring.py:350` | `def merge_confidence(existing, new_observation)` |
| `reliability_from_name` | function | `estorides_core/reliability_scoring.py:400` | `def reliability_from_name(source_name)` |
| `reliability_weight` | function | `estorides_core/reliability_scoring.py:430` | `def reliability_weight(source_name, overrides)` |
| `reliability_weight_for_letter` | function | `estorides_core/reliability_scoring.py:452` | `def reliability_weight_for_letter(letter)` |
| `source_type_from_name` | function | `estorides_core/reliability_scoring.py:415` | `def source_type_from_name(source_name)` |
| `CidrRule` | class | `estorides_core/scope.py:130` | `class CidrRule(ScopeRule)` |
| `ExactHostRule` | class | `estorides_core/scope.py:117` | `class ExactHostRule(ScopeRule)` |
| `RegexRule` | class | `estorides_core/scope.py:148` | `class RegexRule(ScopeRule)` |
| `ScopeMatcher` | class | `estorides_core/scope.py:234` | `class ScopeMatcher` |
| `ScopeReport` | class | `estorides_core/scope.py:344` | `class ScopeReport` |
| `ScopeRule` | class | `estorides_core/scope.py:89` | `class ScopeRule(ABC)` |
| `WildcardRule` | class | `estorides_core/scope.py:102` | `class WildcardRule(ScopeRule)` |
| `__init__` | method | `estorides_core/scope.py:242` | `def __init__(self, in_scope, out_of_scope)` |
| `_assets_from_json` | function | `estorides_core/scope.py:322` | `def _assets_from_json(doc)` |
| `_cidr_factory` | function | `estorides_core/scope.py:179` | `def _cidr_factory(text)` |
| `_exact_host_factory` | function | `estorides_core/scope.py:195` | `def _exact_host_factory(text)` |
| `_ip_factory` | function | `estorides_core/scope.py:188` | `def _ip_factory(text)` |
| `_regex_factory` | function | `estorides_core/scope.py:168` | `def _regex_factory(text)` |
| `_wildcard_factory` | function | `estorides_core/scope.py:161` | `def _wildcard_factory(text)` |
| `build_report` | function | `estorides_core/scope.py:371` | `def build_report(matcher, assets)` |
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
| `load_assets` | function | `estorides_core/scope.py:303` | `def load_assets(path)` |
| `load_rules_file` | function | `estorides_core/scope.py:285` | `def load_rules_file(path)` |
| `matches` | method | `estorides_core/scope.py:93` | `def matches(self, asset)` |
| `matches` | method | `estorides_core/scope.py:107` | `def matches(self, asset)` |
| `matches` | method | `estorides_core/scope.py:122` | `def matches(self, asset)` |
| `matches` | method | `estorides_core/scope.py:135` | `def matches(self, asset)` |
| `matches` | method | `estorides_core/scope.py:153` | `def matches(self, asset)` |
| `normalise_asset` | function | `estorides_core/scope.py:52` | `def normalise_asset(raw)` |
| `out_rules` | method | `estorides_core/scope.py:255` | `def out_rules(self)` |
| `parse_rule` | function | `estorides_core/scope.py:211` | `def parse_rule(line)` |
| `parse_rules` | function | `estorides_core/scope.py:223` | `def parse_rules(lines)` |
| `partition` | method | `estorides_core/scope.py:269` | `def partition(self, assets)` |
| `to_dict` | method | `estorides_core/scope.py:361` | `def to_dict(self)` |
| `write_flat_lists` | function | `estorides_core/scope.py:381` | `def write_flat_lists(report, out_dir)` |
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
| `_assert_clean` | function | `estorides_core/search_telemetry.py:167` | `def _assert_clean(label)` |
| `_default_config` | function | `estorides_core/search_telemetry.py:309` | `def _default_config()` |
| `context` | method | `estorides_core/search_telemetry.py:288` | `def context(self)` |
| `disallowed_brands_in` | function | `estorides_core/search_telemetry.py:75` | `def disallowed_brands_in(text)` |
| `emoji_in` | function | `estorides_core/search_telemetry.py:89` | `def emoji_in(text)` |
| `percent_encoded_emoji_in` | function | `estorides_core/search_telemetry.py:103` | `def percent_encoded_emoji_in(text)` |
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
| `_confidence_for_platform_matches` | function | `estorides_core/socmint.py:185` | `def _confidence_for_platform_matches(platform_count, has_verified, has_keybase)` |
| `_extract_profile_urls` | function | `estorides_core/socmint.py:164` | `def _extract_profile_urls(text)` |
| `discover_from_text` | method | `estorides_core/socmint.py:311` | `def discover_from_text(self, text)` |
| `platform_list` | method | `estorides_core/socmint.py:344` | `def platform_list(self)` |
| `resolve` | method | `estorides_core/socmint.py:218` | `def resolve(self, username, platforms)` |

Next: [SYMBOLS_p3.md](SYMBOLS_p3.md)
