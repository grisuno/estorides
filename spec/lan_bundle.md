# lan_bundle — LAN output deliverables for automation

## Purpose

Write every LAN discovery result to an output directory as machine
readable deliverables. Other tools (LazyOwn intel and attack graphs,
auto_loop orchestration, offline analysis) consume these files without
talking to the web UI. The same device list feeds the 2D graph, the 3D
graph, and the sphere view through the shared graph payload.

## Inputs

- `devices: list[LanDevice]` from `lan_inventory.merge_devices`.
- `graph_payload: dict | None` — optional `KnowledgeGraph.export_json()`
  snapshot to embed alongside devices. When None, only devices ship.
- `output_dir: str | Path` — destination directory. Created when
  missing. Defaults to `ESTORIDES_LAN_OUTPUT_DIR` or `data/lan_output`.
- `stem: str` — file stem, sanitized to `[A-Za-z0-9_-]+`. Default
  `lan`. Bad stems fall back to `lan`, never raise.

## Outputs

Files written atomically (temp file plus rename):

- `<stem>_inventory.json` — devices with ids, ips, mac, hostnames,
  sources, plus `generated_at`, `schema_version`, `scope_cidr`.
- `<stem>_graph.json` — force/sphere-ready payload: `nodes` with
  `id/kind/label/type/sources`, `edges` with
  `source/target/type/evidence`. Device nodes plus co-location edges
  through the scope network node.
- `<stem>_lazyown.json` — LazyOwn vocabulary: `nodes` with
  `kind/etype/value/label/sources/attrs`, `edges` with
  `source_kind/source_value/target_kind/target_value/type/evidence`.
  Device IPs map to `host`, MACs to `mac`, hostnames to `domain`.
- `<stem>_stix.json` — STIX 2.1 bundle reusing the existing STIX
  shapes for ipv4, mac-addr, and domain-name plus relationships.

`write_bundle()` returns `LanBundleResult` with `paths: dict`,
`errors: list`, `device_count`, `node_count`. I/O failures are values
in `errors`, never exceptions.

## Error table

| Failure | Behavior |
|---|---|
| bad stem | sanitize to `lan` |
| empty devices | files still written with empty lists |
| output dir not creatable | `errors` entry, no raise, no partial files |
| unserializable extra | dropped field, noted in errors |
| existing files | atomically replaced |

## Security guarantees

- Stem sanitized: path traversal impossible (`..`, `/` stripped to
  `lan`).
- Output dir confined: resolved path must stay inside the configured
  root or the call records an error and writes nothing.
- Atomic writes: readers never see half-written JSON.
- No network, no subprocess, no shell. JSON only.

## Out of scope

- Authorization (`lan_policy`), scope detection (`lan_scope`),
  discovery parsing (`lan_inventory`).
- Live graph mutation, web rendering, LazyOwn-side import logic.

## Scenarios BDD Given-When-Then

- S1 happy bundle: Given two devices, When built, Then graph has
  device nodes plus one network node and lazyown maps IPs to host.
- S2 empty: Given no devices, When built, Then payloads carry empty
  lists with schema version.
- S3 stem traversal: Given stem `../../etc`, When built, Then files
  use `lan` stem inside output dir.
- S4 entities: Given a MAC plus IP device, When converted, Then STIX
  holds ipv4-addr and mac-addr objects.
- S5 write atomic: Given tmp output dir, When written, Then all four
  files exist and parse as JSON.
- S6 error dir: Given output path is an existing file, When written,
  Then errors non-empty and no exception.
- S7 scope tagged: Given scope `192.168.1.0/24`, When built, Then
  inventory carries scope and graph has network node.
- S8 deterministic: Given same devices twice, When built twice, Then
  node ids and edge sets match exactly.
