# sources

One YAML per origin. The loader (`estorides_core/source_loader.py`) recurses
into the numbered category directories, so a new source is a new file — no
engine change required.

## Conventions

* Filename stem == `name`.
* `category` matches the directory's number and label (e.g.
  `sources/05_threat/` -> `05. Threat Intelligence`).
* `parser` must exist in `estorides_core/parsers.py`; unknown names silently
  fall back to `raw_text`, which hides typos.
* `contact` is deliberate: `none` (the third party already publishes the
  record, e.g. CT logs, RDAP, registries), `broker` (the vendor acts on the
  target's behalf, e.g. TLS scanning, infostealer lookup) or `active` (we
  touch the target).
* `applies_to` uses the query types from
  `estorides_core/entity_extraction.py` (`domain`, `ipv4`, `ipv6`, `mac`,
  `email`, `asn`, `cve`, `username`, `md5`/`sha1`/`sha256`, `btc_address`,
  `eth_address`, `keyword`, `url`).
* Keyless sources are the default. If a key is unavoidable, use
  `requires_key: true` plus `key_env: ESTORIDES_<NAME>_KEY`; never inline a
  secret.

## Maintenance

`enabled: false` retires a dead endpoint without losing its history. The
2026-10 keyless survey that produced the `v1.5` batch (41 sources) is
documented in `docs/KEYLESS_ORIGINS_RESEARCH.md`, including the candidates
that were probed and rejected.
