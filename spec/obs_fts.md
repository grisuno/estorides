# obs_fts — Spec

## Purpose
I give free text search over observations without Elasticsearch. SQLite FTS5 only, fail soft when absent.

## Inputs
- `store.search_observations_fts(query, limit=20)` with plain words. Empty query returns [].
- Indexed: `source`, `parsed_json`, `raw_excerpt`.

## Outputs
- List of `{id, case_id, source, snippet}` ordered by rank. Snippet is FTS snippet with marks stripped to plain text.
- `fts_available()` bool.

## Error table
| Condition | Behaviour |
|---|---|
| FTS5 missing | table absent, methods return [], never raise |
| empty/malformed query | [], never raise |
| quote injection | passed as single parameter to MATCH, never concatenated |

## Security guarantees
- MATCH via `?` placeholder only. Snippet sanitized of `<b>` tags before return.

## Out of scope
- Facets, dates, ranking tunables.

## BDD scenarios
- Given two observations, when searching a rare word, then only matching row returns.
- Given empty query, when searched, then [].
- Given FTS missing, when searched, then [] without raise.
