# Issue #37: Reddit sources scrape the JSON API without OAuth, violating Reddit's ToS and causing IP blocking

- **State:** open
- **Created:** 2026-06-08T11:42:49Z
- **Updated:** 2026-06-08T11:42:49Z
- **Labels:** None

---

## Summary
Three Reddit sources (`reddit_about`, `reddit_posts`, `reddit_subreddit`) scrape the Reddit JSON API using a generic `User-Agent: Estorides/1.0` header and no OAuth credentials. Reddit's API Terms of Service (section 4) requires all API clients to use OAuth 2.0 authentication and to identify the application with a proper User-Agent string in the format `<platform>:<app ID>:<version string> (by /u/<reddit username>)`. Unauthenticated use of the JSON API endpoints is subject to rate-limiting, blocking, and account/IP suspension.

## Evidence
`sources/04_social/reddit_about.yaml`:
```yaml
tool:
  method: GET
  url: https://www.reddit.com/user/{query}/about.json
  headers:
    User-Agent: Estorides/1.0
```

`sources/04_social/reddit_posts.yaml`:
```yaml
  url: https://www.reddit.com/user/{query}/submitted.json
  headers:
    User-Agent: Estorides/1.0
```

`sources/08_knowledge/reddit_subreddit.yaml`:
```yaml
  url: https://www.reddit.com/r/{query}/search.json
  headers:
    User-Agent: Estorides/1.0
```

The `env.example` does list `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET` as optional, but the YAML sources use the public `.json` endpoints without OAuth. The credentials are never wired into these sources.

## Why this matters
Reddit has been actively blocking unauthenticated API scrapers since its 2023 API policy change. Deployments that run Estorides at scale will have their IPs blocked by Reddit, breaking all three sources. More critically, the old public `.json` endpoints are now rate-limited to near-zero without OAuth, so results are unreliable. The collected Reddit data may also have GDPR implications depending on jurisdiction.

## Attack or failure scenario
1. An operator configures Estorides and runs it against many usernames.
2. Reddit detects the generic User-Agent and unauthenticated pattern, and rate-limits or blocks the egress IP.
3. All Reddit sources return empty results silently; the operator receives no feedback that the data is missing.
4. In a cloud deployment with a shared NAT IP, all other services on that IP also get blocked from Reddit.

## Root cause
The Reddit sources were implemented against the old public JSON API without OAuth. The optional `REDDIT_CLIENT_ID`/`REDDIT_CLIENT_SECRET` environment variables are documented but never wired into the source YAML headers or the orchestrator's `_resolve_auth` flow.

## Recommended fix
1. Implement OAuth 2.0 client-credentials flow for Reddit in the source YAML or a pre-fetch hook in the orchestrator.
2. Update the User-Agent to comply with Reddit's requirements: `Estorides/1.0 (by /u/<operator_username>)`.
3. Wire `REDDIT_CLIENT_ID`/`REDDIT_CLIENT_SECRET` into the source definitions and mark them `requires_key: true` so the sources are skipped when no credentials are set.
4. Document the Reddit OAuth setup procedure in the README.

## Acceptance criteria
- All three Reddit sources are marked `requires_key: true` with `key_env: REDDIT_CLIENT_ID`.
- A pre-fetch authenticator (or a `before_fetch` hook) exchanges the client credentials for an OAuth bearer token before hitting Reddit endpoints.
- The User-Agent complies with Reddit's format requirements.
- The `status` command shows these sources as disabled when no Reddit credentials are configured.

## Suggested labels
security, bug, technical-debt

## Priority
P2

## Severity
High — Terms of Service violation that will result in IP blocking in production and may expose operators to legal risk under Reddit's API agreement.

## Confidence
Confirmed — the YAML sources make unauthenticated requests to reddit.com JSON endpoints.
