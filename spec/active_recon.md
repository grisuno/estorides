# active_recon — Kali CLI Tool Wrappers for Estorides

## Purpose
`active_recon` wraps every pre-installed Kali OSINT CLI tool into a typed estorides `Result` dataclass, normalising output to the same entity format used by passive HTTP sources. Each wrapper calls `tool_runner.run_tool()` and parses the tool's stdout into a structured result. This enables estorides to run active reconnaissance (nmap, nikto, dnsrecon, etc.) alongside its existing passive fingerprinting and intelligence gathering — all under the same security guarantees, audit trail, and fusion pipeline.

## Inputs

Each wrapper function accepts a single `target: str` (already validated by the orchestrator) plus an optional `args: list[str]` for tool-specific flags.

| Wrapper | target type | default args | extra config |
|---------|------------|--------------|--------------|
| `run_nmap` | domain, ipv4, ipv6 | `["-sV", "-T4", "-p", "22,80,443"]` | `nmap_script` (extra NSE scripts) |
| `run_nikto` | domain, url | `["-h", target]` | `nikto_timeout` |
| `run_sqlmap` | url | `["-u", target, "--batch", "--level=3", "--risk=2"]` | `sqlmap_timeout` |
| `run_dnsrecon` | domain | `["-d", target, "-t", "std"]` | `dnsrecon_timeout` |
| `run_dnsenum` | domain | `["--noreverse", target]` | `dnsenum_timeout` |
| `run_theHarvester` | domain | `["-d", target, "-b", "all"]` | `harvester_timeout` |
| `run_whatweb` | domain, url | `["--color=0", target]` | `whatweb_timeout` |
| `run_wafw00f` | url | `["-u", target]` | `wafw00f_timeout` |
| `run_sslscan` | domain, host | `[target]` | `sslscan_timeout` |
| `run_sslyze` | domain, host | `[target]` | `sslyze_timeout` |
| `run_aircrack` | bssid | `["-b", target]` | requires monitor mode pre-config |
| `run_enum4linux` | ipv4 | `["-a", target]` | `enum4linux_timeout` |
| `run_smbclient` | host | `["-L", target]` | `smbclient_timeout` |
| `run_nbtscan` | ipv4_range | `[target]` | `nbtscan_timeout` |
| `run_snmpwalk` | ipv4 | `["-v", "2c", "-c", "public", target, "1.3.6.1.2.1.1"]` | `snmp_timeout` |
| `run_amass` | domain | `["enum", "-passive", "-d", target]` | `amass_timeout` |
| `run_bulk_extractor` | image_file | `[target]` | `bulk_extractor_timeout` |
| `run_binwalk` | firmware_file | [`target`] | `binwalk_timeout` |
| `run_radare2` | binary | `["-q", "-c", "aaa; afl", target]` | `radare2_timeout` |
| `run_john` | hash_file | `["--format=auto", target]` | `john_timeout` |
| `run_hashcat` | hash_file | `["-m", "0", target, "/usr/share/wordlists/rockyou.txt"]` | `hashcat_timeout` |
| `run_hydra` | host | `["-l", "admin", "-P", "/usr/share/wordlists/rockyou.txt", target, http-get"]` | `hydra_timeout` |
| `run_wfuzz` | url | `["-c", target, "-z", "file,/usr/share/wordlists/dirb/common.txt"]` | `wfuzz_timeout` |
| `run_ffuf` | url | `["-u", target, "-w", "/usr/share/wordlists/dirb/common.txt"]` | `ffuf_timeout` |
| `run_dirb` | url | `[target, "/usr/share/wordlists/dirb/common.txt"]` | `dirb_timeout` |
| `run_gobuster` | url | `["dir", "-u", target, "-w", "/usr/share/wordlists/dirb/common.txt"]` | `gobuster_timeout` |
| `run_feroxbuster` | url | `["-u", target, "-w", "/usr/share/wordlists/dirb/common.txt"]` | `feroxbuster_timeout` |
| `run_nuclei` | url | `["-u", target, "-tags", "cve,default-credentials"]` | `nuclei_timeout` |
| `run_tcpdump` | interface | `["-c", "100", "-i", target]` | `tcpdump_timeout` |
| `run_tshark` | interface | `["-c", "100", "-i", target]` | `tshark_timeout` |

## Outputs

Each wrapper returns a typed dataclass (e.g., `NmapResult`) with:

```
ToolSpecificResult {
  tool_name: str                # e.g. "nmap"
  success: bool                 # True if exit_code == 0
  exit_code: int
  entities: list[dict]          # normalised estorides entities
  raw_result: str               # parsed/summarised output
  confidence: float             # 0-1 per-result confidence
  metadata: dict[str, Any]     # tool-specific extra data
  error: str | None             # error message if tool failed
}

# Or unified via ToolResult.to_dict() when fed into the fusion pipeline
```

## Tabla de errores

| Condition | Code | Behaviour |
|-----------|------|-----------|
| Tool binary not found | `TOOL_NOT_FOUND` | Return result with `success=False`, `error="binary not found on filesystem"`, no subprocess spawned |
| Tool not in allowlist | `TOOL_NOT_ALLOWED` | Return result with `success=False`, `error="tool not in allowlist"`, no subprocess spawned |
| Argument injection detected | `TOOL_INJECTION` | Return result with `success=False`, `error="shell injection detected in args"`, no subprocess spawned |
| Subprocess timeout | `TOOL_TIMEOUT` | Kill process group, return result with `success=False`, `error="tool timed out"`, partial stdout parsed if possible |
| Subprocess exits non-zero | `TOOL_CRASH` | Return result with `success=False`, attempt to parse stdout anyway, log warning |
| Output exceeds size cap | `OUTPUT_TOO_LARGE` | Truncate stdout, flag `truncated=True`, continue parsing |
| Unicode decode error | `OUTPUT_DECODE_ERR` | Replace undecodable bytes with U+FFFD, continue processing |
| No entities extracted from stdout | `NO_ENTITIES` | Return result with empty `entities` list, `success` based on exit code |

## Garantias de seguridad

1. **Zero shell execution** — `tool_runner.run_tool()` always uses `shell=False` with an argument list.
2. **Allowlist enforcement** — `TOOL_ALLOWLIST` is defined in `config.py` and env-overridable via `ESTORIDES_TOOL_ALLOWLIST`.
3. **Metacharacter blocking** — every arg is checked against the injection character set (`;`, `|`, `&&`, `||`, `` ` ``, `$()`, `\n`, `\r`).
4. **Path resolution** — `shutil.which()` resolves the binary path; no relative paths are passed to subprocess.
5. **Timeout enforcement** — each tool has a configurable timeout (default 300s, max 3600s).
6. **Output size cap** — stdout+stderr capped at 10MB.
7. **Audit logging** — every invocation logged at `INFO` with sanitised args, target, exit code, duration, output SHA1.
8. **Input validation** — target strings pass through `validate_query()` before being used as arguments.
9. **No eval/exec** — zero use of `eval`, `exec`, `os.system`, or `compile`.
10. **Isolation** — each tool call is an independent subprocess; failures in one tool never affect others.

## Out of scope

- **Wireless monitor mode setup** — `airmon-ng` start is assumed pre-configured by the operator.
- **Tool installation** — `active_recon` does not install Kali packages.
- **Interactive tools** — tools requiring stdin/tty interaction are excluded.
- **GUI tools** — only CLI tools are supported.
- **Container/sandbox breakout** — `tool_runner` does not use seccomp or namespaces; it relies on subprocess isolation.
- **CWE-78 (OS Command Injection) fixes** — those are handled by the `tool_runner.py` security layer.

## Escenarios BDD (Given-When-Then)

### S1 [Happy path] nmap returns parsed open ports and entities

Given `target = "scanme.nmap.org"` passes `validate_query()`
And `nmap` is in `TOOL_ALLOWLIST` and present on the filesystem
When `run_nmap("scanme.nmap.org")` is called
Then `result.success == True` (or partial success if nmap exits non-zero)
And `result.entities` contains at least one `ipv4` entity (scanme.nmap.org's IP)
And `result.entities` contains at least one `port` observation (22, 80, 443)
And `result.confidence >= 0.5`
And `result.raw_result` contains the nmap output summary

### S2 [Happy path] dnsrecon returns subdomains for a domain

Given `target = "example.com"` passes `validate_query()`
And `dnsrecon` is in `TOOL_ALLOWLIST` and present on the filesystem
When `run_dnsrecon("example.com")` is called
Then `result.entities` contains `domain` typed entities for discovered subdomains
And `result.raw_result` contains the dnsrecon output
And no subprocess was spawned with shell=True

### S3 [Edge] nikto on an unreachable target returns partial result

Given `target = "192.0.2.1"` (TEST-NET, unreachable)
When `run_nikto("192.0.2.1")` is called
Then `result.success == False` or `result.success == True` with empty entities
And `result.exit_code != 0` (nmap/nikto exit non-zero on unreachable)
And `result.error` is set with the stderr content
And no exception propagates to the caller
And `result.entities` is an empty list (not None)

### S4 [Security] args containing `; rm -rf /` are blocked

Given `args = ["-sV", "example.com; rm -rf /"]`
When `run_nmap("example.com", args=["-sV", "example.com; rm -rf /"])` is called
Then no subprocess is spawned
And `result.success == False`
And `result.error` contains "injection" or "metacharacter"
And a security log entry is written

### S5 [Edge] tool not installed returns TOOL_NOT_FOUND

Given `target = "example.com"`
When `run_nonexistent_tool("example.com")` is called (hypothetical wrapper for a tool not on the filesystem)
Then `result.success == False`
And `result.error == "binary not found on filesystem"`
And no subprocess was spawned

### S6 [Security] target passed through validate_query()

Given `target = "<script>alert(1)</script>"` (adversarial input)
When `run_nmap("<script>alert(1)</script>")` is called internally
Then `validate_query()` rejects the target or normalises it
And the target is never passed as an argument to the subprocess without sanitisation
And a `QueryValidationError` is raised before any subprocess invocation

### S7 [Edge] tool that exits non-zero but produces valid output

Given a tool configured to exit with code 1 but write valid results to stdout
When the tool is called
Then `result.success == False` (exit_code != 0)
But `result.entities` contains entities parsed from stdout
And `result.raw_result` is populated
And a warning is logged but no exception propagates

### S8 [Security] tool not in TOOL_ALLOWLIST is rejected

Given `tool_name = "malware_c2"` (not in `TOOL_ALLOWLIST`)
When `run_tool("malware_c2", ["--help"], target="example.com")` is called
Then `result.success == False`
And `result.error_code == "TOOL_NOT_ALLOWED"`
And no subprocess is spawned
And a security warning is logged