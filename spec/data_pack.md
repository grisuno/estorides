# data_pack — Spec

## Purpose
Static reference datasets are consumed from their upstream at runtime, not
vendored into the repository. A pack is fetch + optional SHA-256 pin +
TTL cache + stale fallback, so Estorides never becomes a fork of somebody
else's data and never silently trusts whatever is at a URL today.

## Inputs
- `load_pack(name, url, parse, cache_path=None, ttl_s=30d, max_bytes=64MiB,
  expected_sha256=None, timeout=60, use_cache=True)`.
- `parse(raw_bytes) -> Any`: caller-owned parser (CSV, JSON, whatever) and
  the thing that is cached.
- `expected_sha256`: hex digest; an unusable value (wrong length, non-hex,
  non-string) is ignored, never an implicit pin.
- `fetch_bytes(url, max_bytes, timeout)`: `assert_safe`-checked,
  `Estorides/1.0` User-Agent, streamed and aborted past the cap.

## Outputs
- Parsed payload, or `None` when nothing is cached and the fetch failed.
- Cache file `{fetched_at, sha256, payload}` under `data/packs/<name>.json`,
  written atomically (tmp + `os.replace`).

## Error table
| Condition | Behaviour |
|---|---|
| Fresh cache (age < ttl, digest matches the pin) | Returned, no network |
| Stale cache + failed fetch | Stale payload returned, warning logged |
| Stale cache + parser raised | Stale payload returned |
| No cache + failed fetch | `None` — callers report "unavailable", never "empty" |
| SHA-256 mismatch | `DataPackIntegrityError`, stale payload kept, cache untouched |
| Payload over `max_bytes` | `DataPackError`, stream aborted |
| Corrupt / foreign cache file | Treated as missing |

## Security guarantees
- `assert_safe` runs before every request (no user-controlled URL unless an
  operator opts in through an env override, which is still checked).
- Size cap bounds memory and a hostile mirror.
- Pinning turns a remote file into a verifiable artifact; an upstream
  rewrite fails closed instead of changing behaviour unnoticed.
- No credentials: packs are keyless reference data.

## Out of scope
- Mirroring or vendoring datasets into the tree.
- Signature verification (GPG/minisign); SHA-256 is the current gate.
- Delta updates / conditional requests (`ETag`, `If-Modified-Since`).

## BDD scenarios
- Given a fresh cache, when `load_pack` runs, then the network is never
  touched.
- Given a stale cache and a failing fetch, then the stale payload is
  returned.
- Given a pinned digest and different bytes, then the load fails closed and
  the last known-good payload survives.
- Given a parser that raises, then the failure degrades to the cache.
- Given a stream larger than the cap, then `fetch_bytes` aborts.
