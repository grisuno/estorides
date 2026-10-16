# `web`

> Source: [web.py:1](../../web.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Deprecated entry point.

Use:

- `python3 estorides_cli.py serve` for the dev server, or
  - `gunicorn -w 4 wsgi:app` for production.

This file is kept as a redirect so old launchers that import from this
module keep working.
