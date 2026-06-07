# Estorides — OSINT Platform

## E.S.T.E.R.O.I.D.E.S. (acronym)

- E — Entities (identification of entities, aliases, emails, IPs).
- S — Signals (capture of digital footprints and metadata).
- T — Targeted (focused on specific objectives).
- E — Extraction (automated extraction from web sources).
- R — Reconnaissance (recon and footprinting).
- O — Open-source (the nature of the OSINT engine).
- I — Intelligence (processing and correlation of data).
- D — Data (massive ingestion of unstructured records).
- E — Engine (the central engine that orchestrates queries).
- S — Scraper (automated and persistent collection).

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
                       |  - ontology engine       |   <- OFAC SDN cross-check
                       |  - MITRE ATT&CK mapper   |   <- technique auto-tagging
                       |  - SSRF guard            |   <- blocklist at egress
                       |  - audit log + RL        |   <- per-IP trail
                       |  - multi-LLM analyst     |   <- BLUF / tactical / system
                       +--------------------------+
                                 |
                                 v
                          Web UI: map / graph / timeline / results
```

## Architecture highlights (state-level)

Estorides is structured around small, single-responsibility registries
so adding a new source, backend, inferer, or feed never requires
touching the central orchestrator. The five plug-in surfaces are:

| Surface | Decorator | File | Used for |
| --- | --- | --- | --- |
| Source parsers | `@register_parser("name")` | `estorides_core/parsers.py` | Translate raw HTTP into structured dicts |
| LLM backends | `@register("name")` | `estorides_llm/manager.py` | Add an LLM provider (ollama, openai, …) |
| Relationship inferers | `@register_inferer("source")` | `estorides_core/relationship_inference.py` | Source -> graph edges |
| Real-time feeds | subclass `Feed` | `estorides_core/feeds.py` | Map layers (quakes, fires, news) |
| Encrypted exporters | `estorides_export.encryption` | `estorides_export/encryption.py` | STIX/MISP + age encryption |

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
| OFAC SDN sanctions cross-check          | none        | **ontology engine** |
| MITRE ATT&CK technique auto-tagging     | none        | **~40 techniques** |
| SSRF / private-NW egress guard          | none        | **RFC1918 + cloud IMDS blocked** |
| Audit log (per request, append-only)    | none        | **JSONL with IP+query+latency** |
| Per-IP rate limit (sliding window)      | none        | **default 30/min, env-tunable** |
| Encrypted export (age)                  | none        | **opt-in via `?key=age1…`** |
| Real-time feed layers                   | none        | **earthquakes + fires + news** |
| Encrypted export (age)                  | none        | **opt-in via `?key=age1…`** |

## What v1.1 adds on top

| Capability                              | v1.0        | v1.1 (this) |
| --------------------------------------- | ----------- | ----------- |
| Persistent graph (Cypher queries)       | NetworkX dump | **Kùzu embedded DB**, cross-run joins |
| Run persistence                         | JSONL append | **SQLite cases** with FK observations/entities |
| Cross-feed entity resolver              | none       | **Wikidata + OFAC + IP-API + NVD** via `intel_resolver` |
| Fuzzy entity clustering                 | exact dedup | **`difflib` SequenceMatcher**, 0.85 threshold, aliases surfaced |
| Extra OSINT endpoints (keyless)         | 99 YAML sources | **+7** (BGP, MAC, phone, GitHub, leaks, CISA KEV, malware C2) |
| Read-only Cypher endpoint               | none       | **`/api/intel/graph?q=...`** with write-keyword guard |
| Case history UI                         | none       | **Cases tab** + full-entity inspector |

### v1.1 architecture

```
                       +--------------------------+
   query "example.com" |  Estorides Orchestrator  |   -> STIX 2.1 / MISP / GraphML / JSON
---------------------> |  + async fanout          |
                       |  + 99 free sources       |
                       |  + 7 Osiris-style probes |
                       |  + SSRF guard + audit     |
                       |  + ontology engine       |
                       |  + MITRE ATT&CK mapper   |
                       |  + multi-LLM analyst     |
                       |  + cross-feed resolver   |   <- Wikidata SPARQL + OFAC + IP-API + NVD
                       |  + fuzzy entity cluster  |   <- difflib SequenceMatcher
                       +-----------+--------------+
                                   |
                  +----------------+-----------------+--------------------+
                  v                                  v                    v
        +------------------+              +------------------+    +------------------+
        | Kùzu graph DB    |              | SQLite case store|    | In-memory NX     |
        | (Cypher queries) |              | (FK observations)|    | (per-run working)|
        | 99 node labels   |              | search by entity |    | per-run edges    |
        | 9 REL types      |              | search by query  |    |                  |
        +------------------+              +------------------+    +------------------+
                  ^                                  ^
                  +---------/api/intel/resolve-------+
                  +---------/api/cases/...-----------+
```

### v1.1 API additions

| Endpoint                                       | Purpose |
| ---------------------------------------------- | ------- |
| `GET /api/cases?q=<substr>&type=<qtype>`       | List past runs. Searchable by query substring. |
| `GET /api/cases/<id>?full=1`                   | Replay a case. `full=1` includes observations + entities. |
| `DELETE /api/cases/<id>`                       | Drop a case. |
| `GET /api/intel/resolve?type=<t>&id=<v>`       | Cross-feed resolution. `type` is one of `ip`, `domain`, `company`, `person`, `country`, `cve`, `btc_address`, `eth_address`. |
| `GET /api/intel/graph?q=<cypher>`              | Read-only Cypher against the Kùzu graph. Mutations (`CREATE`/`MERGE`/`SET`/`DELETE`) are rejected. |
| `GET /api/intel/stats`                         | One-glance dashboard: case count, Kùzu node/edge counts, resolver cache size. |
| `GET /api/osiris/bgp?query=<ip\|ASxxxxx>`      | BGP / ASN lookup via `bgpview.io`. |
| `GET /api/osiris/mac?mac=00:1A:...`            | MAC OUI vendor via `macvendors.co`. |
| `GET /api/osiris/phone?number=+14155552671`    | Phone geolocation (NANP area code → lat/lng). |
| `GET /api/osiris/github?user=torvalds`         | GitHub user + 5 most recent repos. |
| `GET /api/osiris/leaks?email=...`              | XposedOrNot breach analytics (more detail than HIBP). |
| `GET /api/osiris/cisa-kev?limit=10&days=30`    | CISA Known Exploited Vulnerabilities, recent window. |
| `GET /api/osiris/malware?limit=200`            | Feodo Tracker + URLhaus active C2, geolocated. |

### v1.1 install

```
pip install -r requirements.txt
```

The only new required dep is `kuzu>=0.11`. The orchestrator falls
back to in-memory NetworkX if Kùzu is not importable, but a persistent
cross-run graph only happens with Kùzu present.

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

## Security & operations

| Concern | Control | Where |
| --- | --- | --- |
| Outbound to RFC1918 / loopback / cloud IMDS | SSRF guard runs on every URL before fetch (allowlist override via `ESTORIDES_ALLOWED_HOSTS`) | `estorides_core/ssrf_guard.py` |
| Web DoS / scraping | Sliding-window per-IP rate limit (default 30/min; tune via `ESTORIDES_RATE_LIMIT`) | `estorides_core/audit.py` |
| Compliance trail | Append-only JSONL audit log of every API call (timestamp, IP, query, sources, status, latency) at `data/audit.jsonl` | `estorides_core/audit.py` |
| Adversarial input | `validate_query()` rejects empty, oversize, control-char, bidi-override, and unsupported-type queries; bidi is rejected outright rather than silently stripped | `estorides_core/validation.py` |
| API key leakage | Keys read from env at call time, never logged, never written to disk | `estorides_core/orchestrator.py` (`_resolve_auth`) |
| Encrypted report delivery | `age` (https://age-encryption.org) opt-in via `?key=age1…` on the export endpoint; graceful fallback to plaintext when `age` is missing | `estorides_export/encryption.py` |
| Trusting X-Forwarded-For | Only honoured when `ESTORIDES_TRUST_PROXY=1` is set explicitly | `estorides_web.py` |

## Intelligence features

### Ontology engine — OFAC SDN cross-check

`estorides_core/ontology.py` loads the OpenSanctions OFAC SDN list
(CC-BY 4.0) once, indexes it by normalised name + alias, and stamps
every observation with `{sanctioned, hits, fields}`. The LLM analyst
stage then writes a "SANCTIONED — OFAC SDN match on …" line into the
brief so sanctions exposure is impossible to miss in the report.

Index characteristics:

- ~7 MB, low-tens-of-thousands of entries
- 24h lazy refresh
- Single-flight: concurrent first-loads share one fetch
- Best-effort disk cache at `data/ontology_sdn.json`
- Stale-on-error: keeps the previous snapshot if a refresh fails

### MITRE ATT&CK auto-tagging

`estorides_core/mitre_attack.py` maps every observation to the
ATT&CK techniques it might support, by both source-keyed table
(40+ techniques across the threat-intel, breach, and web sources)
and keyword scan (catches malware families: mimikatz, cobalt
strike, lockbit, …). Aggregated techniques are exposed at the top
of the orchestrator result as `result.mitre.techniques`.

### Real-time feeds

`estorides_core/feeds.py` ships three keyless feeds that the map
UI can layer on top of OSINT results:

| Feed | Source | Refresh | Notes |
| --- | --- | --- | --- |
| Earthquakes | USGS M2.5+ GeoJSON | 10 min | Always on |
| Fires | NASA FIRMS VIIRS_NOAA20_NRT CSV | 30 min | Requires `ESTORIDES_FIRMS_KEY` |
| News | GDELT 2.0 article list | 15 min | Coords unavailable; surfaces at (0,0) |

Endpoint: `GET /api/feeds?bbox=min_lon,min_lat,max_lon,max_lat&no_cache=1`.

### LLM prompt flavours

`estorides_llm/intelligence_prompts.py` ships three prompt styles:

- `system` — the default Palantir-grade analyst with BLUF + confidence-graded findings.
- `bluf` — single-paragraph BLUF only, for time-critical briefs.
- `tactical` — adds THREAT PICTURE + COA-1/2/3 + IMMEDIATE ACTION.

Backend priority is configurable: `ESTORIDES_BACKEND_PRIORITY=openai,ollama`
or via the `LLMManager` constructor.

## Tests

```bash
# All tests, ~10s
python3 _validate.py

# Individual suites
python3 _test_ssrf.py        # 20 SSRF cases
python3 _test_validation.py  # 16 input-validation cases
python3 _test_feeds.py       # 3 real-time feeds
python3 _test_encryption.py  # age encryption + graceful degradation
python3 _test_routes.py      # Flask route table
python3 _multi_test.sh       # end-to-end: 5 query types through the orchestrator
```

The validator exits 0 only when every check passes. CI runners can
`grep FAIL` to surface regressions.


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) [![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y2Z73AV)
