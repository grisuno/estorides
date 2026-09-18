# source_routing — Spec

## Purpose
`_select_sources` must route every `detect_query_type` output to the
sources that can answer it, including alias families and the two new
M1 types (`phone`, `mac`). Previously `phone`/`mac` matched nothing,
`kali_phoneinfoga`/`kali_phonefy` were tagged `username`, and generic
aliases (`ip`, `hash`, `btc`) never matched their concrete YAML tags.

## Inputs
- `query_type: str` from `detect_query_type`.
- Source `applies_to: list[str]` per YAML.

## Outputs
- Selected sources: a source matches when its `applies_to` intersects
  the expansion set of the query type. `any` still matches everything.
  Sources without `applies_to` keep legacy match-all behaviour.

## Expansion sets (directional)
| query_type | also matches |
|---|---|
| `url` | `url`, `domain` |
| `domain` | `domain` |
| `ip` | `ipv4`, `ipv6` |
| `ipv4`/`ipv6` | itself only |
| `btc` | `btc_address` |
| `eth` | `eth_address` |
| `hash` | `md5`, `sha1`, `sha256` |
| `phone`/`phone_e164` | `phone`, `phone_e164` |
| `handle` | `username` |
| `mac` | `mac` |
| default | itself |

## Error table
| Condition | Behaviour |
|---|---|
| Unknown query_type | Matches itself only; `any` sources still included. |
| `names` explicit + passive ceiling | Alias expansion applies first, contact filter second; passive-only never widened by name. |

## Security guarantees
- No change to contact-ceiling enforcement or key gating.

## Out of scope
- New sources (M3), detector changes (M1).

## BDD scenarios
- Given query_type `phone`, when selecting, then `kali_phoneinfoga` and `kali_phonefy` are included.
- Given query_type `url` for `https://example.com/x`, when selecting, then domain sources are included.
- Given query_type `hash`, when selecting, then md5/sha1/sha256 sources are included.
- Given query_type `mac`, when selecting, then `macvendors_lookup` is included.
