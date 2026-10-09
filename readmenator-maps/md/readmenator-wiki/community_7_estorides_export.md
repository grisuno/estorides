# estorides_export

*Community 7 | 8 files | cohesion 0.45*

## Definition

This community groups 8 file(s) rooted at `estorides_export` with dominant language py (cohesion 0.45). Central symbols: `KnowledgeGraph`, `ReportMetadata`, `ReportResult`, `ReportSection`, `TestCredentialsRedacted`, `TestExecutiveSummaryFindings`, `TestFullReport`, `TestMinimalReport`. Core file: `tests/test_recon_report.py` (19 symbols). Documented purpose: estorides_core.knowledge_graph.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/knowledge_graph.py` | py | utility | 17 | yes |
| `estorides_export/__init__.py` | py | utility | 0 | yes |
| `estorides_export/encryption.py` | py | utility | 4 | yes |
| `estorides_export/misp.py` | py | utility | 3 | yes |
| `estorides_export/recon_report.py` | py | utility | 11 | no |
| `estorides_export/stix.py` | py | utility | 4 | yes |
| `tests/test_encrypted_export.py` | py | testing | 9 | yes |
| `tests/test_recon_report.py` | py | testing | 19 | yes |

## Key Symbols

- `_node_sources` (function, `estorides_core/knowledge_graph.py:73`) `def _node_sources(node)` - Read the distinct source set off a node, tolerating GraphML's
- `KnowledgeGraph` (class, `estorides_core/knowledge_graph.py:90`) `class KnowledgeGraph`
- `__init__` (method, `estorides_core/knowledge_graph.py:91`) `def __init__(self, name)`
- `add_entity` (method, `estorides_core/knowledge_graph.py:97`) `def add_entity(self, entity)` - Insert an entity. Returns the node id used.
- `add_observation` (method, `estorides_core/knowledge_graph.py:127`) `def add_observation(self, source, entities)` - Add every entity + every co-occurrence edge within the same response.
- `add_relationship` (method, `estorides_core/knowledge_graph.py:142`) `def add_relationship(self, src_type, src_value, rel, dst_type, dst_value)`
- `export_graphml` (method, `estorides_core/knowledge_graph.py:164`) `def export_graphml(self, path)`
- `export_json` (method, `estorides_core/knowledge_graph.py:183`) `def export_json(self)`
- `summary` (method, `estorides_core/knowledge_graph.py:197`) `def summary(self)`
- `top_entities` (method, `estorides_core/knowledge_graph.py:215`) `def top_entities(self, n, by)`
- `communities` (method, `estorides_core/knowledge_graph.py:235`) `def communities(self, nodes)` - Partition entity nodes into communities (clusters).
- `intel_level` (method, `estorides_core/knowledge_graph.py:266`) `def intel_level(self, node_id, bridge_nodes)` - Classify a node into the intelligence pipeline tier.
- `ego_subgraph` (method, `estorides_core/knowledge_graph.py:311`) `def ego_subgraph(self, node_id, radius)`
- `neighbours` (method, `estorides_core/knowledge_graph.py:322`) `def neighbours(self, node_id, relation)`
- `_node_id` (method, `estorides_core/knowledge_graph.py:338`) `def _node_id(self, kind, value)`
- `_source_node` (method, `estorides_core/knowledge_graph.py:341`) `def _source_node(self, source)`
- `_node_color` (method, `estorides_core/knowledge_graph.py:351`) `def _node_color(self, ent_type)`
- `_have_age` (function, `estorides_export/encryption.py:47`) `def _have_age()`
- `encrypt_file` (function, `estorides_export/encryption.py:51`) `def encrypt_file(plaintext_path, recipient_pubkey)` - Encrypt `plaintext_path` to `<plaintext_path>.age` for the recipient.
- `export_stix_encrypted` (function, `estorides_export/encryption.py:100`) `def export_stix_encrypted(kg, recipient_pubkey, path)` - Build the STIX bundle, write to disk, encrypt to <path>.age.
- `export_misp_encrypted` (function, `estorides_export/encryption.py:128`) `def export_misp_encrypted(kg, recipient_pubkey, path)`
- `event_from_graph` (function, `estorides_export/misp.py:36`) `def event_from_graph(kg)`
- `_category` (function, `estorides_export/misp.py:65`) `def _category(ent_type)`
- `export` (function, `estorides_export/misp.py:79`) `def export(kg, path)`
- `ReportMetadata` (class, `estorides_export/recon_report.py:23`) `class ReportMetadata`
- `__post_init__` (method, `estorides_export/recon_report.py:29`) `def __post_init__(self)`
- `to_dict` (method, `estorides_export/recon_report.py:35`) `def to_dict(self)`
- `ReportSection` (class, `estorides_export/recon_report.py:40`) `class ReportSection`
- `to_dict` (method, `estorides_export/recon_report.py:46`) `def to_dict(self)`
- `ReportResult` (class, `estorides_export/recon_report.py:51`) `class ReportResult`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 15
- Cross-boundary resolved imports (EXTRACTED): 13

## Connections

- [EXTRACTED] depends_on community 2 <-> 7 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/knowledge_graph.py.
- [EXTRACTED] depends_on community 7 <-> 3 (strength 0.9): Extracted import edge crosses communities: estorides_core/knowledge_graph.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 7 <-> 8 (strength 0.9): Extracted import edge crosses communities: estorides_core/knowledge_graph.py imports estorides_core/entity_extraction.py.
- [EXTRACTED] depends_on community 1 <-> 7 (strength 0.9): Extracted import edge crosses communities: estorides_core/orchestrator.py imports estorides_core/knowledge_graph.py.

## Risks

- [cycle] `estorides_export/__init__.py` -> `estorides_export/encryption.py` -> `estorides_export/__init__.py`
- [cycle] `estorides_export/__init__.py` -> `estorides_export/encryption.py` -> `estorides_export/__init__.py`

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `estorides_export/recon_report.py`)? What purpose do they serve?
- Can the cycle `estorides_export/__init__.py` -> `estorides_export/encryption.py` be broken with an interface?
- What would break if the most connected file in estorides_export changed?
- Should estorides_export be split, given cohesion 0.45?

## Sources

- `estorides_core/knowledge_graph.py`
- `estorides_export/__init__.py`
- `estorides_export/encryption.py`
- `estorides_export/misp.py`
- `estorides_export/recon_report.py`
- `estorides_export/stix.py`
- `tests/test_encrypted_export.py`
- `tests/test_recon_report.py`
