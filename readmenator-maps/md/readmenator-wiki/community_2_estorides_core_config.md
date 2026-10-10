# estorides_core: config

*Community 2 | 19 files | cohesion 0.37*

## Definition

This community groups 19 file(s) rooted at `estorides_core` with dominant language py (cohesion 0.37). Central symbols: `AlertDispatcher`, `AsyncClient`, `BufferedEventSink`, `CacheConfig`, `CircuitBreaker`, `EarthquakesFeed`, `EntityRunner`, `EventSink`. Core file: `tests/test_security_remediation.py` (67 symbols). Documented purpose: estorides_core.__init__.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/__init__.py` | py | utility | 0 | yes |
| `estorides_core/alerter.py` | py | utility | 15 | yes |
| `estorides_core/async_client.py` | py | infrastructure | 21 | yes |
| `estorides_core/config.py` | py | infrastructure | 26 | yes |
| `estorides_core/feeds.py` | py | utility | 16 | yes |
| `estorides_core/observation_models.py` | py | business_logic | 14 | yes |
| `estorides_core/osiris_sources.py` | py | utility | 8 | yes |
| `estorides_core/pivot_engine.py` | py | utility | 25 | yes |
| `estorides_core/ssrf_guard.py` | py | utility | 12 | yes |
| `tests/properties/test_observation_models_properties.py` | py | testing | 7 | yes |
| `tests/test_async_client.py` | py | testing | 15 | yes |
| `tests/test_config_env.py` | py | testing | 13 | yes |
| `tests/test_monitoring.py` | py | testing | 35 | yes |
| `tests/test_observation_models.py` | py | testing | 28 | yes |
| `tests/test_orchestrator_fanout.py` | py | testing | 9 | yes |
| `tests/test_parsers.py` | py | testing | 9 | yes |
| `tests/test_retry_policy.py` | py | testing | 2 | yes |
| `tests/test_security_remediation.py` | py | testing | 67 | no |
| `tests/test_structured_extraction.py` | py | testing | 8 | yes |

## Key Symbols

- `_check_cooldown` (function, `estorides_core/alerter.py:42`) `def _check_cooldown(channel)`
- `_NoRedirectHandler` (class, `estorides_core/alerter.py:53`) `class _NoRedirectHandler(HTTPRedirectHandler)` - Refuse every HTTP redirect.
- `redirect_request` (method, `estorides_core/alerter.py:64`) `def redirect_request(self, req, fp, code, msg, headers, newurl)`
- `_http_post` (method, `estorides_core/alerter.py:77`) `def _http_post(url, payload)` - POST JSON payload to URL, return True on success.
- `_send_slack` (method, `estorides_core/alerter.py:111`) `def _send_slack(webhook_url, title, body, severity)` - Send a Slack message via Incoming Webhook.
- `_send_discord` (method, `estorides_core/alerter.py:126`) `def _send_discord(webhook_url, title, body, severity)` - Send a Discord embed via Webhook.
- `_send_telegram` (method, `estorides_core/alerter.py:141`) `def _send_telegram(bot_token, chat_id, title, body, severity)` - Send a Telegram message via Bot API.
- `_send_email` (method, `estorides_core/alerter.py:156`) `def _send_email(smtp_host, smtp_port, smtp_user, smtp_pass, from_addr, to_addr,` - Send an email alert via SMTP.
- `_send_webhook` (method, `estorides_core/alerter.py:177`) `def _send_webhook(webhook_url, title, body, severity)` - Send a generic webhook POST.
- `AlertDispatcher` (class, `estorides_core/alerter.py:194`) `class AlertDispatcher` - Central alert dispatcher: routes alerts to configured channels.
- `send` (method, `estorides_core/alerter.py:201`) `def send(self, channel, title, body, severity)` - Send an alert to a single channel. Returns True on success.
- `send_watch_alert` (method, `estorides_core/alerter.py:260`) `def send_watch_alert(self, watch, entity_count, obs_count, new_entities)` - Send alerts for a completed watch run to all configured channels.
- `test` (method, `estorides_core/alerter.py:280`) `def test(self, channel)` - Send a test alert to verify channel configuration.
- `available_channels` (method, `estorides_core/alerter.py:290`) `def available_channels(self)` - Return list of configured channels with their status.
- `_fmt_time` (method, `estorides_core/alerter.py:314`) `def _fmt_time(ts)`
- `_is_socks` (function, `estorides_core/async_client.py:49`) `def _is_socks(proxy)` - True when the proxy URL is a SOCKS proxy (e.g. Tor).
- `_redact_proxy` (function, `estorides_core/async_client.py:54`) `def _redact_proxy(proxy)` - Strip any `user:pass@` credentials from a proxy URL before logging.
- `CircuitBreaker` (class, `estorides_core/async_client.py:64`) `class CircuitBreaker` - Per-host circuit breaker.
- `allow` (method, `estorides_core/async_client.py:69`) `def allow(self, host)`
- `record_success` (method, `estorides_core/async_client.py:75`) `def record_success(self, host)`
- `record_failure` (method, `estorides_core/async_client.py:79`) `def record_failure(self, host)`
- `ResponseCache` (class, `estorides_core/async_client.py:86`) `class ResponseCache` - SQLite-backed response cache. Key = (url + method + body hash).
- `__init__` (method, `estorides_core/async_client.py:95`) `def __init__(self, path)`
- `_conn` (method, `estorides_core/async_client.py:109`) `def _conn(self)` - Short-lived connection that is always closed.
- `_init_db` (method, `estorides_core/async_client.py:123`) `def _init_db(self)`
- `_key` (method, `estorides_core/async_client.py:136`) `def _key(method, url, body)`
- `get` (method, `estorides_core/async_client.py:145`) `def get(self, method, url, body)`
- `set` (method, `estorides_core/async_client.py:161`) `def set(self, method, url, body, value)`
- `AsyncClient` (class, `estorides_core/async_client.py:172`) `class AsyncClient` - Async HTTP client with retries, backoff, circuit breaker, cache.
- `__init__` (method, `estorides_core/async_client.py:175`) `def __init__(self)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 42
- Cross-boundary resolved imports (EXTRACTED): 51

## Connections

- [EXTRACTED] depends_on community 4 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 1 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_core/audit.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 8 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_core/entity_extraction.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 3 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_core/fusion_store.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 0 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_core/intel_resolver.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 7 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_core/knowledge_graph.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 6 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_core/tool_install.py imports estorides_core/config.py.

## Risks

- [taint medium] `estorides_core/alerter.py` -> `estorides_core/alerter.py` via `urllib.request` (0 hops)
- [taint medium] `estorides_core/alerter.py` -> `estorides_core/ssrf_guard.py` via `urllib.request` (1 hops)
- [taint medium] `estorides_core/alerter.py` -> `estorides_core/alerter.py` via `urllib.request` (0 hops)
- [taint medium] `estorides_core/alerter.py` -> `estorides_core/ssrf_guard.py` via `urllib.request` (1 hops)
- [taint medium] `estorides_core/async_client.py` -> `estorides_core/async_client.py` via `requests` (0 hops)
- [taint medium] `estorides_core/async_client.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/async_client.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/feeds.py` via `requests` (0 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/feeds.py` via `requests` (0 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/feeds.py` via `requests` (0 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `tests/test_security_remediation.py`)? What purpose do they serve?
- Is the dangerous import `urllib.request` in `estorides_core/alerter.py` still required, or can it be isolated?
- What would break if the most connected file in estorides_core: config changed?
- Should estorides_core: config be split, given cohesion 0.37?

## Sources

- `estorides_core/__init__.py`
- `estorides_core/alerter.py`
- `estorides_core/async_client.py`
- `estorides_core/config.py`
- `estorides_core/feeds.py`
- `estorides_core/observation_models.py`
- `estorides_core/osiris_sources.py`
- `estorides_core/pivot_engine.py`
- `estorides_core/ssrf_guard.py`
- `tests/properties/test_observation_models_properties.py`
- `tests/test_async_client.py`
- `tests/test_config_env.py`
- `tests/test_monitoring.py`
- `tests/test_observation_models.py`
- `tests/test_orchestrator_fanout.py`
- `tests/test_parsers.py`
- `tests/test_retry_policy.py`
- `tests/test_security_remediation.py`
- `tests/test_structured_extraction.py`
