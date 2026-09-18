# query_intent — Spec

## Purpose
Free-form operator input must map to exactly one routable query type so
the orchestrator fans out to sources that can answer it. The previous
detector misrouted phone numbers, MAC addresses, `@handles`, uppercase
bech32, and bare URLs, and had no normaliser, so infrastructure queries
leaked into username sources and vice versa.

## Inputs
- `query: str`, raw operator input, any case, leading/trailing spaces.

## Outputs
- `detect_query_type(query) -> str`, one of `ipv4|ipv6|url|email|
  btc_address|eth_address|md5|sha1|sha256|cve|asn|phone|mac|
  domain|username|keyword|empty|user_agent`.
- `normalize_query(query) -> str`, routing form: trimmed; URLs reduced
  to `host[:port-stripped]` lowercased; `@handle` reduced to bare handle;
  everything else trimmed verbatim.

## Error table
| Condition | Behaviour |
|---|---|
| Empty/blank | `empty`; normaliser returns `""`. |
| URL with no host | `url`; normaliser returns trimmed input. |
| Phone-looking with 16+ digits | Not phone; falls through to existing rules. |
| MAC with non-hex groups | Not mac; falls through. |

## Security guarantees
- Pure string classification, no I/O, no eval, bounded regexes only.
- Normaliser never emits credentials: userinfo and port are stripped.

## Out of scope
- Source selection itself (M2), person-name NLP, IDN/punycode handling.

## BDD scenarios
- Given `+1 (415) 555-0132`, when detected, then type is `phone`.
- Given `AA:BB:CC:DD:EE:FF`, when detected, then type is `mac`.
- Given `@octocat`, when detected and normalised, then type is `username` and normalised is `octocat`.
- Given `https://Example.COM:443/a?b=c`, when detected and normalised, then type is `url` and normalised is `example.com`.
- Given `BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4`, when detected, then type is `btc_address`.
- Given `putin`, when detected, then type stays `username` (backward compat with 25 username sources).
