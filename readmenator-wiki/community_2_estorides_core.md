# estorides_core

*Community 2 | 2 files | cohesion 0.33*

## Definition

This community groups 2 file(s) rooted at `estorides_core` with dominant language py (cohesion 0.33). Central symbols: `DnsreconResult`, `NiktoResult`, `NmapResult`, `SqlmapResult`, `TestDnsreconResult`, `TestErrorResultsFlowThrough`, `TestNiktoResult`, `TestNmapResult`. Core file: `estorides_core/active_recon.py` (25 symbols). Documented purpose: ATDD + BDD tests for estorides_core.active_recon.  Implements the Given-When-Then contracts declared in ``spec/active_recon.md``. Property-based invariants live.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/active_recon.py` | py | utility | 25 | no |
| `tests/test_active_recon.py` | py | testing | 24 | yes |

## Key Symbols

- `NmapResult` (class, `estorides_core/active_recon.py:13`) `class NmapResult`
- `to_dict` (method, `estorides_core/active_recon.py:24`) `def to_dict(self)`
- `to_entities` (method, `estorides_core/active_recon.py:27`) `def to_entities(self)`
- `NiktoResult` (class, `estorides_core/active_recon.py:32`) `class NiktoResult`
- `to_dict` (method, `estorides_core/active_recon.py:41`) `def to_dict(self)`
- `to_entities` (method, `estorides_core/active_recon.py:44`) `def to_entities(self)`
- `SqlmapResult` (class, `estorides_core/active_recon.py:49`) `class SqlmapResult`
- `to_dict` (method, `estorides_core/active_recon.py:58`) `def to_dict(self)`
- `to_entities` (method, `estorides_core/active_recon.py:61`) `def to_entities(self)`
- `DnsreconResult` (class, `estorides_core/active_recon.py:66`) `class DnsreconResult`
- `to_dict` (method, `estorides_core/active_recon.py:77`) `def to_dict(self)`
- `to_entities` (method, `estorides_core/active_recon.py:80`) `def to_entities(self)`
- `TheHarvesterResult` (class, `estorides_core/active_recon.py:85`) `class TheHarvesterResult`
- `to_dict` (method, `estorides_core/active_recon.py:95`) `def to_dict(self)`
- `to_entities` (method, `estorides_core/active_recon.py:98`) `def to_entities(self)`
- `_parse_nmap_stdout` (method, `estorides_core/active_recon.py:102`) `def _parse_nmap_stdout(stdout, tool_name)`
- `_parse_nikto_stdout` (method, `estorides_core/active_recon.py:125`) `def _parse_nikto_stdout(stdout, tool_name)`
- `_parse_sqlmap_stdout` (method, `estorides_core/active_recon.py:144`) `def _parse_sqlmap_stdout(stdout, tool_name)`
- `_parse_dnsrecon_stdout` (method, `estorides_core/active_recon.py:171`) `def _parse_dnsrecon_stdout(stdout, tool_name)`
- `_parse_harvester_stdout` (method, `estorides_core/active_recon.py:188`) `def _parse_harvester_stdout(stdout, tool_name)`
- `run_nmap` (method, `estorides_core/active_recon.py:213`) `def run_nmap(target, args)`
- `run_nikto` (method, `estorides_core/active_recon.py:243`) `def run_nikto(target, args)`
- `run_sqlmap` (method, `estorides_core/active_recon.py:269`) `def run_sqlmap(target, args)`
- `run_dnsrecon` (method, `estorides_core/active_recon.py:295`) `def run_dnsrecon(target, args)`
- `run_theHarvester` (method, `estorides_core/active_recon.py:325`) `def run_theHarvester(target, args)`
- `TestNmapResult` (class, `tests/test_active_recon.py:24`) `class TestNmapResult`
- `test_run_nmap_returns_result` (method, `tests/test_active_recon.py:25`) `def test_run_nmap_returns_result(self)`
- `test_nmap_result_has_to_dict` (method, `tests/test_active_recon.py:29`) `def test_nmap_result_has_to_dict(self)`
- `test_nmap_result_to_entities_is_list` (method, `tests/test_active_recon.py:38`) `def test_nmap_result_to_entities_is_list(self)`
- `TestNiktoResult` (class, `tests/test_active_recon.py:45`) `class TestNiktoResult`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 1
- Cross-boundary resolved imports (EXTRACTED): 2

## Connections

- [EXTRACTED] depends_on community 2 <-> 6 (strength 0.9): Extracted import edge crosses communities: estorides_core/active_recon.py imports estorides_core/tool_runner.py.
- [INFERRED] shares_context community 0 <-> 2 (strength 0.5): Inferred shared context (language py) with no import path between community 0 (root) and community 2 (estorides_core).
- [INFERRED] shares_context community 1 <-> 2 (strength 0.5): Inferred shared context (language py and layer testing) with no import path between community 1 (tests) and community 2 (estorides_core).

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `estorides_core/active_recon.py`)? What purpose do they serve?
- What would break if the most connected file in estorides_core changed?
- Should estorides_core be split, given cohesion 0.33?

## Sources

- `estorides_core/active_recon.py`
- `tests/test_active_recon.py`
