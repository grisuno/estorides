# `wsgi`

> Source: [wsgi.py:1](../../wsgi.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

estorides.wsgi ==============

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
