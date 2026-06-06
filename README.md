# Estorides — OSINT Platform

## E.S.T.E.R.O.I.D.E.S.

- E – Entity (Identificación de entidades, alias, correos, IPs).

- S – Signals (Captura de huellas digitales y metadatos).

- T – Targeted (Focalizado en objetivos específicos).

- E – Extraction (Extracción automatizada de fuentes web).

- R – Reconnaissance (Reconocimiento y footprinting).

- O – Open-source (La naturaleza del motor OSINT).

- I – Intelligence (Procesamiento y correlación de datos).

- D – Data (Ingesta masiva de registros no estructurados).

- E – Engine (El motor central que orquesta las consultas).

- S – Scraper (Recolección automatizada y persistente).

Open-source intelligence (OSINT) aggregator and correlation engine
inspired by Palantir, Bellingcat, Maltego, and Citizen Lab workflows.
A pure open-source re-imagining of the original `fucklantir` /
`osint_palantir` toolchain, with a much bigger source catalogue, a
proper knowledge graph, structured parsers, and a multi-backend LLM
analyst.

No payloads. No active scanning. Just 99+ free public OSINT sources,
fanned out in parallel, fused into a single intelligence picture.

```
                       +--------------------------+
   query "example.com" |  Estorides Orchestrator  |   -> STIX 2.1 bundle
---------------------> |  - async fanout          |   -> MISP event JSON
                       |  - 99+ free sources      |   -> GraphML for Gephi
                       |  - structured parsers    |   -> JSONL for training
                       |  - entity resolution     |
                       |  - knowledge graph       |
                       |  - multi-LLM analyst     |
                       +--------------------------+
                                 |
                                 v
                          Web UI: map / graph / timeline / results
```

## What you get that the original does not

| Capability                              | Original    | Estorides |
| --------------------------------------- | ----------- | --------- |
| Number of free OSINT sources            | ~20         | **99**    |
| Intelligence categories                 | 6           | **12**    |
| HTTP fanout model                       | sequential  | **async** |
| Retries + backoff + circuit breaker     | basic       | **yes**   |
| Response cache (SQLite)                 | none        | **yes**   |
| Per-source parsers                      | none        | **50+**   |
| Entity extraction (IP, domain, CVE…)    | regex only  | **structured** + dedup |
| Knowledge graph                         | none        | **NetworkX** + GraphML |
| STIX 2.1 / MISP export                  | none        | **yes**   |
| Multi-LLM (Ollama / OpenAI / Anthropic) | Ollama only | **4 backends** + stub |
| Map (geolocation results)               | PyVista 3D  | **Leaflet 2D** |
| Force-directed graph view               | none        | **D3.js** |
| API key handling                        | none        | **per-source env vars** |
| Paid source support                     | none        | **flag-based opt-in** |

## Quickstart

### 1. Install (no extra packages needed; the project uses Flask + NetworkX + requests)

```bash
cd estorides
python3 -m pip install flask networkx requests pyyaml
```

Optional, for a real LLM:

```bash
# pick one
ollama serve && ollama pull llama3.1:8b
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export OPENROUTER_API_KEY=sk-or-...
```

### 2. CLI

```bash
# 99 sources, 12 categories
python3 estorides_cli.py status

# run a query (free sources only)
python3 estorides_cli.py run 8.8.8.8

# enable sources that need an API key
python3 estorides_cli.py run user@example.com --include-paid

# only a subset of sources
python3 estorides_cli.py run example.com \
    --only-sources crt_sh_certificates,shodan_internetdb,ipapi_free

# export the latest run as STIX 2.1 or MISP
python3 estorides_cli.py stix --out my_bundle.json
python3 estorides_cli.py misp --out my_event.json
```

### 3. Web UI

```bash
python3 estorides_cli.py serve --port 5050
# open http://127.0.0.1:5050
```

UI features:

- 2D map (Leaflet) of every geolocated result
- D3.js force-directed knowledge graph (drag, zoom, hover)
- Timeline of source acquisition
- Source results panel with per-source parsed output
- Filterable entity list
- LLM analysis with backend / model badge
- One-click export: STIX 2.1, MISP, GraphML, JSON

## 99 sources, 12 categories

01. DNS Intelligence       (9)  - Google DoH, Cloudflare DoH, HackerTarget,
                                 crt.sh, Cert Spotter, RDAP, DNS Dumpster, host search
02. IP & Infrastructure    (13) - ip-api, ipinfo, ipapi.co, ipwho.is, Shodan InternetDB,
                                 GreyNoise, ipwhois, Robtex, RDAP, AS lookup,
                                 AbuseIPDB, MAC OUI, RIPE Stat
03. Web Intelligence       (10) - urlscan, Wayback CDX, Wayback availability,
                                 HTTP headers, whois, geoip, traceroute, nping,
                                 Microlink, Google cache
04. Social Media           (13) - GitHub, Reddit, Mastodon, Keybase,
                                 HackerNews, Telegram, Pinterest, WordPress,
                                 Medium, DEV.to
05. Threat Intelligence    (13) - ThreatFox, URLhaus, payloads, PhishTank,
                                 OpenPhish, OTX (+passive domain/IP, no key),
                                 MalwareBazaar, Feodo, SSLBL,
                                 Emerging Threats, blocklist.de
06. Breach Intelligence    (6)  - HIBP breaches, HIBP pastes, Phonebook email,
                                 Phonebook domain, DeHashed, IntelligenceX
07. Geolocation            (5)  - Nominatim search + reverse, OpenWeather
                                 geocoding, TimeZoneDB, Wikidata
08. Knowledge              (12) - Wikipedia, summary, DuckDuckGo IA, OpenAlex,
                                 Crossref, arXiv, GitHub advisories, NVD CVE,
                                 cve.circl, ExploitDB, Reddit subreddit search
09. Wireless               (5)  - WiGLE, IEEE OUI, OpenSky, MarineTraffic, N2YO
10. Blockchain             (5)  - blockchain.info (balance + tx), Blockstream,
                                 Ethplorer, mempool.space
11. Paste & Leaks          (4)  - psbdmp, GitHub gist search, TGStat, LeakCheck
12. Visual                 (4)  - ScreenshotMachine, Microlink, TinEye, EXIF

Sources are addons: one YAML file per source, organised into category
subdirectories under `sources/` (lazyaddons-style). The loader recurses, so
add a new source by dropping `sources/<NN_category>/<name>.yaml` — no central
registry to edit. Grouped multi-document files still load if present. Point
`ESTORIDES_SOURCES_DIR` at another tree to use your own addon set. The schema
is documented at the top of `estorides_core/source_loader.py`.

```
sources/
  01_dns/
    dns_google.yaml
    crt_sh_certificates.yaml
  02_ip_infra/
    shodan_internetdb.yaml
  ...
```

`tools/split_sources.py` migrates legacy grouped files into this layout.

## Architecture

```
sources/                  one YAML per addon, grouped by category dir (99 addons)
estorides_core/
    config.py             every tunable (env-overridable)
    source_loader.py      registry, validation, lookup
    async_client.py       aiohttp + circuit breaker + SQLite cache
    parsers.py            50+ structured parsers (ipapi, dns_json, crtsh…)
    entity_extraction.py  regex-based entity finder with dedup
    knowledge_graph.py    NetworkX MultiDiGraph + GraphML export
    orchestrator.py       glues everything, infers higher-level relations
estorides_llm/
    manager.py            multi-backend LLM (Ollama → OpenRouter → Anthropic → OpenAI → stub)
estorides_export/
    stix.py               STIX 2.1 bundle export
    misp.py               MISP event JSON export
estorides_cli.py          argparse CLI
estorides_web.py          Flask app
templates/index.html      UI
static/{css,js}/estorides.*  UI styles + D3 controller
```

## Tips for a real run

1. Start with the free-tier sources (default) — that is 80+ endpoints.
2. Set `ESTORIDES_PARALLEL=16` for faster fanout.
3. Set `ESTORIDES_TIMEOUT=20` if your network is slow.
4. Disable paid sources you don't have keys for by setting
   `ESTORIDES_DISABLE_BACKENDS=openai,anthropic` (or by leaving
   `--include-paid` off in the CLI).
5. The SQLite cache lives in `data/estorides_cache.sqlite` —
   delete it to force fresh fetches.
6. The LLM stage needs a **generative** model. Ollama auto-selects an
   installed model if `ESTORIDES_OLLAMA_MODEL` is missing, but an
   embedding-only model (e.g. `*:e2b`) returns no text and the run falls
   back to the stub. `ollama pull llama3.1:8b` for real analysis.

### Performance knobs (bounds that keep a run from stalling)

| Env var | Default | What it caps |
|---|---|---|
| `ESTORIDES_DEADLINE` via `--deadline` | 30s | hard wall-clock cap for the whole fanout |
| `ESTORIDES_ENTITY_MAX_SCAN` | 120000 | chars scanned per response (huge crt.sh/wayback dumps) |
| `ESTORIDES_ENTITY_MAX_PER_TYPE` | 750 | entities kept per type per source |
| `ESTORIDES_KG_MAX_COOCCUR` | 30 | entities per source in the co-occurrence clique (O(n²) guard) |
| `ESTORIDES_LLM_REQUEST_TIMEOUT` | 12s | per-call LLM HTTP timeout (no orphaned threads) |

## Hard rules

- This is a passive intelligence tool. It does not probe, exploit, or
  interact with the target beyond what the public sources allow.
- All API keys stay in environment variables; they are never written
  to disk.
- Respect the rate limits of the upstream services. The circuit
  breaker will back off automatically when a host starts returning
  errors.
- Output is for legitimate OSINT, threat intelligence, journalism,
  academic research, and defensive security work.


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) [![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y2Z73AV)
