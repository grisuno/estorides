# Estorides — Cheatsheet by user goal

One section per goal. Pick the one that matches what you want to do
right now. Each section gives the shortest path through the CLI or web
UI; for the full reference, see `README.md` and the per-module
docstrings in `estorides_core/`.

## I want to enumerate a domain

```bash
# Free sources, 100+ endpoints in parallel
estorides run example.com

# Same, but also enable API-key sources
estorides run example.com --include-paid

# Only a few specific sources
estorides run example.com \
    --only-sources crt_sh_certificates,shodan_internetdb,ipapi_free,rdap
```

In the web UI: paste the domain, hit **Run**. Use the **Map** and
**Graph** tabs to walk the discovered surface.

## I want to walk the attack surface recursively

```bash
# Subdomains + sibling domains, depth 2
estorides discover example.com

# Deeper crawl, more steps
estorides discover example.com --max-depth 3 --max-steps 100

# Strictly passive (no contact with target infra)
estorides discover example.com --passive-only
```

The web UI's **Discover** button opens a live SSE feed — the surface
grows in real time. When the job is done, the case is saved
automatically and shows up in the **Cases** tab.

## I want to classify the surface against a scope file

```bash
# Save the surface, then classify
estorides discover example.com --out-json surface.json
estorides scope --assets surface.json --scope scope.txt --flat-dir in_scope/
```

`scope.txt` format:

```
## in-scope
*.example.com
203.0.113.0/24

## out-of-scope
# (anything listed here is logged but never targeted)
*.staging.example.com

## deny (hard block)
acme.internal
```

`--flat-dir` writes `in_scope_hosts.txt`, `in_scope_ips.txt`, and
`unknown.txt` — the three files your pipeline actually consumes.

## I want to find what's new since last week

```bash
# Compare two cases by entity (type,value)
estorides diff <case_old> <case_new>

# Or get the same in the web UI:
#   /api/cases/diff?a=<old>&b=<new>
#   POST /api/cases/<id>/save      → bookmark a case
```

The report shows new domains, new IPs, dropped indicators, and a
per-type breakdown. The Markdown report embeds the diff:

```bash
estorides report <case_new> --diff <case_old> --out weekly.md
```

## I want a STIX / MISP bundle for the SOC

```bash
# Plain JSON
estorides stix --out bundle.json
estorides misp --out event.json

# Encrypted with age (paste a recipient)
# in the web UI:
#   /api/export/stix?key=age1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#   /api/export/misp?key=age1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

The bundle includes every observation in the latest case, with
typed STIX objects (domain-name, ipv4-addr, email-addr, software with
CVE) and the corresponding MISP attributes.

## I want to anonymise my egress

```bash
# Quick Tor (needs aiohttp_socks — install.sh installs it on full mode)
estorides run example.com --tor

# Any SOCKS5 / HTTP proxy
estorides run example.com --proxy socks5://127.0.0.1:9050
estorides run example.com --proxy http://127.0.0.1:8080
```

Combine with `--passive-only` to keep the crawl invisible from the
target's network. The engine adds jittered retries and a per-host
circuit breaker so a flaky SOCKS hop doesn't kill the run.

## I want aircraft, satellites and launches on the map

The **Map** tab ships an **Estorides Aerospace** panel with four
keyless layers. Toggle them on; the panel fetches only the enabled
feeds, caches them on disk and refreshes every 90 seconds.

```bash
# Same data over the API (feed names are a whitelist)
curl 'http://127.0.0.1:5050/api/feeds?feeds=aircraft,satellites'
curl 'http://127.0.0.1:5050/api/feeds?feeds=military_aircraft,rocket_launches&no_cache=1'

# Query-driven counterparts (routed automatically by query type)
estorides run 25544                     # NORAD catalog id -> CelesTrak TLE
estorides run "ISS (ZARYA)"             # satellite name -> CelesTrak TLE
estorides run 400a1b                    # ICAO hex -> adsbdb aircraft
estorides run BAW123                    # callsign -> adsbdb flight route
estorides run 3f5a1b --only-sources opensky_aircraft_track
estorides run "Falcon 9" --only-sources launch_library_search
```

Satellite positions come from SGP4 when `pip install "estorides[space]"`
is present, and from a two-body fallback otherwise. All four feeds are
`contact: none` and keyless; the panel renders the required OpenSky,
adsb.lol (ODbL), CelesTrak and Launch Library 2 credits. See
`spec/aerospace.md`.

## I want to add a new source

Drop a YAML file under `sources/<NN_category>/`:

```yaml
# sources/02_ip_infra/my_new_source.yaml
name: my_new_source
category: "02. IP & Infrastructure"
url: "https://api.example.com/lookup?ip={query}"
method: GET
requires_key: MY_API_KEY
contact: passive        # passive | active — passive_only filter reads this
parser: json
parse: |
    {
      "asn": data.get("asn"),
      "asn_name": data.get("asn_name"),
      "country": data.get("country_code")
    }
ttl: 3600               # cache TTL in seconds
```

`{query}` is substituted at fetch time. The loader recurses, so you
can also group multiple sources in a single YAML with `---`
separators. Restart the server and it is registered.

## I want to enable a paid source

1. Add the key to `.env` (see `.env.example` for the full list).
2. Run with `--include-paid` (CLI) or tick the "paid" toggle in the
   web UI's run form.
3. The engine reads the key from the environment at request time,
   so no restart is needed between runs.

## I want to ask the LLM for a narrative

Every run includes an LLM analysis block. The resolver tries
backends in this order: `ollama → openrouter → anthropic → openai →
stub`. Set any of the matching API keys in `.env` and re-run. Without
any key the engine returns a templated stub — still useful, just
not generated. The full analysis is also embedded in the Markdown
report (`estorides report <case_id>`).

## I want to plug Estorides into my C2 / SIEM

The `estorides_core.discoverer` and `estorides_web` are the integration
points. Two common patterns:

  * **Pull**: poll `GET /api/cases?q=<substring>` from your SIEM, parse
    entities, and ingest them as IOCs.
  * **Push**: open `EventSource('/api/discover/stream?job_id=...')` and
    stream node_found events into your pipeline in real time.

The knowledge graph can also be exported as GraphML for Gephi /
Cytoscape: `estorides graph --export graphml`.

## I want to harden the deployment

```bash
# 1. Bind to loopback behind a reverse proxy
export ESTORIDES_HOST=127.0.0.1
export ESTORIDES_PORT=5050

# 2. Tight CORS allowlist (no wildcard)
export ESTORIDES_CORS_ORIGINS="https://app.example.com"

# 3. Enforce HTTPS (only meaningful behind TLS)
export ESTORIDES_HSTS=1
export ESTORIDES_FORCE_HTTPS=1

# 4. Run under gunicorn, never the Flask dev server
gunicorn -w 4 -b 127.0.0.1:5050 --timeout 120 wsgi:app

# 5. Sanity check — debug must be off, headers must be present
curl -sI http://127.0.0.1:5050/api/status | grep -E 'X-Frame|Content-Security'
```

The Werkzeug interactive debugger is hard-disabled inside
`create_app` regardless of the env var — `gunicorn wsgi:app` is the
only path that gets a debug-free app.
