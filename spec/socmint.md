# SOCMINT — Social Media Intelligence Module

**Spec version:** 1.0  
**Date:** 2026-07-14  
**Status:** draft  

---

## Purpose

Expand the social media intelligence (SOCMINT) capabilities of Estorides beyond
the existing GitHub/Reddit/Mastodon/Keybase/Telegram sources. Add support for:

- **YouTube** — channel/profile lookup, video metadata, subscriber counts
- **Twitter/X** — user profile lookup (API v2, requires paid tier)
- **Twitch** — user profile, channel metadata, follower counts
- **Discord** — public server discovery via discords.com/disboard.org
- **SocialMediaInferer** — cross-platform entity linking engine that correlates
  usernames across all known social platforms into unified person profiles

The module follows the existing YAML source + parser pattern: each platform is
a separate YAML addon with a registered parser function. The SocialMediaInferer
is a pure Python module that aggregates across sources.

---

## Inputs

### Per-source inputs (YAML-driven)

Each source accepts a `{query}` parameter, typically a username or channel ID:

| Source | Query type | Format | Key required? |
|--------|-----------|--------|---------------|
| YouTube | `username` | handle (e.g. `@mkbhd`) | Yes (Google API key) |
| Twitter/X | `username` | handle (e.g. `elonmusk`) | Yes (X API Bearer token) |
| Twitch | `username` | login (e.g. `shroud`) | Yes (Twitch Client-ID) |
| Discord | `keyword` | server name (e.g. `cybersecurity`) | No (public scraper) |

### SocialMediaInferer inputs

```python
class SocmintInput:
    username: str
    platforms: list[str] | None  # None = check all known platforms
```

### Platform registry

The `PLATFORM_REGISTRY` dict maps platform names to their source metadata:

```python
PLATFORM_REGISTRY: dict[str, PlatformInfo] = {
    "github": PlatformInfo(...),
    "reddit": PlatformInfo(...),
    "twitter": PlatformInfo(...),
    "youtube": PlatformInfo(...),
    "twitch": PlatformInfo(...),
    "discord": PlatformInfo(...),
    "mastodon": PlatformInfo(...),
    "keybase": PlatformInfo(...),
    "hackernews": PlatformInfo(...),
    "telegram": PlatformInfo(...),
}
```

---

## Outputs

### YouTube parser output

```json
{
  "kind": "youtube_channel",
  "channel_id": "UC...",
  "title": "Marques Brownlee",
  "description": "Tech reviews...",
  "custom_url": "@mkbhd",
  "published_at": "2010-01-15T00:00:00Z",
  "country": "US",
  "view_count": 4500000000,
  "subscriber_count": 18000000,
  "video_count": 1500,
  "avatar_url": "https://...",
  "banner_url": "https://...",
  "topic_ids": ["/m/07c1v", "/m/04rlf"],
  "keywords": ["tech", "reviews"],
  "social_links": ["https://twitter.com/MKBHD"]
}
```

### Twitter/X parser output

```json
{
  "kind": "twitter_user",
  "id": "123456789",
  "name": "Elon Musk",
  "username": "elonmusk",
  "description": "...",
  "location": "Austin, TX",
  "verified": true,
  "followers_count": 150000000,
  "following_count": 500,
  "tweet_count": 25000,
  "listed_count": 120000,
  "created_at": "2010-06-02T20:12:30Z",
  "profile_image_url": "https://...",
  "url": "https://t.co/...",
  "protected": false
}
```

### Twitch parser output

```json
{
  "kind": "twitch_user",
  "id": "12345678",
  "login": "shroud",
  "display_name": "shroud",
  "description": "Former pro CS:GO...",
  "type": "partner",
  "broadcaster_type": "partner",
  "view_count": 120000000,
  "followers_count": 10000000,
  "created_at": "2013-08-15T00:00:00Z",
  "offline_image_url": "https://...",
  "profile_image_url": "https://..."
}
```

### Discord parser output

```json
{
  "kind": "discord_server",
  "id": "123456789012345678",
  "name": "CyberSec Community",
  "description": "A community for cybersecurity...",
  "approximate_member_count": 15000,
  "approximate_presence_count": 2500,
  "vanity_url_code": null,
  "features": ["COMMUNITY", "NEWS"],
  "discovery_url": "https://discord.com/servers/...",
  "icon_url": "https://cdn.discordapp.com/..."
}
```

### SocialMediaInferer output

```python
class ProfileMatch:
    platform: str
    username: str
    display_name: str | None
    profile_url: str | None
    verified: bool
    confidence: float  # 0.0 - 1.0
    metadata: dict

class SocialMediaProfile:
    username: str
    display_name: str | None
    email: str | None
    location: str | None
    bio: str | None
    avatar_url: str | None
    platform_profiles: list[ProfileMatch]
    linked_platforms: list[LinkedPlatform]  # e.g., GitHub showing Twitter handle
    cross_platform_confidence: float
    last_updated: float
```

---

## Error handling

| Error | Code | Condition | Behaviour |
|-------|------|-----------|-----------|
| Missing API key | `missing_key` | `requires_key: true` + no env var | Skip source gracefully (existing mechanism) |
| API error | `api_error` | Non-2xx HTTP response | Return `{"error": "api_error", "detail": "..."}` |
| Not found | `not_found` | 404 or empty result | Return `{"error": "not_found"}` |
| Rate limited | `rate_limited` | 429 response | Return with retry-after header (existing circuit breaker handles) |
| Invalid username | `invalid_query` | Query doesn't match expected pattern | Return `{"error": "invalid_query"}` |
| SocialMediaInferer: no matches | `no_matches` | No platform found the username | Return `{"profiles": [], "no_matches": true}` |

---

## Security guarantees

- **No API keys stored on disk**: keys read from environment at call time via existing `_resolve_auth()` mechanism.
- **Passive sources only**: ALL new sources are `contact: none` (they hit third-party APIs, never the target directly).
- **Output sanitisation**: All raw API responses go through structured parsers before reaching the LLM analyst; no raw HTML/script content from social platforms flows unprocessed.
- **Rate limiting**: Existing per-IP sliding window (30/min default) applies to all endpoints.
- **YouTube**: Requires `GOOGLE_API_KEY` env var (free tier: 10,000 quota units/day).
- **Twitter/X**: Requires `TWITTER_BEARER_TOKEN` env var (Basic tier $100/mo for read access).
- **Twitch**: Requires `TWITCH_CLIENT_ID` + `TWITCH_CLIENT_SECRET` (free, standard rate limits).
- **Discord**: No key required; uses public discords.com scraper (passive, rate-limit aware).

---

## Out of scope

- Posting/commenting/interacting on any platform.
- Scraping private/protected profiles.
- Social graph crawling (friends/followers of followers).
- Dark web social platforms.
- TikTok (API restricted to academic researchers only per 2026 policy).
- Instagram (Basic Display API deprecated Dec 2024; Graph API requires Business account).
- LinkedIn (scraping explicitly prohibited per ToS; API requires partnership).

---

## Escenarios BDD Given-When-Then

### S1 — YouTube channel lookup (happy path)

```
Given: a valid Google API key is set
  And: a YouTube username "@mkbhd" is queried
 When: the youtube_user source is executed
 Then: it returns a parsed dict with channel_id, title, subscriber_count
  And: subscriber_count is a non-negative integer
```

### S2 — YouTube channel not found

```
Given: a valid Google API key is set
  And: a YouTube username "@nonexistent_channel_abc123xyz" is queried
 When: the youtube_user source is executed
 Then: it returns {"error": "not_found"}
```

### S3 — YouTube without API key

```
Given: GOOGLE_API_KEY is not set
  And: the youtube_user source requires a key
 When: the orchestrator selects sources with include_paid=False
 Then: the source is not included in the target list
```

### S4 — Twitch user lookup (happy path)

```
Given: valid Twitch credentials are set
  And: a Twitch username "shroud" is queried
 When: the twitch_user source is executed
 Then: it returns a parsed dict with id, login, display_name, followers_count
  And: followers_count is a non-negative integer
```

### S5 — Twitch user not found

```
Given: valid Twitch credentials are set
  And: a Twitch username "this_user_does_not_exist_ever" is queried
 When: the twitch_user source is executed
 Then: it returns {"error": "not_found"}
```

### S6 — Twitter/X user lookup (happy path)

```
Given: a valid X API Bearer token is set
  And: a Twitter username "elonmusk" is queried
 When: the twitter_user source is executed
 Then: it returns a parsed dict with id, name, username, followers_count
  And: username matches the query
```

### S7 — Discord server search (happy path)

```
Given: a keyword "cybersecurity" is queried
 When: the discord_discovery source is executed
 Then: it returns a list of server results with name and description
  And: at least one result matches the query
```

### S8 — SocialMediaInferer correlates across platforms

```
Given: a username "torvalds" is known
  And: the platform registry has GitHub, Twitter, Reddit, Mastodon, Keybase
 When: SocialMediaInferer.resolve("torvalds") is called
 Then: it returns a SocialMediaProfile with at least 2 platform_profiles
  And: at least one profile has verified=True (Keybase)
  And: cross_platform_confidence > 0.5
```

### S9 — SocialMediaInferer handles unknown username

```
Given: a username "xqkz_nonexistent_999" is queried
 When: SocialMediaInferer.resolve("xqkz_nonexistent_999") is called
 Then: it returns {"profiles": [], "no_matches": true}
```

### S10 — YouTube parser handles malformed response

```
Given: the youtube_user parser receives a non-dict input (None, list, int)
 When: the parser is called
 Then: it returns {"error": "unexpected_response"}
```

### S11 — Twitch parser handles error responses

```
Given: the twitch_user parser receives a response with status 401 or 429
 When: the parser is called
 Then: it returns {"error": "api_error", "detail": "..."} 
```

### S12 — Entity extraction from social media profiles

```
Given: a YouTube parser output with display_name "John Doe"
  And: and social_links containing "twitter.com/johndoe"
 When: extract_structured() processes the parser output
 Then: it extracts a "person" entity with value "John Doe"
  And: it extracts a "username" entity from the twitter URL
```

---

## Changelog

| Date | Change |
|------|--------|
| 2026-07-14 | Initial spec (YouTube, Twitter/X, Twitch, Discord, SocialMediaInferer) |
