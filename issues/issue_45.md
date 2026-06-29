# Issue #45: WiGLE source references non-existent env var WIGLE_API_NAME_WIGLE_API_API_KEY — source never authenticates

- **State:** closed
- **Created:** 2026-06-08T11:43:26Z
- **Updated:** 2026-06-29T16:31:18Z
- **Labels:** None

---

## Summary
The WiGLE WiFi network geolocation source (`sources/09_wireless/wigle_search.yaml`) specifies an incorrect API key environment variable name: `WIGLE_API_NAME_WIGLE_API_API_KEY`. The correct WiGLE API key environment variables are `WIGLE_API_NAME` and `WIGLE_API_TOKEN` (as documented in `.env.example`). Because the source references a non-existent env var, it will never authenticate to WiGLE even when a valid key is configured by the operator. This causes the source to silently fail or attempt unauthenticated requests, which WiGLE rejects.

## Evidence
`sources/09_wireless/wigle_search.yaml` line 7:
```yaml
requires_key: true
key_env: WIGLE_API_NAME_WIGLE_API_API_KEY   # WRONG - this env var never exists
```

`.env.example` (the correct names):
```
# WIGLE_API_NAME=
# WIGLE_API_TOKEN=
```

WiGLE's API v2 uses HTTP Basic Authentication with `api_name:api_token`. The YAML source only supports a single `key_env` field for the `{api_key}` template placeholder, so neither `WIGLE_API_NAME` nor `WIGLE_API_TOKEN` alone is sufficient. The source YAML would need to support Basic Auth header construction.

## Why this matters
1. Operators who set `WIGLE_API_NAME` and `WIGLE_API_TOKEN` as documented in `.env.example` will see the source silently skip (because `requires_key: true` and `WIGLE_API_NAME_WIGLE_API_API_KEY` is unset) or attempt an unauthenticated request.
2. WiGLE's API requires authentication for all requests; unauthenticated requests return 401.
3. The source is non-functional as shipped — operators cannot use WiGLE even with valid credentials.

## Attack or failure scenario
An operator investigating wireless networks sets `WIGLE_API_NAME=myname` and `WIGLE_API_TOKEN=mytoken` as instructed by the README. They run a wireless query. The WiGLE source is skipped because `os.environ.get("WIGLE_API_NAME_WIGLE_API_API_KEY")` returns `None`. No error is surfaced — the source just produces no output.

## Root cause
The env var name was mistyped during YAML authoring and no automated test validates that `key_env` references correspond to names listed in `.env.example` or that the source actually authenticates correctly.

## Recommended fix
1. Fix the `key_env` typo. Since WiGLE uses Basic Auth with two fields, the simplest fix is to construct a combined credential:
   ```yaml
   key_env: WIGLE_ENCODED_KEY   # operator sets WIGLE_ENCODED_KEY=$(echo -n "name:token" | base64)
   headers:
     Authorization: "Basic {api_key}"
   ```
2. Alternatively, extend the source YAML schema to support `basic_auth: {user_env: WIGLE_API_NAME, pass_env: WIGLE_API_TOKEN}` and implement the Basic Auth construction in the async client.
3. Add a test that for every source with `requires_key: true`, the `key_env` value exists in `.env.example` comments.

## Acceptance criteria
- The WiGLE source authenticates correctly when `WIGLE_API_NAME` and `WIGLE_API_TOKEN` are set.
- The `estorides status` command shows the WiGLE source as active when the correct env vars are present.
- A test validates that `key_env` values in YAML sources correspond to documented env var names.

## Suggested labels
bug, technical-debt

## Priority
P2

## Severity
Medium — Source is entirely non-functional for all operators, but only for WiFi OSINT. No security impact, but represents a reliability failure for the WiGLE integration.

## Confidence
Confirmed — the `key_env` value `WIGLE_API_NAME_WIGLE_API_API_KEY` does not match any env var name in `.env.example` or documented elsewhere.
