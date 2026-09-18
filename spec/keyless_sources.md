# keyless_sources — Spec

## Purpose
Three high-value keyless feeds exist in the codebase only as one-off
`osiris_sources` endpoints, unreachable from the orchestrator fanout:
BGPView IP, BGPView ASN, and the CISA KEV catalog. This spec promotes
them to first-class YAML sources with total parsers so every run
correlates routing and exploited-vuln context without an API key.

## Inputs
- BGPView IP: `https://api.bgpview.io/ip/{query}` for `ipv4`.
- BGPView ASN: `https://api.bgpview.io/asn/{query}` for `asn`
  (`AS123` or `123`; digits normalised by stripping a leading `AS`).
- CISA KEV: `https://www.cisa.gov/sites/default/files/feeds/
  known_exploited_vulnerabilities.json` for `cve` and `keyword`.

## Outputs
- `parse_bgpview(payload)`: `{"prefixes": [...], "asns": [...],
  "rir": str, "allocation": str}`; empty containers on any bad input.
- `parse_cisa_kev(payload)`: `{"vulnerabilities": [...<=20], "total": int}`;
  each item keeps `cveID`, `vendorProject`, `product`,
  `vulnerabilityName`, `dateAdded`, `dueDate`.
- New YAMLs load via `SourceRegistry` with `requires_key: false` and
  correct `applies_to`.

## Error table
| Condition | Behaviour |
|---|---|
| Payload `None`/str/list | Parser returns empty containers, never raises. |
| Upstream `status != ok` | `parse_bgpview` returns empties. |
| KEV feed with 0 vulns | `{"vulnerabilities": [], "total": 0}`. |
| Hostile nested types | Coerced via `_d`/`_list`; never raises. |

## Security guarantees
- Parsers are pure and total; URLs pass through the existing
  `ssrf_guard` in the HTTP layer, not the parser.
- Capped at 20 items per observation (bounded memory).

## Out of scope
- Authenticated feeds (Shodan, Censys, Hunter), VT enrichment.

## BDD scenarios
- Given a BGPView IP payload with prefixes, when parsed, then prefixes and ASNs are extracted.
- Given `None`/`"x"`/`[]`, when parsed by either parser, then empty containers return without raising.
- Given the registry loads, when queried, then `bgpview_ip`, `bgpview_asn`, `cisa_kev_recent` exist, are keyless, and route for `ipv4`/`asn`/`cve`.
