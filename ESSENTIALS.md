# Estorides — Essentials

State-level OSINT orchestrator. 100+ free public sources, async fanout,
knowledge graph, multi-LLM analyst. This file is the 80/20 cheatsheet:
install, run, and the 12 commands that cover 90% of operator workflows.

## 60-second install

```bash
git clone https://github.com/grisuno/estorides.git
cd estorides
./install.sh             # full install (kuzu + aiohttp_socks + gunicorn)
# or
./install.sh --minimal   # if kuzu / aiohttp_socks fail to build (ARM, musl)

cp .env.example .env     # optional: add API keys for paid sources
```

The script:
  * creates a venv at `./env`,
  * runs `pip install -e .` (registers the `estorides` console script),
  * falls back to a minimal install with a clear warning if native deps fail,
  * prints the next commands.

## Run it

```bash
estorides status                              # list 100+ sources / 13 categories
estorides run example.com                     # free sources only
estorides run user@example.com --include-paid # add API-key sources
estorides discover example.com                # recursive surface walk
estorides discover 8.8.8.8 --passive-only     # no target-touching sources
estorides report <case_id> --diff <older>     # Markdown report w/ diff
estorides diff <case_a> <case_b>              # CLI diff
estorides serve --port 5050                   # dev server (loopback)
gunicorn -w 4 -b 127.0.0.1:5050 wsgi:app      # production
```

## Web UI (http://127.0.0.1:5050)

  * **Run** — single query, sources fanout, results populate as they arrive.
  * **Discover** — recursive background fanout. Live SSE feed into the UI
    (the surface grows as you watch).
  * **Map** — every geolocated result on Leaflet 2D.
  * **Graph** — D3 force-directed knowledge graph with clusters, transforms,
    and click-to-enrich.
  * **Timeline** — source acquisition over time.
  * **Cases** — every run is a case. Save / diff / replay from here.
  * **Intel** — cross-feed resolver (Wikidata, OFAC, NVD, IP-API).

## OPSEC flags (apply to `run` and `discover`)

```bash
--passive-only      # only sources marked contact=none (no probes to target)
--tor               # shortcut for --proxy socks5://127.0.0.1:9050
--proxy URL         # route all egress through this proxy
--parallel N        # concurrent sources per step (default 8)
--timeout S         # per-source HTTP timeout (default 8s)
--deadline S        # hard wall-clock cap for the whole run (default 30s)
```

## Output formats

```bash
estorides stix --out bundle.json            # STIX 2.1 bundle
estorides misp --out event.json             # MISP event JSON
estorides graph --export graphml            # for Gephi / Cytoscape
# Encrypted export — pass an age recipient over the web:
#   curl 'http://127.0.0.1:5050/api/export/stix?key=age1xxx...'
```

## Where things live

```
sources/                100+ YAML addons, drop-in
estorides_core/         engine, knowledge graph, SSRF guard, web security
estorides_llm/          multi-backend LLM manager
estorides_export/       STIX, MISP, encrypted (age), Markdown report
templates/, static/     web UI
data/                   dataset, graph, cache, case store (gitignored)
reports/                generated Markdown / STIX / MISP
wsgi.py                 gunicorn entry point
pyproject.toml          console script + optional deps
```

## Validate after install

```bash
python3 _validate.py     # runs every offline test suite
```

## Uninstall / reset

```bash
rm -rf env data reports
```
