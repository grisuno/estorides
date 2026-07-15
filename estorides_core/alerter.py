"""
estorides_core.alerter
======================
Alert channel dispatcher for watch target notifications.

Supports:
  * Slack webhook
  * Discord webhook (embedded messages)
  * Telegram bot
  * Email (SMTP)
  * Generic webhook (HTTP POST)

Each channel reads its credentials from environment variables so they are
never stored in the database.
"""
from __future__ import annotations

import json
import logging
import os
import smtplib
import time
import urllib.error
import urllib.request
from datetime import datetime
from email.mime.text import MIMEText
from typing import Any
from urllib.request import Request, urlopen

log = logging.getLogger("estorides.alerter")


# ---------------------------------------------------------------------------
# Cooldown — prevent alert storms: max 1 alert per channel per 5 min
# ---------------------------------------------------------------------------
_ALERT_COOLDOWN_S: float = 300.0
_last_alert: dict[str, float] = {}


def _check_cooldown(channel: str) -> bool:
    now = time.time()
    last = _last_alert.get(channel, 0.0)
    if now - last < _ALERT_COOLDOWN_S:
        log.debug("alert cooldown active for %s (%.0fs remaining)",
                  channel, _ALERT_COOLDOWN_S - (now - last))
        return False
    _last_alert[channel] = now
    return True


def _http_post(url: str, payload: dict[str, Any]) -> bool:
    """POST JSON payload to URL, return True on success."""
    try:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        with urlopen(req, timeout=10) as resp:
            return resp.status < 300
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
        log.warning("HTTP POST to %s failed: %s", url, e)
        return False


# ---------------------------------------------------------------------------
# Channel implementations
# ---------------------------------------------------------------------------

def _send_slack(webhook_url: str, title: str, body: str, severity: str) -> bool:
    """Send a Slack message via Incoming Webhook."""
    color_map = {"info": "#5B8FF9", "warning": "#F6BD16", "error": "#FF6B6B"}
    payload = {
        "attachments": [{
            "color": color_map.get(severity, "#5B8FF9"),
            "title": title,
            "text": body[:2000],
            "footer": "Estorides Monitor",
            "ts": int(time.time()),
        }],
    }
    return _http_post(webhook_url, payload)


def _send_discord(webhook_url: str, title: str, body: str, severity: str) -> bool:
    """Send a Discord embed via Webhook."""
    color_map = {"info": 6003455, "warning": 16167446, "error": 16711680}
    payload = {
        "embeds": [{
            "title": title[:256],
            "description": body[:2000],
            "color": color_map.get(severity, 6003455),
            "footer": {"text": "Estorides Monitor"},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }],
    }
    return _http_post(webhook_url, payload)


def _send_telegram(
    bot_token: str, chat_id: str, title: str, body: str, severity: str,
) -> bool:
    """Send a Telegram message via Bot API."""
    text = f"*{title}*\n\n{body[:3000]}"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    return _http_post(url, payload)


def _send_email(
    smtp_host: str, smtp_port: int, smtp_user: str, smtp_pass: str,
    from_addr: str, to_addr: str,
    title: str, body: str, severity: str,
) -> bool:
    """Send an email alert via SMTP."""
    try:
        msg = MIMEText(body[:5000], "plain", "utf-8")
        msg["Subject"] = f"[Estorides] {title[:200]}"
        msg["From"] = from_addr
        msg["To"] = to_addr
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return True
    except Exception as e:
        log.warning("email send failed: %s", e)
        return False


def _send_webhook(
    webhook_url: str, title: str, body: str, severity: str,
) -> bool:
    """Send a generic webhook POST."""
    payload = {
        "event": "estorides_alert",
        "severity": severity,
        "title": title,
        "body": body[:5000],
        "timestamp": time.time(),
    }
    return _http_post(webhook_url, payload)


# ---------------------------------------------------------------------------
# Alert Dispatcher
# ---------------------------------------------------------------------------
class AlertDispatcher:
    """Central alert dispatcher: routes alerts to configured channels.

    Reads channel credentials from environment variables on each dispatch
    so an operator can hot-configure without restarting.
    """

    def send(self, channel: str, title: str, body: str,
             severity: str = "info") -> bool:
        """Send an alert to a single channel. Returns True on success."""
        if not _check_cooldown(channel):
            return False

        channel = channel.strip().lower()
        if channel == "slack":
            url = os.environ.get("ESTORIDES_SLACK_WEBHOOK", "")
            if not url:
                log.warning("slack alert: ESTORIDES_SLACK_WEBHOOK not set")
                return False
            return _send_slack(url, title, body, severity)

        elif channel == "discord":
            url = os.environ.get("ESTORIDES_DISCORD_WEBHOOK", "")
            if not url:
                log.warning("discord alert: ESTORIDES_DISCORD_WEBHOOK not set")
                return False
            return _send_discord(url, title, body, severity)

        elif channel == "telegram":
            token = os.environ.get("ESTORIDES_TELEGRAM_BOT_TOKEN", "")
            chat_id = os.environ.get("ESTORIDES_TELEGRAM_CHAT_ID", "")
            if not token or not chat_id:
                log.warning("telegram alert: tokens not set")
                return False
            return _send_telegram(token, chat_id, title, body, severity)

        elif channel == "email":
            host = os.environ.get("ESTORIDES_SMTP_HOST", "")
            port = int(os.environ.get("ESTORIDES_SMTP_PORT", "587"))
            user = os.environ.get("ESTORIDES_SMTP_USER", "")
            pwd = os.environ.get("ESTORIDES_SMTP_PASS", "")
            to_addr = os.environ.get("ESTORIDES_ALERT_EMAIL", user)
            from_addr = os.environ.get("ESTORIDES_ALERT_FROM", user)
            if not host or not user or not pwd:
                log.warning("email alert: SMTP not configured")
                return False
            return _send_email(
                host, port, user, pwd, from_addr, to_addr,
                title, body, severity,
            )

        elif channel == "webhook" or channel.startswith("http"):
            url = channel if channel.startswith("http") else \
                os.environ.get("ESTORIDES_WEBHOOK_URL", "")
            if not url:
                log.warning("webhook alert: URL not set")
                return False
            return _send_webhook(url, title, body, severity)

        else:
            log.warning("unknown alert channel: %s", channel)
            return False

    def send_watch_alert(
        self, watch: Any, entity_count: int,
        obs_count: int, new_entities: int = 0,
    ) -> None:
        """Send alerts for a completed watch run to all configured channels."""
        title = f"🔄 Watch complete: {watch.query}"
        body = (
            f"Watch: {watch.id}\n"
            f"Query: {watch.query} ({watch.query_type})\n"
            f"Sources succeeded: {obs_count}\n"
            f"Entities found: {entity_count}\n"
            f"New entities since last run: {new_entities}\n"
            f"Next run: {_fmt_time(watch.next_run_at)}"
        )
        status = "info"
        for channel in watch.channels:
            ok = self.send(channel, title, body, severity=status)
            if ok:
                log.info("alert sent to %s for watch %s", channel, watch.id)

    def test(self, channel: str) -> bool:
        """Send a test alert to verify channel configuration."""
        return self.send(
            channel,
            "⚙️ Estorides Alert Test",
            "This is a test alert from Estorides monitoring.\n"
            "If you received this, your alert channel is configured correctly.",
            severity="info",
        )

    def available_channels(self) -> list[dict[str, Any]]:
        """Return list of configured channels with their status."""
        checks = {
            "slack": ("ESTORIDES_SLACK_WEBHOOK", "url"),
            "discord": ("ESTORIDES_DISCORD_WEBHOOK", "url"),
            "telegram": ("ESTORIDES_TELEGRAM_BOT_TOKEN", "token"),
            "email": ("ESTORIDES_SMTP_HOST", "smtp host"),
        }
        result = []
        for name, (env_var, _kind) in checks.items():
            configured = bool(os.environ.get(env_var))
            result.append({
                "name": name,
                "configured": configured,
                "env_var": env_var,
            })
        result.append({
            "name": "webhook",
            "configured": bool(os.environ.get("ESTORIDES_WEBHOOK_URL")),
            "env_var": "ESTORIDES_WEBHOOK_URL",
        })
        return result


def _fmt_time(ts: float) -> str:
    from datetime import datetime, timezone
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


# Singleton
dispatcher = AlertDispatcher()


__all__ = ["AlertDispatcher", "dispatcher"]
