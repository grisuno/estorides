# lan_runner — real LAN scan execution

## Purpose

Execute an actual local network scan and return devices. Reads the
ARP/neighbor table and DHCP leases already present on the host
(passive, no wire traffic), optionally runs one active tool through
the `tool_runner` sandbox when the policy permits it, merges sightings
with `lan_inventory`, writes deliverables with `lan_bundle`, and
returns graph-ready entities for the route to feed the knowledge
graph. Readers are injectable so tests never touch the system.

## Inputs

- `scan()` parameters:
  - `scope_cidr: str | None` — explicit scope. When None, resolved
    from `interfaces` via `lan_scope.default_scope`.
  - `interfaces: list` — interface addresses for scope resolution.
  - `consent: bool` — strict True required, enforced via
    `lan_policy`. False refuses the scan, never raises.
  - `allow_active: bool` — checkbox intent. Active runs only on the
    triple gate; otherwise the scan degrades to passive with
    `notice` set.
  - `arp_text / dhcp_text / active_text: str | None` — injected
    reader output for tests. When None, the real readers run.
  - `output_dir` — bundle destination. Default
    `lan_bundle.default_output_dir()`.

## Outputs

- `LanScanResult` frozen dataclass (`to_dict()`):
  - `refused: bool`, `block_reason`, `message`
  - `scope_cidr`, `devices: list[dict]`, `device_count`
  - `entities: list[dict]` (graph-ready, via
    `lan_inventory.device_to_entities`)
  - `bundle: dict` (paths from `write_bundle`), `bundle_errors`
  - `active_used: bool`, `notice: str | None`

## Error table

| Failure | Behavior |
|---|---|
| consent not True | refused, `consent_required`, no readers run |
| scope invalid or public | refused, `scope_invalid` |
| no private scope found | refused, `scope_invalid`, message says so |
| reader binary/files missing | empty text, scan continues |
| active gate fails | passive runs, `notice` set, `active_used` False |
| active tool fails | passive results kept, noted in `notice` detail |
| bundle unwritable | devices still returned, `bundle_errors` set |

## Security guarantees

- Consent enforced before any reader or tool runs.
- Active path uses `tool_runner.run_tool` only (allowlist, no shell,
  timeout cap 120 s). Scope is validated private before reaching the
  tool; the tool never receives raw operator text.
- Readers: `ip` via resolved full path, lease files from a fixed
  allowlist of paths, size-capped reads. No sockets, no broadcast.
- Never raises on hostile input; refusals and errors are values.

## Out of scope

- Authorization math (`lan_policy`), HTTP wiring, JS rendering.
- Graph mutation (the route feeds `entities` to the graph).
- Vendor OUI lookup, port scanning, credential checks.

## Fix 2026-10-11 (scan always runs + real results)

- Checkbox-on without server ceiling degraded the whole run to a 403
  with a message blaming the checkbox. Now the scan always runs:
  active-unavailable degrades to passive with a warning notice.
- Scan LAN ran an OSINT query for the CIDR string and returned
  nothing. Now `POST /api/lan/scan` executes `lan_runner.scan`
  (ARP plus DHCP passive, one gated arp-scan when permitted), writes
  the bundle, feeds the knowledge graph, and the UI renders device
  cards plus refreshes the graph views.
- Dead neighbor entries (FAILED, INCOMPLETE) are dropped by
  `parse_arp_table` so counts reflect live hosts.

## Scenarios BDD Given-When-Then

- S1 happy passive injected: Given ARP plus DHCP text and consent,
  When scanned, Then devices merged, entities non-empty, bundle
  written, `active_used` False.
- S2 no consent: Given consent False, When scanned, Then refused and
  no readers run (injected texts ignored).
- S3 bad scope: Given public scope, When scanned, Then refused
  `scope_invalid`.
- S4 degrade active: Given allow_active True but env ceiling False,
  When scanned, Then passive devices returned with `notice` set.
- S5 active injected: Given active text plus ceiling True (env),
  When scanned, Then `active_used` True and active sightings merge.
- S9 tool order: Given a fake runner, When nmap succeeds, Then the
  tool is `nmap`; when nmap fails but arp-scan succeeds, Then the
  tool is `arp-scan`; when both fail, Then empty output and no
  exception. Active command is `nmap -sn -oG - <scope>` first,
  `arp-scan <scope>` fallback, each through the `tool_runner`
  sandbox with bounded timeouts.
- S6 empty readers: Given empty texts, When scanned, Then zero
  devices, bundle still written, not refused.
- S7 scope auto: Given interfaces with one private net and no scope,
  When scanned, Then scope resolves to it.
- S8 no scope found: Given empty interfaces and no scope, When
  scanned, Then refused `scope_invalid`.
