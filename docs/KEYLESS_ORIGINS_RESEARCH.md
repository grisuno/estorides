# Keyless origins: exhaustive source survey (2026-10)

Every origin in `sources/` is a YAML descriptor; adding one must not require
touching engine code. This document records the survey that produced the
`v1.5 keyless` batch: what the catalogue already covered, which keyless
endpoints were probed live, which were accepted, and which were rejected (and
why). It is the evidence trail behind the YAMLs, not a second catalogue —
`sources/*/*.yaml` stays the single source of truth.

## Method

1. Enumerate what the registry already loads (`SourceLoader.all()`, 160 YAMLs
   at the start of the survey) and de-duplicate by *capability*, not by URL.
2. Build a candidate list from the keyless/no-signup API surface used by the
   OSINT community (CT logs, DoH, RDAP, BGP, blocklists, package registries,
   AT Protocol, CVE/EPSS/OSV, sanctions lists, archives, geocoders …).
3. Probe every candidate with a plain `curl` (only a descriptive
   `User-Agent`), 20–30 s timeout, following redirects. A candidate was only
   accepted when the live probe returned `200` **and** parseable JSON/text that
   maps to the ontology.
4. Reject on: `401/403` (key or WAF), `429` without a documented free tier,
   `5xx` at probe time, binary-only bodies, or a shape already covered by an
   existing source.

Probe scripts and raw output live in `.scratchpad/` during the session; the
verdicts are summarised below.

## Accepted (new batch)

| Source | Endpoint | Category | Parser | Why it matters |
|---|---|---|---|---|
| `epss_score` | `api.first.org/data/v1/epss` | 05 Threat | `epss` | Exploit-prediction score per CVE; NVD/CIRCL do not carry it |
| `osv_vulnerability` | `api.osv.dev/v1/vulns/{id}` | 05 Threat | `osv` | Per-ecosystem affected versions and fix commits |
| `cve_org_record` | `cveawg.mitre.org/api/cve/{id}` | 05 Threat | `cve_record` | Authoritative CNA record (CVE 5.x) |
| `ransomware_live_recent` | `api.ransomware.live/v2/recentvictims` | 05 Threat | `ransomware_live` | Leak-site victim feed with sector/country |
| `yaraify_search` | `yaraify-api.abuse.ch/api/v1/` | 05 Threat | `yaraify` | YARA rule to sample correlation, keyless POST |
| `sans_isc_ip` | `isc.sans.edu/api/ip/{ip}` | 05 Threat | `sans_isc_ip` | Honeypot attack counts + threat-feed membership |
| `tor_exit_nodes` | `check.torproject.org/torbulkexitlist` | 02 IP | `text_lines` | Exit-node attribution |
| `hudsonrock_email` | `cavalier.hudsonrock.com` | 06 Breach | `hudsonrock` | Infostealer infections keyed by email |
| `disify_email` | `disify.com/api/email/{email}` | 06 Breach | `disify` | Disposable/role/validity signal |
| `gravatar_hash` | `gravatar.com/{md5}.json` | 06 Breach | `gravatar` | Hash to public profile pivot |
| `ip_guide` | `ip.guide/{ip}` | 02 IP | `ip_guide` | Clean network/asn/location object |
| `dbip_free` | `api.db-ip.com/v2/free/{ip}` | 02 IP | `dbip_ip` | Independent geo signal (no key, no quota page) |
| `geojs_ip` | `get.geojs.io/v1/ip/geo/{ip}.json` | 02 IP | `geojs_ip` | Third geo/ASN opinion |
| `ipapi_is` | `api.ipapi.is/?q={ip}` | 02 IP | `ipapi_is` | Datacenter/abuse flags, RIR data |
| `maclookup` | `api.maclookup.app/v2/macs/{mac}` | 02 IP | `maclookup` | OUI + registration block, complements macvendors |
| `peeringdb_net_search` | `peeringdb.com/api/net?name__contains=` | 02 IP | `peeringdb` | Network contacts, IX presence, policy |
| `tranco_rank` | `tranco-list.eu/api/ranks/domain/` | 02 IP | `tranco` | Popularity rank without Majestic/Cisco keys |
| `team_cymru_origin_asn` | DoH TXT `origin.asn.cymru.com` | 01 DNS | `dns_json` | ASN/prefix via DNS, zero HTTP API |
| `hstspreload_status` | `hstspreload.org/api/v2/status` | 01 DNS | `hstspreload` | HSTS preload state, error list |
| `ssl_labs_analyze` | `api.ssllabs.com/api/v3/analyze` | 03 Web | `ssl_labs` | TLS grade, protocol/cert posture |
| `gdelt_news` | `api.gdeltproject.org/api/v2/doc/doc` | 03 Web | `gdelt` | Global news index (entity to coverage) |
| `archive_org_search` | `archive.org/advancedsearch.php` | 03 Web | `archive_org` | Item metadata across the Internet Archive |
| `bluesky_profile` | `public.api.bsky.app/xrpc/...` | 04 Social | `bluesky` | AT Protocol profile, keyless |
| `lemmy_user` | `lemmy.world/api/v3/user` | 04 Social | `lemmy` | Fediverse (threads) presence |
| `gitlab_user` | `gitlab.com/api/v4/users` | 04 Social | `gitlab_user` | Code-host identity |
| `codeberg_user` | `codeberg.org/api/v1/users/` | 04 Social | `forgejo_user` | Code-host identity (Gitea/Forgejo) |
| `photon_geocode` | `photon.komoot.io/api/` | 07 Geo | `photon` | OSM geocoder, keyless and fast |
| `openlibrary_search` | `openlibrary.org/search.json` | 08 Knowledge | `openlibrary` | Books/authors, person pivots |
| `pubmed_search` | `eutils.ncbi.nlm.nih.gov` | 08 Knowledge | `pubmed` | Biomedical literature |
| `europepmc_search` | `ebi.ac.uk/europepmc/...` | 08 Knowledge | `europepmc` | Full-text life-science corpus |
| `doaj_search` | `doaj.org/api/search/articles` | 08 Knowledge | `doaj` | Open-access journals |
| `radio_browser_search` | `de1.api.radio-browser.info` | 09 Wireless | `radio_browser` | Station registry / transmitter context |
| `ofac_sanctions_eth` | GitHub `0xB10C/ofac-...` | 10 Blockchain | `address_list` | OFAC SDN ETH addresses, keyless mirror |
| `npm_package` | `registry.npmjs.org/{pkg}/latest` | 18 Supply | `npm_package` | Package metadata, maintainers, repo |
| `pypi_package` | `pypi.org/pypi/{pkg}/json` | 18 Supply | `pypi_package` | Package metadata, author, URLs |
| `dockerhub_search` | `hub.docker.com/v2/search/repositories` | 18 Supply | `dockerhub_search` | Image popularity/official flag |
| `huggingface_models` | `huggingface.co/api/models` | 18 Supply | `huggingface` | Model/dataset supply chain |
| `adsbfi_aircraft_by_hex` | `opendata.adsb.fi/api/v2/hex/` | 21 Aerospace | `adsblol_aircraft` | Second live ADS-B network (failover) |
| `planespotters_photos` | `api.planespotters.net/pub/photos` | 21 Aerospace | `planespotters` | Tail-number photo + photographer |
| `satnogs_satellite` | `db.satnogs.org/api/satellites/` | 21 Aerospace | `satnogs` | Satellite catalogue by NORAD id |
| `spaceflightnews_search` | `api.spaceflightnewsapi.net/v4` | 21 Aerospace | `spaceflightnews` | Launch/space news search |

Reused parsers are deliberate: `dns_json` already understands DoH answers,
`text_lines` already understands plaintext feeds, and `adsblol_aircraft`
already normalises the `{"ac": [...]}` envelope that adsb.fi shares with
adsb.lol.

## Rejected at probe time

| Candidate | Probe | Reason |
|---|---|---|
| Quad9 DoH (`dns.quad9.net`) | 400 / empty on `:5053` | Only serves `application/dns-message` here; `dns_json` cannot read it |
| Common Crawl index | 502 / 504 (twice) | At capacity during the survey; not reliable enough for a source |
| airplanes.live | 403 | Requires an allow-listed contact email from the operator |
| Anubis (`jldc.me`) | 403 | Cloudflare challenge |
| RapidDNS | 200 HTML | No JSON; would need a site-specific HTML parser |
| `threatminer`, `phishstats`, `spacexdata` | 522 / 502 | Origin down |
| `peeringdb` (default UA) | 403 | WAF rejects non-descriptive UA; fixed by UA, accepted above |
| `crates.io`, `coingecko`, `planespotters` (default UA) | 403 | Same: descriptive UA required |
| `api.datacite.org`, `api.gleif.org`, `overpass-api.de` | empty / 502 | Blocked or at capacity from the probe network |
| `opensanctions`, `api.sec.gov`, `api.stackexchange` | 401 / 403 | Key or WAF |
| `blockchair`, `binance` | 430 / 451 | IP blacklist / regional block |
| `ssl_labs` for `example.com` | `Hostname blacklisted` | Endpoint fine; use a real host |
| `packetstorm`, `iabot` | HTML | Feed returns a web page, not the machine format |
| `api.semanticscholar.org`, `grep.app` | 429 | Free tier exhausted at probe time |
| `nuget.org` | 200 gzip | Binary-ish payload; low marginal value over npm/PyPI |
| `restcountries.com` | 200 `success:false` | v3.1 deprecated at probe time |
| `cloudflare-eth.com`, `eth.llamarpc.com` | error / 525 | Public RPC endpoints retired |

## Deliberate non-additions

* `commoncrawl`: see above; revisit when the index is stable.
* Extra geocoders: `nominatim` and `photon` are enough; more would duplicate
  the same OSM data.
* Feeds whose only payload is "the entire internet" (FireHOL level1,
  blocklist.de, Spamhaus DROP, Cloudflare/GCP IP ranges) stay represented by
  `blocklist_de_all` plus `tor_exit_nodes`; adding more multiplies fan-out cost
  and floods the graph with thousands of unrelated IP entities without new
  signal for the queried target.
* `wikimedia_search`: `wikipedia_search` already covers the MediaWiki search
  API; a second entry would be a duplicate capability.

## Maintenance

* Probes are cheap: re-run the `.scratchpad` scripts quarterly and flip
  `enabled: false` on anything that stops answering (never delete history).
* Keep `contact: none` only where the third party is queried about a *public
  record* it already serves (CT logs, RDAP, registries, blocklists). Anything
  that forwards the target to a vendor for scanning (`ssl_labs`,
  `hudsonrock`) stays `contact: broker`.
* Re-check the free-tier terms before raising fan-out: `ipapi.is`, `db-ip` and
  `maclookup` publish soft quotas even without keys.
