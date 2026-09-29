# retry_policy — Spec

## Purpose
I centralize retry bounds so no caller hardcodes attempts or sleeps. Stdlib only, no tenacity. Fail soft and capped so a hostile slow source cannot hold a worker forever.

## Inputs
- `RetryConfig(attempts, base_s, factor, cap_s)` frozen, built from `ESTORIDES_MAX_RETRIES`, `ESTORIDES_BACKOFF_BASE`, `ESTORIDES_BACKOFF_FACTOR`, `ESTORIDES_BACKOFF_CAP_S` (default 30.0).
- `retry_delay(attempt)` returns seconds for 1-indexed attempt, capped.
- `AsyncClient(max_retries=None)` uses `RETRY.attempts` when None; explicit int still honored.

## Outputs
- `RETRY` singleton + `retry_delay()` helper. `AsyncClient` sleeps `retry_delay(attempt)` on 429/5xx/timeout instead of inline math.

## Error table
| Condition | Behaviour |
|---|---|
| attempt < 1 | treated as 1, never negative sleep |
| malformed env | fallback defaults, never raise at import |
| cap exceeded | clamped to cap_s |

## Security guarantees
- Cap prevents worker hold. No new network surface. Jitter omitted deliberately for deterministic tests.

## Out of scope
- Tenacity, per status policies, circuit changes.

## BDD scenarios
- Given defaults, when `retry_delay(1/2/3)`, then `0.6/1.2/2.4` within epsilon and capped at 30.
- Given `attempt=0`, when called, then same as 1.
- Given client with default, when constructed, then `max_retries` equals `RETRY.attempts`.
