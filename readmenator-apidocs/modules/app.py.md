# `app`

> Source: [app.py:1](../../app.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Deprecated entry point.

Use:

- the `estorides` console script (installed by `pip install -e .`), or
  - `python3 estorides_cli.py serve` for the dev server, or
  - `gunicorn -w 4 wsgi:app` for production.

This file is kept as a redirect so old launchers that import [`app`](app.py.md) from
this module keep working. It intentionally does NOT start a server on
import.
