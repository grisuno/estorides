# estorides_core: tool_install

*Community 6 | 10 files | cohesion 0.43*

## Definition

This community groups 10 file(s) rooted at `tests` with dominant language py (cohesion 0.43). Central symbols: `DnsreconResult`, `InstallRecipe`, `InstallResult`, `NiktoResult`, `NmapResult`, `Query`, `QueryValidationError`, `SqlmapResult`. Core file: `tests/test_tool_runner.py` (29 symbols). Documented purpose: estorides_core.tool_install.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/active_recon.py` | py | utility | 25 | no |
| `estorides_core/tool_install.py` | py | utility | 27 | yes |
| `estorides_core/tool_runner.py` | py | utility | 15 | no |
| `estorides_core/validation.py` | py | utility | 6 | yes |
| `tests/properties/test_tool_runner_properties.py` | py | testing | 3 | yes |
| `tests/test_active_recon.py` | py | testing | 24 | yes |
| `tests/test_central_config.py` | py | testing | 3 | yes |
| `tests/test_tool_doctor.py` | py | testing | 4 | yes |
| `tests/test_tool_install.py` | py | testing | 28 | yes |
| `tests/test_tool_runner.py` | py | testing | 29 | yes |

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
- `InstallRecipe` (class, `estorides_core/tool_install.py:81`) `class InstallRecipe` - One tool's install recipe, loaded from ``tool_recipes/<name>.yaml``.
- `has_apt` (method, `estorides_core/tool_install.py:95`) `def has_apt(self)`
- `has_git` (method, `estorides_core/tool_install.py:98`) `def has_git(self)`
- `InstallResult` (class, `estorides_core/tool_install.py:103`) `class InstallResult` - Outcome of one ``install_tool`` invocation. Failures are values.
- `to_dict` (method, `estorides_core/tool_install.py:113`) `def to_dict(self)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 13
- Cross-boundary resolved imports (EXTRACTED): 16

## Connections

- [EXTRACTED] depends_on community 5 <-> 6 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/validation.py.
- [EXTRACTED] depends_on community 1 <-> 6 (strength 0.9): Extracted import edge crosses communities: estorides_core/system_app_sources.py imports estorides_core/tool_runner.py.
- [EXTRACTED] depends_on community 6 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_core/tool_install.py imports estorides_core/config.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- Why do 2 file(s) lack file-level docs (e.g. `estorides_core/active_recon.py`)? What purpose do they serve?
- What would break if the most connected file in estorides_core: tool_install changed?
- Should estorides_core: tool_install be split, given cohesion 0.43?

## Sources

- `estorides_core/active_recon.py`
- `estorides_core/tool_install.py`
- `estorides_core/tool_runner.py`
- `estorides_core/validation.py`
- `tests/properties/test_tool_runner_properties.py`
- `tests/test_active_recon.py`
- `tests/test_central_config.py`
- `tests/test_tool_doctor.py`
- `tests/test_tool_install.py`
- `tests/test_tool_runner.py`
