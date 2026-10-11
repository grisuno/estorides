---
name: estorides-source-author
description: Create, feed, modify, improve, and maintain Estorides source and tool YAMLs (HTTP APIs, system_app Kali tools, LAN discovery tools). Use when adding a new OSINT origin, wiring a Kali binary, changing contact class, parser, applies_to, or category.
---

# Estorides source author

One registry, three origin kinds. Every YAML in `sources/` becomes a
`Source` through `estorides_core/source_loader.py`. The loader is
lenient by design (unknown contact becomes `active`, bad args reset to
`[]`), so the author must be strict.

## 1. Pick the kind

- HTTP API (`kind` omitted, `tool.url` + `tool.params`): third-party
  database, resolver, CT log. `contact` is almost always `none`.
- System tool (`kind: system_app`, `tool.binary` + `tool.args` with
  `{query}`/`{outdir}` placeholders): local Kali binary run through
  `tool_runner` sandbox. `contact` follows `lan_inventory`:
  local readers are `none`, anything touching the target is `active`.
- LAN discovery (lives in `sources/20_system_tools/`, `applies_to`
  includes `ipv4`, `cidr`, or `mac`): passive readers first
  (`ip-neigh`, `dhcp-leases` style local state). Active tools
  (`nmap`, `arp-scan`, `nbtscan`, `netdiscover`, `snmpwalk`,
  `enum4linux`, `smbclient`) require `contact: active` plus the LAN
  consent triple gate (`lan_policy` + checkbox + env ceiling).

## 2. Scaffold from a template

Copy the closest template in this skill directory, never start blank:

- `templates/http_source.yaml` for HTTP APIs.
- `templates/system_tool.yaml` for Kali binaries.
- `templates/lan_tool.yaml` for LAN discovery tools.

Name the file `<tool>_<function>.yaml` in the category directory
(`sources/20_system_tools/` for tools, numbered category dirs for
APIs). The filename stem should match `name`.

## 3. Required fields

`name`, `description`, `category`, `contact`, `parser`,
`entity_hints`, `applies_to`, `tool`. Optional: `os`,
`requires_key` plus `key_env`, `logs_queries`, `output_file`,
`timeout`, `pagination`.

Rules:

- `contact`: `none` (target never sees anything), `broker` (third
  party probes on your behalf), `active` (you touch the target).
  Unknown strings become `active`. When in doubt, pick `active`.
- `parser`: must exist in `estorides_core/parsers.py` registry or be
  added there with the same SDD cycle (spec plus tests plus code).
  `raw_text` is the fallback, never a goal.
- `entity_hints` and `applies_to`: use the ontology vocabulary
  (`domain`, `ipv4`, `ipv6`, `cidr`, `mac`, `email`, `asn`, `cve`).
- `tool.args`: argument list only, no shell. `{query}` and `{outdir}`
  are the only placeholders. New binaries must join `TOOL_ALLOWLIST`
  in `estorides_core/config.py`.
- Secrets: never hardcode keys. Use `requires_key: true` plus
  `key_env: ESTORIDES_<NAME>_KEY`.

## 4. Validate

```bash
python3 -c "from estorides_core.source_loader import SourceLoader; l=SourceLoader(); print(len(l.all()))"
python3 -m pytest tests/test_source_loader.py -q
python3 -m ruff check sources/<dir>/<file>.yaml
```

Checklist before done: loader parses the file with no warnings,
`contact` is deliberate, parser exists and is covered by tests,
`TOOL_ALLOWLIST` includes the binary, category directory matches the
`category` label, no secrets in YAML.

## 5. Maintain

- Improve a weak parser before adding a duplicate source.
- Retire dead endpoints: set `enabled: false`, never delete history.
- Active tools stay `contact: active` even when they feel passive.
  Downgrading contact is a security change and needs explicit review.
- Record decisions with `readmenator . remember "<note>" --kind decision`.
