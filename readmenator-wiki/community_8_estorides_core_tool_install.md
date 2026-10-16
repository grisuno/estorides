# estorides_core: tool_install

*Community 8 | 12 files | cohesion 0.46*

## Definition

This community groups 12 file(s) rooted at `tests` with dominant language py (cohesion 0.46). Central symbols: `DnsreconResult`, `InstallRecipe`, `InstallResult`, `LanScanResult`, `NiktoResult`, `NmapResult`, `Query`, `QueryValidationError`. Core file: `tests/test_tool_runner.py` (29 symbols). Documented purpose: estorides_core.lan_runner.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/active_recon.py` | py | utility | 25 | no |
| `estorides_core/lan_runner.py` | py | utility | 8 | yes |
| `estorides_core/tool_install.py` | py | utility | 27 | yes |
| `estorides_core/tool_runner.py` | py | utility | 15 | no |
| `estorides_core/validation.py` | py | utility | 6 | yes |
| `tests/properties/test_tool_runner_properties.py` | py | testing | 3 | yes |
| `tests/test_active_recon.py` | py | testing | 24 | yes |
| `tests/test_central_config.py` | py | testing | 3 | yes |
| `tests/test_lan_runner.py` | py | testing | 14 | yes |
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
- `_parse_nmap_stdout` (function, `estorides_core/active_recon.py:102`) `def _parse_nmap_stdout(stdout, tool_name)`
- `_parse_nikto_stdout` (function, `estorides_core/active_recon.py:125`) `def _parse_nikto_stdout(stdout, tool_name)`
- `_parse_sqlmap_stdout` (function, `estorides_core/active_recon.py:144`) `def _parse_sqlmap_stdout(stdout, tool_name)`
- `_parse_dnsrecon_stdout` (function, `estorides_core/active_recon.py:171`) `def _parse_dnsrecon_stdout(stdout, tool_name)`
- `_parse_harvester_stdout` (function, `estorides_core/active_recon.py:188`) `def _parse_harvester_stdout(stdout, tool_name)`
- `run_nmap` (function, `estorides_core/active_recon.py:213`) `def run_nmap(target, args)`
- `run_nikto` (function, `estorides_core/active_recon.py:243`) `def run_nikto(target, args)`
- `run_sqlmap` (function, `estorides_core/active_recon.py:269`) `def run_sqlmap(target, args)`
- `run_dnsrecon` (function, `estorides_core/active_recon.py:295`) `def run_dnsrecon(target, args)`
- `run_theHarvester` (function, `estorides_core/active_recon.py:325`) `def run_theHarvester(target, args)`
- `LanScanResult` (class, `estorides_core/lan_runner.py:41`) `class LanScanResult` - Outcome of a LAN scan. Refusals and errors are values.
- `to_dict` (method, `estorides_core/lan_runner.py:56`) `def to_dict(self)`
- `read_arp_table` (function, `estorides_core/lan_runner.py:60`) `def read_arp_table()` - Read the local neighbor table. Fail-soft, no probes sent.
- `read_dhcp_leases` (function, `estorides_core/lan_runner.py:81`) `def read_dhcp_leases()` - Read the first readable dnsmasq lease file. Fail-soft.
- `_default_runner` (function, `estorides_core/lan_runner.py:93`) `def _default_runner()`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 15
- Cross-boundary resolved imports (EXTRACTED): 17

## Connections

- [EXTRACTED] depends_on community 4 <-> 8 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/validation.py.
- [EXTRACTED] depends_on community 1 <-> 8 (strength 0.9): Extracted import edge crosses communities: estorides_core/system_app_sources.py imports estorides_core/tool_runner.py.
- [EXTRACTED] depends_on community 8 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_core/tool_install.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 8 <-> 7 (strength 0.9): Extracted import edge crosses communities: estorides_core/tool_runner.py imports estorides_core/entity_extraction.py.
- [EXTRACTED] depends_on community 0 <-> 8 (strength 0.9): Extracted import edge crosses communities: estorides_web.py imports estorides_core/validation.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- Why do 2 file(s) lack file-level docs (e.g. `estorides_core/active_recon.py`)? What purpose do they serve?
- What would break if the most connected file in estorides_core: tool_install changed?
- Should estorides_core: tool_install be split, given cohesion 0.46?

## Sources

- `estorides_core/active_recon.py`
- `estorides_core/lan_runner.py`
- `estorides_core/tool_install.py`
- `estorides_core/tool_runner.py`
- `estorides_core/validation.py`
- `tests/properties/test_tool_runner_properties.py`
- `tests/test_active_recon.py`
- `tests/test_central_config.py`
- `tests/test_lan_runner.py`
- `tests/test_tool_doctor.py`
- `tests/test_tool_install.py`
- `tests/test_tool_runner.py`
