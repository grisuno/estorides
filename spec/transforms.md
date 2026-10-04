# transforms — Spec (Maltego-style pivoting)

## Purpose
The current fan-out is "collection" (99 sources fired blindly). This module is
"analysis": given one graph node `(type, value)`, it runs only the exact source
needed and returns `nodes/links` to merge without clearing the existing graph.
It enables chained pivoting (domain → IP → ASN → siblings), saves API quota,
and tells an exportable story. Interactive layer over `intel_resolver` plus
the keyless `osiris_sources` probes.

## Inputs
- `ent_type: str` — entity type, lowercased/trimmed. Accepted: `ip, ipv4,
  ipv6, domain, email, username, file, hash, md5, sha1, sha256, company,
  person, country, cve, btc_address, eth_address` plus any future `t` (exact
  match or `any`). Empty → error `missing type`. Max length 64.
- `value: str` — selector (IP, domain, email...). Trimmed, non-empty, max
  length 512. Never executed nor evaluated; only passed to `resolver.resolve`
  / `osiris.*`, which already enforce SSRF guards.
- `transform_id: str` — registered id (`[a-z0-9_]+`, max 64). Unknown →
  error `unknown transform`.
- `for_type(ent_type)`: `ent_type` may be `""` → empty list (no 500).

## Outputs
`registry.for_type(type) -> [{id, label, tier, description, input_types,
output_types, cost}]` sorted by `(TIERS.index(tier), label)`.
`registry.run(tid, type, value) ->` JSON-schema:
```json
{"nodes": [{"id": "ip:1.2.3.4", "label": "1.2.3.4", "type": "ip",
"kind": "ip", "properties": {"source": "query"}}],
"links": [{"source": "ip:1.2.3.4", "target": "asn:15169",
"relation": "announced_by"}],
"sources": ["bgp"], "transform": "ip_to_bgp", "tier": "information"}
```
On error: `{"error": "<code>", "nodes": [], "links": [], "sources": []}`
plus `transform/tier` when the id exists. Never raises.
**YAML transforms** (same ease as `sources/`): dropping a `*.yaml` file into
`transforms/` registers a pivot without touching Python. Schema:
`{id, label, tier, description, input_types|applies|applies_to, output_types,
cost, engine, relations|nodes|links}`. `engine` is one of `resolver` (filters
`resolver.resolve` by `relations`, `null` = full), `osiris_bgp|osiris_leaks|
osiris_github`, `static` (fixed nodes/links with `{query}`). Loaded with
`yaml.safe_load` (multi-doc / list docs like `source_loader`), id must match
`^[a-z0-9_]{1,64}$`, unknown tier → `information`, duplicate → overwrite with
warning, broken YAML → skip with log (fail-soft, built-ins survive).
`registry.load_yaml_dir(path) -> int` reloads (tests + future reload).
Web: `GET /api/transforms?type=` → `{"type","transforms"}`.
`POST /api/transform/run {transform_id,type,value}` → same dict.
`GET /api/transform/stream?transform_id=&type=&value=` → SSE
`event: node|link|done|error` with progressive `data: {...}` plus `done`
`{nodes:N, links:N}`. The frontend keeps `_expansionSeen` (dedupe) and
`_graphBatches[]` (snapshot stack `{nodes,links}`, cap 50, `Ctrl+Z` undo).

## Error table
| Condition | Code | Behaviour |
|---|---|---|
| empty type (API) | `missing type` 400 | registry untouched |
| empty tid/type/value (run) | `transform_id, type and value required` 400 | no run |
| unknown tid | `unknown transform '<id>'` 200+error | empty nodes/links |
| runner raises | `transform-run-failed` 200+error | log.exception, fail-closed |
| osiris import fails / empty data | `_empty` | root-only or empty nodes, sources [] |
| value >512 / type >64 / malformed tid | `transform-failed`/`invalid` 400 | rejected before any I/O |
| stream with missing params | SSE `error` + close | connection never hangs |
| graph polluted with 500 junk nodes | UX undo | `Ctrl+Z` restores previous snapshot |

## Security guarantees
- All input is hostile: `type/value/tid` trimmed and capped, never
  `eval/exec/os.system/shell=True`. Argument lists / function calls only.
- Network only via `intel_resolver` + `osiris_sources`, which already go
  through `ssrf_guard.assert_safe/check_url` (blocks loopback/metadata/scheme).
- No CWE-209 leak: runners never return `str(e)` to the client; codes only.
- YAML via `yaml.safe_load` only (no Python tags), statics capped (50 nodes /
  100 links, strings ≤512), `{query}` is plain text substitution, never an
  executable template; rendering escapes like everything else.
- Frontend: remote strings (`label/type/value/sources`) via
  `escapeHTML/textContent/DOMPurify.sanitize`; colors via `safeColor`;
  zero `innerHTML=renderMarkdown`, zero inline `style=""`.
- Auth + rate-limit on all 3 routes (`api_transforms/api_transform_run/
  stream`) like the rest of the API.

## Out of scope
- Live WHOIS/RDAP, keyed HIBP, keyed VirusTotal, historical BGP siblings
  (needs bulk CT/pDNS). Only what `resolver` + keyless `osiris` already give.
- Graph persistence / server-side history (client-side memory stack only).
- Narrative GraphML/PDF export (covered by `recon_report`/existing export).
- Automatic tier mutation (the localStorage override stays manual).

## BDD scenarios Given-When-Then
- S1 happy: Given `ip_to_bgp` registered for `ip`, when `run(ip_to_bgp,ip,
  8.8.8.8)` with mocked bgp `{asn:15169, holder:Google}`, then 3 nodes
  (root+asn+company) and 2 links `announced_by/hosted_by`, `sources==[bgp]`.
- S2 empty edge: Given osiris returns `{}` or the import fails, when run,
  then `nodes==[root]` or `[]`, `links==[]`, no raise, `sources==[]`.
- S3 error id: Given a nonexistent tid, when `run(nope,ip,1.2.3.4)`, then
  `error` contains `unknown transform`, empty nodes/links.
- S4 security broken-runner: Given a raising runner, when run, then
  `error==transform-run-failed`, logged, exception never propagates.
- S5 rich metadata: Given `for_type(ip)`, when listed, then every item carries
  `id/label/tier/description/input_types/output_types/cost`, sorted by tier.
- S6 SSE stream: Given a valid transform, when `GET /stream?...`, then
  `node*` + `link*` + `done{nodes,links}` arrive and the client merges without
  duplicating (idempotent re-click) and can undo from a snapshot.
- S7 codeless yaml: Given `transforms/my_pivot.yaml` with `engine: resolver`
  + `relations: [resolves_to]`, when the registry loads, then the pivot shows
  in `for_type(domain)` with its `label/tier/output_types/cost` and `run()`
  filters to those links only; one broken YAML never kills the built-ins.
- S8 yaml catalog: Given the 14 files in `transforms/`, when the suite runs,
  then every file carries full metadata, every id is registered, and every
  `static` pivot runs offline with zero `{query}` leftovers at any depth
  (including nested `properties`).

## Transform catalog (YAML pivots, codeless)

One file per pivot in `transforms/`. To add number 15, copy any file, change
`id`/`label`/`relations`, save. No Python, no restart logic beyond reload.

| id | label | tier | inputs | outputs | engine | description |
|---|---|---|---|---|---|---|
| abuse_contact_hint | Domain to Abuse-contact hint | information | domain | email | static | Static hint node showing where to ask for the abuse contact. |
| asn_siblings | ASN Announced + hosted (pivot) | information | ip,ipv4,ipv6 | asn,company | resolver relations=announced_by,hosted_by | Hosting org and ASN for an IP without re-scanning 99 sources. |
| asn_to_bgp | ASN to BGP holder (Osiris) | information | asn | asn,company | osiris_bgp | Route holder and announced prefixes for an ASN via RIPEstat. |
| btc_to_explorer | BTC address to Explorer | information | btc_address | url | static | Hint node pointing at the mempool explorer for this address. |
| cve_to_nvd | CVE to NVD detail | information | cve | url | static | Hint node pointing at the NVD page for this CVE. |
| cve_to_products | CVE to Affected products | intelligence | cve | product | resolver relations=produces | Products produced by affected vendors (NVD). |
| domain_to_crtsh | Domain to Certificate history | intelligence | domain | url | static | Hint node pointing at crt.sh certificate search for this domain. |
| domain_to_wayback | Domain to Wayback captures | information | domain | url | static | Hint node pointing at archived copies of this domain. |
| hash_to_virustotal | Hash to VirusTotal report | intelligence | file,hash,md5,sha1,sha256 | url | static | Hint node pointing at the VirusTotal file report for this hash. |
| ip_to_abuseipdb | IP to Reputation page | information | ip,ipv4,ipv6 | url | static | Hint node pointing at the AbuseIPDB check page for this IP. |
| ip_to_geo | IP to Geolocation | intelligence | ip,ipv4,ipv6 | country | resolver relations=located_in | Country where this IP is located, without re-scanning 99 sources. |
| ip_to_host | IP to Hosting org | information | ip,ipv4,ipv6 | company | resolver relations=hosted_by | Organisation hosting this IP, without re-scanning 99 sources. |
| person_full | Person to Full cross-resolve | intelligence | person | company,country,sanction | resolver (full) | Everything the resolver knows about this person. |
| username_to_github_page | Username to GitHub page | data | username | url | static | Hint node pointing at the public GitHub profile page. |

## Closed 2026-10-04, extended with 12 more pivots
- 8 green BDD (`tests/test_transforms.py` S1-S8). `ruff` clean on
  `transforms.py` + tests + `estorides_web.py`; `mypy --strict` 0 errors on
  `transforms.py` (4 pre-existing closed along the way: unannotated `_osiris`);
  `bandit` 0 High/Medium; `node --check` OK.
- `transforms/` ships 14 codeless pivots (4 resolver, 1 osiris, 9 static);
  registry is 26 built-ins + 14 YAML = 40. `GET /api/transform/stream` SSE.
  Frontend: `_graphBatches` + `undoGraph()` + `Ctrl+Z`, `runTransformStream`
  (shift+click), merge with no extra refetch.
- Bug fixed along the way: `{query}` was not substituted inside nested
  `properties` dicts of static pivots (S8 pins recursive substitution).
- Environment-pending (no `hypothesis`/`mutmut` here, same as milestone M6):
  `tests/properties/test_transforms_properties.py` (1000 ex.) and `mutmut run`
  with 0 survivors before calling it hardened.
