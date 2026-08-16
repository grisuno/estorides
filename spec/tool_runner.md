# tool_runner — Safe CLI Tool Execution

## Purpose
Estorides currently executes all OSINT sources via HTTP (aiohttp). This module adds a safe subprocess executor that invokes Kali Linux CLI tools (nmap, nikto, dnsrecon, etc.) without command injection. Every tool call is guarded by: argument-list-only execution (no shell), an allowlist of permitted binaries, input validation, output size caps, timeouts, and audit logging. The result is normalised to the estorides entity format so it feeds the same recon_fusion and target_scoring pipeline as passive HTTP sources.

## Inputs

- `tool_name: str` — name of the binary to execute. Must be in `TOOL_ALLOWLIST`.
- `args: list[str]` — argument list passed directly to `subprocess.run()`. No shell expansion.
- `target: str` — the OSINT query (domain, IP, email, etc.) being investigated. Already validated by `validate_query()`.
- `timeout: int` — maximum seconds before the subprocess is killed. Default from `config.TOOL_TIMEOUT` (300s).
- `max_output_bytes: int` — cap on stdout+stderr combined. Default 10MB.
- `cwd: str | None` — optional working directory for the subprocess (default:
  inherit). Added 2026-08-16 for `system_app_sources`, which runs tools inside
  a private TemporaryDirectory so they can never write into the repo or `/tmp`
  with a predictable path. Existing callers are unaffected (default None).

Preconditions:
- `tool_name` must be in `TOOL_ALLOWLIST` (raises `ToolNotAllowedError` otherwise).
- `target` must pass `validate_query()` (raises `QueryValidationError` otherwise).
- No element in `args` may contain shell metacharacters (`;`, `|`, `&&`, `||`, backtick, `$()`, newline, carriage return).

## Outputs

```
ToolResult {
  tool_name: str
  exit_code: int
  stdout: str                    # truncated to max_output_bytes
  stderr: str                    # truncated to max_output_bytes
  duration_s: float              # wall-clock seconds
  parsed_entities: list[dict]    # normalised estorides entities
  confidence: float              # 0-1
  raw_output_sha1: str           # SHA1 of full stdout for audit trail
}
```

Parsed entities match the `Entity` shape produced by `entity_extraction.py`:
```
{
  "type": "ipv4" | "domain" | "url" | "email" | "md5" | "sha256" | "asn" | "ip",
  "value": str,
  "confidence": float,
  "source": str,                 # e.g. "nmap"
  "raw": str                     # original text fragment the entity was extracted from
}
```

Error outcome (no exception propagates to caller):
```
ToolErrorResult {
  tool_name: str
  error_code: str                # TOOL_NOT_FOUND | TOOL_TIMEOUT | TOOL_INJECTION | TOOL_CRASH | OUTPUT_TOO_LARGE
  message: str
  exit_code: int | None
  duration_s: float
}
```

## Table of errors

| Condition | Code | Behaviour |
|-----------|------|-----------|
| `tool_name` not in `TOOL_ALLOWLIST` | `TOOL_NOT_ALLOWED` | Return `ToolErrorResult` with code `TOOL_NOT_ALLOWED`, log warning, no subprocess spawned |
| Binary not found on filesystem | `TOOL_NOT_FOUND` | Return `ToolErrorResult` with code `TOOL_NOT_FOUND`, log warning |
| `args` contain shell metacharacters | `TOOL_INJECTION` | Return `ToolErrorResult` with code `TOOL_INJECTION`, log security event, no subprocess spawned |
| Subprocess exceeds `timeout` seconds | `TOOL_TIMEOUT` | Kill process group, return `ToolErrorResult` with code `TOOL_TIMEOUT`, log warning |
| Subprocess exits non-zero | `TOOL_CRASH` | Return `ToolResult` with `exit_code != 0`, attempt to parse stdout anyway |
| stdout+stderr exceed `max_output_bytes` | `OUTPUT_TOO_LARGE` | Truncate to `max_output_bytes`, set `stdout_truncated`/`stderr_truncated` flags, log warning |
| SHA1 computation failure | `OUTPUT_HASH_ERR` | Return `ToolResult` with `raw_output_sha1 = ""`, log error |
| Unicode decode error on output | `OUTPUT_DECODE_ERR` | Replace undecodable bytes with U+FFFD, continue processing |
| `args` list is empty | `NO_ARGS` | Return `ToolErrorResult` with code `NO_ARGS` (a tool called with no arguments is always wrong) |

## Security guarantees

1. **No shell execution** — `subprocess.run()` is always called with `shell=False` and an argument list. No string ever undergoes shell expansion.
2. **Tool allowlist** — only binaries in `TOOL_ALLOWLIST` (configurable via `ESTORIDES_TOOL_ALLOWLIST` env var) can be executed. The allowlist is resolved via `shutil.which()` so only system-installed binaries are permitted.
3. **Input validation** — every argument is checked against the shell metacharacter blocklist (`;`, `|`, `&&`, `||`, `` ` ``, `$()`, `\n`, `\r`). Any match raises `ToolInjectionError`.
4. **Timeout enforcement** — `subprocess.run(timeout=...)` kills the process and its group after the configured seconds. The default is 300s; max is 3600s (enforced by config).
5. **Output size cap** — stdout and stderr are truncated to `max_output_bytes` (default 10MB) to prevent memory exhaustion from verbose tool output.
6. **Audit trail** — every invocation (successful or failed) is logged at `INFO` level with tool name, sanitised args (metacharacters redacted), target, exit code, duration, and output SHA1.
7. **No eval/exec** — `tool_runner.py` contains zero calls to `eval`, `exec`, `os.system`, or `compile`.
8. **Least privilege** — the subprocess inherits estorides' process credentials. No privilege escalation is attempted.
9. **Output sanitisation** — parsed entities pass through the same `validate_query()` flow that the orchestrator uses for all query strings, preventing entity injection into downstream consumers.
10. **No network access from tools** — the module does not proxy or tunnel subprocess output. The tool speaks directly to the target; estorides only captures and parses the result.

## Out of scope

- **Privilege escalation** — `tool_runner` does not change user/group or use setuid wrappers.
- **Interactive tools** — tools that require stdin (e.g. `reaver` in interactive mode) are not supported; all tools must operate in batch/CLI mode.
- **TTY allocation** — no PTY is allocated; tools that require a terminal (e.g. `aircrack-ng` in monitor mode) must be pre-configured by the operator.
- **Tool installation** — `tool_runner` does not install Kali packages; it assumes tools are already present on the system.
- **GUI tools** — only CLI tools are supported (no gtk, qt, or web UIs spawned as subprocesses).
- **Parallelism** — `tool_runner` executes one tool at a time; concurrent execution is handled by the caller (orchestrator/fusion) using asyncio tasks or threads.

## Escenarios BDD (Given-When-Then)

### S1 [Happy path] nmap -sV against a domain returns parsed entities

Given `tool_name = "nmap"` is in `TOOL_ALLOWLIST`
And `args = ["-sV", "-T4", "-p", "22,80,443", "example.com"]`
And `target = "example.com"` passes `validate_query()`
When `run_tool("nmap", args, target="example.com", timeout=120)` is called
And nmap is present on the system at `/usr/bin/nmap`
Then a `subprocess.run()` call is made with `shell=False` and the exact arg list
And `exit_code == 0` (or non-zero — parsing still attempted)
And the returned `ToolResult` contains `parsed_entities` with at least one `ipv4` or `domain` entity
And `raw_output_sha1` is a valid SHA1 hex string
And the audit log contains one entry for this invocation

### S2 [Injection attempt] args containing `; rm -rf /` are rejected

Given `args = ["-sV", "example.com; rm -rf /"]`
When `run_tool("nmap", args, target="example.com")` is called
Then no subprocess is spawned
And a `ToolErrorResult` is returned with `error_code == "TOOL_INJECTION"`
And a security log entry is written
And `exit_code` is `None` (no process was started)

### S3 [Timeout] a tool that hangs is killed after the configured timeout

Given `tool_name = "nmap"` with a target that causes nmap to hang indefinitely
And `timeout = 5`
When `run_tool("nmap", ["-sV", "192.0.2.1"], timeout=5)` is called
And nmap does not exit within 5 seconds
Then the subprocess process group is killed
And a `ToolErrorResult` is returned with `error_code == "TOOL_TIMEOUT"`
And `duration_s >= 5.0` and `< 6.0`

### S4 [Tool not found] a binary not in PATH returns TOOL_NOT_FOUND

Given `tool_name = "nonexistent_tool_xyz"`
When `run_tool("nonexistent_tool_xyz", ["--help"], target="example.com")` is called
And `shutil.which("nonexistent_tool_xyz")` returns `None`
Then a `ToolErrorResult` is returned with `error_code == "TOOL_NOT_FOUND"`
And no subprocess is spawned
And a warning is logged

### S5 [Not allowed] a tool outside the allowlist is rejected

Given `tool_name = "malware"` (not in `TOOL_ALLOWLIST`)
When `run_tool("malware", ["--help"], target="example.com")` is called
Then a `ToolErrorResult` is returned with `error_code == "TOOL_NOT_ALLOWED"`
And no subprocess is spawned
And a warning is logged

### S6 [Edge] tool exits non-zero but stdout contains valid data

Given `args` for a tool that exits with code 1 but writes valid results to stdout
When `run_tool("some_tool", args, target="example.com")` is called
Then a `ToolResult` is returned (not an error result)
And `exit_code == 1`
And `parsed_entities` contains whatever was extractable from stdout