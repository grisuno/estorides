# system_app_sources — Kali OSINT Tools as First-Class Sources

## Purpose

Estorides treats every OSINT provider as an HTTP API. Kali, the platform
where estorides normally runs, ships a curated set of OSINT CLI tools
(theHarvester, amass, sherlock, maigret, holehe, phoneinfoga, sublist3r,
fierce, dnsrecon, dnsenum, dmitry, urlcrazy, metagoofil, whatweb, wafw00f,
OSRFramework usufy/mailfy/phonefy/searchfy). These tools speak DNS,
search-engine scraping and platform lookups directly — no HTTP gateway in
between. This module introduces a **new source kind**, `system_app`, that
executes a local binary through the existing `tool_runner` sandbox (10-layer
defence: allowlist, no shell, injection blocking, timeouts, output caps) and
feeds the result into the **same** aggregation pipeline as HTTP sources:
observations → entity extraction → fusion → reliability scoring → recon
tiers → target scoring. The YAML schema for a `system_app` source differs
from the HTTP schema (`tool.binary` + `tool.args` instead of `tool.url` +
`tool.params`), which is the point: one registry, two origin kinds, zero
special-casing downstream. Open-source Palantir: every Kali OSINT technique
becomes a pluggable, weighted, corroborating source.

## Inputs

A source YAML (see `sources/20_system_tools/`) with the system_app schema:

```yaml
name: kali_sherlock
enabled: true
category: 20. System Tools (Kali)
kind: system_app            # NEW — local binary vs remote HTTP API
os: linux                   # platform gate; "any" allowed
requires_key: false
contact: none               # none|broker|active — feeds the passive-only guarantee
logs_queries: true
parser: sherlock_text
entity_hints: [username, url]
applies_to: [username]
tool:
  binary: sherlock          # resolved via shutil.which, must be in TOOL_ALLOWLIST
  args: ["{query}", "--print-found", "--no-color", "--timeout", "30"]
  output_format: text       # json | text | lines — how to interpret stdout/file
  output_file: "{outdir}/result.json"   # optional; for tools that only write files
  timeout: 300
```

Field rules (validated at load, fail-loud on programmer input):

- `kind: system_app` required for binary sources; derived from the tool
  block if omitted (binary present → `system_app`, else `http_api`).
- `tool.binary`: non-empty string, present in `config.TOOL_ALLOWLIST`,
  resolved on the filesystem with `shutil.which`.
- `tool.args`: list of strings. `{query}` and `{outdir}` placeholders are
  substituted per invocation. Unknown `{tokens}` are left verbatim
  (same contract as `_safe_format`). Non-string args are rejected.
- `tool.output_format` ∈ {json, text, lines}; unknown → `text`.
- `tool.output_file`: optional string template rendered with the same
  placeholders; the file is read (capped) and preferred over stdout when
  present.
- `tool.timeout`: int seconds (default `config.TOOL_TIMEOUT`, 300).
- `contact` uses the same three classes as HTTP sources and is
  **conservative**: tools that talk directly to the target's own
  infrastructure (dnsrecon zone transfer, whatweb, wafw00f, metagoofil
  downloads, fierce, dnsenum) are `active` and are excluded from
  `--passive-only` runs. Tools that only touch third-party services
  (search engines, CT logs, platform profiles) are `none`.

## Outputs

```
SystemAppResult {
  source_name: str
  tool_name: str
  success: bool                 # exit_code == 0
  exit_code: int
  stdout: str                   # capped
  stderr: str                   # capped
  duration_s: float
  parsed: Any                   # parser output (list[dict] | list[str] | dict | None)
  raw_output_sha1: str
  truncated: bool
  error_code: str | None        # NO_BINARY | TOOL_NOT_ALLOWED | TOOL_NOT_FOUND |
                                # UNSUPPORTED_PLATFORM | TOOL_INJECTION |
                                # TOOL_TIMEOUT | TOOL_CRASH | NO_ARGS
  error_message: str | None
}
```

The orchestrator's binary branch converts `SystemAppResult` into the same
4-tuple `(source, parsed, raw, meta)` as HTTP sources; `parsed` is consumed
by `entity_extraction.extract_from_json` / `extract_structured` and
`meta.error` routes failures into the standard error-observation path
(case store, UI, health). No downstream change: recon_fusion,
fusion_store, reliability_scoring and target_scoring see "kali_sherlock"
exactly like "hunter_email".

## Table of errors

| Condition | Code | Behaviour |
|-----------|------|-----------|
| `tool.binary` missing from YAML | `NO_BINARY` | `SystemAppResult` with `success=False`, log warning, no subprocess |
| Binary not in `TOOL_ALLOWLIST` | `TOOL_NOT_ALLOWED` | Failure result, log security event, no subprocess |
| Binary not on filesystem (`shutil.which`) | `TOOL_NOT_FOUND` | Failure result; orchestrator records an error observation; run continues |
| `source.os` not `any` and not the running platform | `UNSUPPORTED_PLATFORM` | Failure result, no subprocess |
| Rendered arg contains shell metacharacters | `TOOL_INJECTION` | `tool_runner` rejects; failure result; security log |
| Subprocess exceeds timeout | `TOOL_TIMEOUT` | `tool_runner` kills it; failure result |
| Exit code != 0 | `TOOL_CRASH` | `SystemAppResult.success=False`, stdout still parsed (best effort) |
| stdout/file exceeds cap | truncation | `truncated=True`, parse what fits |
| `output_file` unreadable | parse fallback | Parse stdout instead; never raise |
| Parser raises on tool output | parse fallback | `parse_entities_generic` over raw text; never raise |
| Non-string element in `tool.args` | `INVALID_ARGS` (load-time) | `tool.args` reset to `[]` with warning |
| Unknown `kind` value | load-time fallback | Derive from tool block, log warning |

## Security guarantees

1. **Same 10-layer sandbox** — execution goes through
   `tool_runner.run_tool`: `shell=False` with an argument list, allowlist,
   metacharacter blocking, `shutil.which` resolution, timeout kill, output
   caps, audit logging. No new subprocess path is opened.
2. **No eval/exec** — the module contains zero `eval`, `exec`,
   `os.system` or `compile`.
3. **Operator-authored args only** — `tool.args` come from YAML in
   `sources/`, never from remote content; the remote-derived part is only
   the `{query}` token, which `validation.validate_query` constrains.
4. **Private scratch outdir** — `{outdir}` renders into a fresh
   `tempfile.TemporaryDirectory(prefix="estorides_tool_")` that is
   removed after parsing. Tools can never write into the repo or `/tmp`
   with a predictable path.
5. **Passive-only guarantee intact** — `contact` classification is
   conservative (any doubt → `active`); `--passive-only` excludes system
   apps the same way it excludes HTTP brokers, even with `--only-sources`.
6. **Output file capped** — `output_file` reads are capped at
   `TOOL_MAX_OUTPUT_BYTES`; giant tool outputs cannot exhaust memory.
7. **Fail-soft on tool failure** — every failure is an error observation,
   never an exception; one missing binary cannot poison a run.

## Out of scope

- Tools that require API keys, workspaces or interactive setup
  (spiderfoot, recon-ng, h8mail) — batch 2 with `key_env` support.
- `exiftool` on uploaded files (query flow is a file path, not a selector).
- Active-recon tools (nmap, nikto, sqlmap) — already covered by
  `active_recon.py`; system_app batch 1 stays OSINT.
- GUI tools (maltego), interactive/TTY tools, tor/proxy chaining per tool.
- Tool installation: missing tools surface as `TOOL_NOT_FOUND`, estorides
  does not apt-install anything.

## Escenarios BDD (Given-When-Then)

### S1 [Happy path] sherlock source executes, parses and produces entities

Given a `kali_sherlock` YAML with `tool.binary: sherlock`, args
`["{query}", "--print-found"]`, parser `sherlock_text`
And `sherlock` exists in `TOOL_ALLOWLIST` and on the filesystem
When `execute(source, "testuser")` runs with a stub runner returning
stdout `"[+] testuser: https://github.com/testuser\n[-] notfound: x"`
Then the result has `success=True`, `exit_code=0`
And `parsed` contains a line with the found profile URL
And the stub runner received args `["testuser", "--print-found"]`

### S2 [Missing binary] tool absent on system degrades to an error observation

Given `kali_sherlock` declares `tool.binary: sherlock`
And `shutil.which("sherlock")` returns None
When the orchestrator executes the source
Then `SystemAppResult.error_code == "TOOL_NOT_FOUND"`, `success=False`
And the orchestrator returns `raw=None` with `meta["error"]` set
And the run continues (no exception reaches the caller)

### S3 [Crash] non-zero exit still parses stdout best-effort

Given the runner returns `ToolResult(exit_code=1, stdout="partial data", error_code="TOOL_CRASH")`
When `execute` runs
Then `success=False`, `error_code="TOOL_CRASH"` and `parsed` is not None

### S4 [Security] metacharacters in a rendered arg are rejected, no subprocess

Given a YAML arg template `["{query}", "x; rm -rf /"]` (query clean)
When `execute` renders and calls the runner
Then the runner rejects with `TOOL_INJECTION`
And `SystemAppResult.error_code == "TOOL_INJECTION"`
And the stub process was never spawned

### S5 [JSON file output] amass writes `{outdir}/amass.json`, parsed from file

Given `kali_amass` with `output_file: "{outdir}/amass.json"` and parser `amass_json`
And the runner (after execution) has materialised `{outdir}/amass.json`
  with one JSON object per line (`{"name": "sub.example.com", "addresses": [{"ip": "192.0.2.1"}]}`)
When `execute` runs
Then `parsed` is a list of dicts with `domain == "sub.example.com"`
And the temporary outdir no longer exists after the call returns

### S6 [Placeholders] `{query}` and `{outdir}` are substituted; unknown tokens survive

Given args `["{query}", "--out", "{outdir}/r.json", "{env}"]`
When `render_args(args, "example.com", "/tmp/x")` runs
Then the result is `["example.com", "--out", "/tmp/x/r.json", "{env}"]`

### S7 [Passive-only] contact ceiling excludes touching tools even by name

Given `kali_dnsrecon` declares `contact: active` and `kali_sherlock` `contact: none`
When the orchestrator selects sources with `max_contact="none"` and
  `--only-sources=kali_dnsrecon,kali_sherlock`
Then only `kali_sherlock` survives the contact ceiling
And `kali_dnsrecon` is dropped with a log line

### S8 [Registry] kind is exposed, loader validates the system_app schema

Given a YAML with `kind: system_app`, binary present, `output_format: json`
When the registry loads `sources/`
Then `source["kind"] == "system_app"`, `tool["output_format"] == "json"`
And `registry.summary()` exposes `kind` per source
And a YAML with `output_format: nonsense` normalises to `text`
And a YAML with non-string args gets `tool.args == []` with a warning

### S9 [Concurrency] a slow system app never blocks the event loop

Given the orchestrator executes a system_app source whose runner sleeps 0.6s
When the binary branch of `_execute_source` runs inside an asyncio loop
Then the execution is offloaded to a worker thread (`asyncio.to_thread`)
And an unrelated asyncio task scheduled 0.2s later still fires while the
  tool is running (loop not frozen)
And the source result is returned once the tool finishes

## Escenarios de property-based testing (doctrina §6)

- P1 parsers never raise: 1000 random byte/text blobs into every
  registered tool parser → always a list, never an exception.
- P2 templating never emits metachars: 1000 random query/outdir strings →
  rendered args contain no `; | \` $ ( ) \n \r` beyond what tool_runner
  already rejects as a whole.
- P3 output-file reads are capped: 1000 random sizes → parsed text ≤ cap.
- P4 unknown-parser fallback: random parser names + random text →
  `parse_tool_output` never raises, returns a list.
