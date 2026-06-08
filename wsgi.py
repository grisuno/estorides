"""
estorides.wsgi
==============

WSGI entry point for production deployments.

Run with gunicorn (already pinned in requirements.txt):

    gunicorn -w 4 -b 0.0.0.0:5050 --timeout 120 --access-logfile - wsgi:app

Environment variables that matter for prod:
  ESTORIDES_HOST          bind address (default 127.0.0.1 — loopback only)
  ESTORIDES_PORT          port (default 5050)
  ESTORIDES_CORS_ORIGINS  comma-separated allowlist for browser CORS
  ESTORIDES_HSTS          1 to emit Strict-Transport-Security (only behind TLS)
  ESTORIDES_FORCE_HTTPS   1 to redirect plain http to https (only behind TLS)
  ESTORIDES_MAX_BODY_BYTES   int, default 1 MiB

The Werkzeug dev server in estorides_web.py is single-threaded and not safe
to expose. Do not use `python3 estorides_web.py` in production; use this
entry point.
"""
from __future__ import annotations

import logging
import os

# Force the dev-server flag off BEFORE importing the app. This is belt-and-
# braces: `install_security` in estorides_core/web_security.py also refuses
# to register routes when DEBUG is on, so even a misconfigured FLASK_DEBUG=1
# in the environment will cause `create_app()` to raise.
os.environ.setdefault("FLASK_DEBUG", "0")
os.environ.setdefault("ESTORIDES_DEBUG", "0")

# Bind to loopback by default. Operators exposing this on a network port
# must set ESTORIDES_HOST=0.0.0.0 explicitly so the intent is documented.
os.environ.setdefault("ESTORIDES_HOST", "127.0.0.1")

# Lazy import: the app factory reads the env, so the os.environ overrides
# above have to land first.
from estorides_web import create_app  # noqa: E402

log = logging.getLogger("estorides.wsgi")
log.info(
    "wsgi: bind=%s:%s cors=%s hsts=%s",
    os.environ.get("ESTORIDES_HOST"),
    os.environ.get("ESTORIDES_PORT", "5050"),
    "on" if os.environ.get("ESTORIDES_CORS_ORIGINS") else "off",
    os.environ.get("ESTORIDES_HSTS", "0"),
)

app = create_app()
