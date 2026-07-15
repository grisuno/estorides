# Monitoring — Watch Targets & Alerting

**Spec version:** 1.0  
**Date:** 2026-07-14  
**Status:** draft  

---

## Purpose

Add continuous monitoring capabilities to Estorides: watch targets can be
scheduled for recurring OSINT scans, and changes detected between runs
trigger alerts via configurable channels (Slack, Discord, Telegram, Email,
generic webhook).

This turns Estorides from a "run it and forget it" query tool into a
persistent intelligence monitoring platform.

---

## Inputs

### WatchTarget

Each watch represents a recurring OSINT investigation:

```python
class WatchTarget:
    id: str                    # auto-generated sha1 prefix
    query: str                 # e.g. "example.com"
    query_type: str            # e.g. "domain"
    interval_minutes: int      # how often to re-run (min 15, max 43200 = 30d)
    next_run_at: float         # unix timestamp
    last_run_at: float | None
    last_status: str           # "pending" | "ok" | "error"
    channels: list[str]        # alert channel names
    enabled: bool
    created_at: float
    notes: str
```

### AlertChannel

```python
class AlertChannel(Protocol):
    name: str
    def send(self, title: str, body: str, severity: str) -> bool: ...
```

Built-in channels:
- `slack` — webhook URL via `ESTORIDES_SLACK_WEBHOOK`
- `discord` — webhook URL via `ESTORIDES_DISCORD_WEBHOOK`
- `telegram` — bot token + chat id via `ESTORIDES_TELEGRAM_BOT_TOKEN` + `ESTORIDES_TELEGRAM_CHAT_ID`
- `email` — SMTP config via env vars
- `webhook` — generic HTTP POST, URL per watch

---

## Outputs

### Watch list response

```json
{
  "watches": [
    {
      "id": "a1b2c3d4",
      "query": "example.com",
      "query_type": "domain",
      "interval_minutes": 1440,
      "next_run_at": 1700000000.0,
      "last_run_at": 1699913600.0,
      "last_status": "ok",
      "channels": ["slack", "telegram"],
      "enabled": true,
      "created_at": 1699827200.0,
      "notes": "Monitor example.com daily"
    }
  ]
}
```

### Alert payload

```json
{
  "watch_id": "a1b2c3d4",
  "query": "example.com",
  "severity": "info",
  "title": "🔄 Watch completed: example.com",
  "body": "Sources succeeded: 45/99\nEntities found: 127\nNew entities since last run: 12\nChanges detected: 3"
}
```

---

## Error handling

| Error | Code | Condition | Behaviour |
|-------|------|-----------|-----------|
| Invalid interval | `invalid_interval` | interval < 15 min | Reject with message |
| Unknown channel | `unknown_channel` | channel not configured | Fail watch creation |
| Watch not found | `not_found` | watch ID doesn't exist | 404 |
| Scheduler unavailable | `scheduler_unavailable` | APScheduler not installed | 503 |
| Channel send failed | `send_failed` | HTTP error from Slack/Discord | Log error, continue |

---

## Security guarantees

- **No hardcoded credentials**: All channel credentials come from environment
  variables or the watch's `channels` config.
- **No secrets in logs**: Alert bodies are truncated to 2000 chars before
  logging.
- **Rate-limited alerts**: Maximum 1 alert per channel per 5 minutes
  (cooldown window) to prevent alert storms.
- **Contact classification**: Watch runs use the same `contact` / `passive_only`
  rules as regular runs.

---

## Out of scope

- PagerDuty / OpsGenie / incident management integration (future).
- SLA monitoring / uptime checking.
- Real-time streaming watch (SSE). Watches are poll-based (cron-style).

---

## Escenarios BDD

### M1 — Create a watch target

```
Given: a valid query "example.com" of type "domain"
 When: a watch is created with interval=1440 minutes
 Then: the watch is saved with status "pending"
  And: next_run_at is in the future
  And: the watch appears in the watch list
```

### M2 — Watch runs and completes

```
Given: a watch with query="8.8.8.8" every 60 minutes
  And: the orchestrator is available
 When: the scheduler triggers the watch
 Then: the orchestrator runs with the watch's query
  And: last_status is updated to "ok"
  And: next_run_at is set to now + interval
```

### M3 — Alert sent on completion

```
Given: a watch with channels=["slack"]
  And: ESTORIDES_SLACK_WEBHOOK is configured
 When: the watch run completes successfully
 Then: a Slack webhook POST is sent
  And: the payload contains the watch's query and entity count
```

### M4 — Disable a watch

```
Given: an existing watch "a1b2c3d4"
 When: the watch is updated with enabled=false
 Then: the watch is not deleted
  And: its enabled field is false
  And: it will not be scheduled for future runs
```

### M5 — Delete a watch

```
Given: an existing watch "a1b2c3d4"
 When: the watch is deleted
 Then: the watch is removed from the database
  And: it no longer appears in the watch list
```

### M6 — Email alert channel

```
Given: ESTORIDES_SMTP_HOST, ESTORIDES_SMTP_USER, ESTORIDES_SMTP_PASS are set
  And: a watch with channels=["email"]
 When: the watch run completes
 Then: an email is sent to ESTORIDES_ALERT_EMAIL
  And: the subject contains the watch query
```

### M7 — Discord alert channel

```
Given: ESTORIDES_DISCORD_WEBHOOK is configured
  And: a watch with channels=["discord"]
 When: the watch run completes
 Then: a Discord embed is sent via webhook
  And: the embed title contains the watch query
```

### M8 — Telegram alert channel

```
Given: ESTORIDES_TELEGRAM_BOT_TOKEN and ESTORIDES_TELEGRAM_CHAT_ID are set
  And: a watch with channels=["telegram"]
 When: the watch run completes
 Then: a Telegram message is sent
  And: the message text contains the entity count
```

### M9 — Webhook alert channel

```
Given: a watch with channels=["webhook"]
  And: the watch has webhook_url configured
 When: the watch run completes
 Then: an HTTP POST is sent to the webhook_url
  And: the Content-Type is application/json
```

### M10 — Remove alerts on watch delete

```
Given: a watch with pending alerts
 When: the watch is deleted
 Then: no further alerts are sent for that watch
  And: the watch is removed from the scheduler
```

---

## Changelog

| Date | Change |
|------|--------|
| 2026-07-14 | Initial spec |
