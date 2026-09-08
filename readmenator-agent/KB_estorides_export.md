# Subsystem: estorides_export

## estorides_export/__init__.py
- Layer: utility
- Language: py
- Depends on: `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/recon_report.py`, `estorides_export/report.py`, `estorides_export/stix.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`

## estorides_export/encryption.py
- Layer: utility
- Language: py
- Symbols:
  - `_have_age` (function, line 47) `def _have_age()`
  - `encrypt_file` (function, line 51) `def encrypt_file(plaintext_path, recipient_pubkey)`
  - `export_stix_encrypted` (function, line 100) `def export_stix_encrypted(kg, recipient_pubkey, path)`
  - `export_misp_encrypted` (function, line 128) `def export_misp_encrypted(kg, recipient_pubkey, path)`
- Depends on: `estorides_core/knowledge_graph.py`
- Imported by: `estorides_export/__init__.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_encrypted_export.py`, `tests/test_encrypted_export.py`

## estorides_export/misp.py
- Layer: utility
- Language: py
- Symbols:
  - `event_from_graph` (function, line 36) `def event_from_graph(kg)`
  - `_category` (function, line 65) `def _category(ent_type)`
  - `export` (function, line 79) `def export(kg, path)`
- Depends on: `estorides_core/config.py`, `estorides_core/knowledge_graph.py`
- Imported by: `estorides_export/__init__.py`

## estorides_export/recon_report.py
- Layer: utility
- Language: py
- Symbols:
  - `ReportMetadata` (class, line 23) `class ReportMetadata`
  - `ReportSection` (class, line 40) `class ReportSection`
  - `ReportResult` (class, line 51) `class ReportResult`
  - `redact_sensitive` (method, line 61) `def redact_sensitive(text)`
  - `build_subdomain_tree` (method, line 67) `def build_subdomain_tree(subdomains)`
  - `build_executive_summary` (method, line 92) `def build_executive_summary(critical_findings, total_targets, domain)`
  - `generate_report` (method, line 114) `def generate_report(query, target_scoring, metadata)`
  - `__post_init__` (method, line 29) `def __post_init__(self)`
  - `to_dict` (method, line 35) `def to_dict(self)`
  - `to_dict` (method, line 46) `def to_dict(self)`
  - `to_dict` (method, line 57) `def to_dict(self)`
- Imported by: `estorides_export/__init__.py`, `tests/test_recon_report.py`, `tests/test_recon_report.py`

## estorides_export/report.py
- Layer: utility
- Language: py
- Symbols:
  - `_tldr` (function, line 37) `def _tldr(case, entities, sources_queried, sources_succeeded, diff)`
  - `_iocs` (function, line 77) `def _iocs(entities)`
  - `_diff_section` (function, line 121) `def _diff_section(diff)`
  - `_analysis` (function, line 156) `def _analysis(case)`
  - `_meta_footer` (function, line 177) `def _meta_footer(case, sources_queried, sources_succeeded)`
  - `render_markdown_report` (function, line 194) `def render_markdown_report(case, entities, sources_queried, sources_succeeded, diff)`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_export/__init__.py`, `static/js/estorides.js`

## estorides_export/stix.py
- Layer: utility
- Language: py
- Symbols:
  - `_id` (function, line 28) `def _id(stix_type)`
  - `_now` (function, line 32) `def _now()`
  - `bundle_from_graph` (function, line 55) `def bundle_from_graph(kg)`
  - `export` (function, line 145) `def export(kg, path)`
- Depends on: `estorides_core/config.py`, `estorides_core/knowledge_graph.py`
- Imported by: `estorides_export/__init__.py`
