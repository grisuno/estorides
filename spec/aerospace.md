# aerospace — free satellite, aircraft and launch intelligence

## Purpose

Add the free air-and-space layer set that the `gods-eye-view` project
proved useful, re-implemented from scratch for Estorides and branded as
Estorides / Lazy Own Red Team. No source names, class names, CSS
classes or UI strings are copied from the upstream project.

The layer set answers three operator questions that the existing
catalog could not:

1. What is flying right now over a region (civil and military aircraft)?
2. What is in orbit right now (satellites, stations, navigation
   constellations)?
3. What is scheduled to launch, from where, and with which vehicle?

Two delivery surfaces, one shared normaliser module:

| Surface | File | Used by |
| --- | --- | --- |
| Query-driven sources | `sources/21_aerospace/*.yaml` + `estorides_core/parsers.py` | `estorides run <hex|name|slug>` |
| Polled map layers | `estorides_core/feeds.py` + `GET /api/feeds` | Map tab layer panel |

## Free upstream APIs (all keyless)

| Upstream | Endpoint | Used for | Terms |
| --- | --- | --- | --- |
| OpenSky Network | `https://opensky-network.org/api/states/all?extended=1` | Worldwide civil aircraft snapshot (anonymous tier) | Non-commercial research / education, attribution |
| adsb.lol | `https://api.adsb.lol/v2/mil`, `/v2/point/{lat}/{lon}/{radius}`, `/v2/hex|reg|callsign|type|squawk/{key}` | Military snapshot, regional roster, single-airframe state, emergency squawk poll | ODbL 1.0, attribution |
| adsbdb | `https://api.adsbdb.com/v0/aircraft/{hex}`, `/v0/callsign/{callsign}` | Registration, type, operator, route | No published licence, courtesy credit |
| hexdb.io | `https://hexdb.io/api/v1/aircraft/{hex}`, `/api/v1/route/icao/{callsign}` | Registration, ICAO type, registered owner, route (redundant with adsbdb) | Community data, courtesy credit |
| OurAirports | `https://davidmegginson.github.io/ourairports-data/airports.csv` | Aerodrome reference set for the nearest-airport annotation | Public domain |
| CelesTrak | `https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=tle` and `?CATNR={id}` / `?NAME={name}` | TLE catalog for orbit propagation | US government origin, citation requested |
| Launch Library 2 | `https://ll.thespacedevs.com/2.3.0/launches/` | Upcoming and recent launches with pad coordinates | Free tier, attribution |

No API key is required. All feeds are `contact: none` (the target
never sees traffic); upstream availability is the only dependency.

## Module: `estorides_core/aerospace.py`

Pure functions only, no network and no filesystem, so mutation testing
is meaningful and deterministic.

- `decode_catalog_field(field)` -> `int | None`: NORAD catalog number,
  including Alpha-5 spelling (`A0000` .. `Z9999`, skipping I and O).
- `tle_catalog_number(line)` -> `int | None`: catalog number from TLE
  line 1 or line 2 columns 3-7.
- `parse_tle_catalog(payload)` -> `list[dict]`: three-line TLE text
  (or `{"raw_text": ...}`) into `{name, norad_id, line1, line2}`.
  Malformed sets are skipped, valid neighbours survive, duplicates by
  NORAD id keep the first entry.
- `tle_epoch_unix(line1)` -> `float | None`: TLE epoch as Unix seconds.
- `tle_mean_elements(line1, line2)` -> `dict | None`: inclination,
  RAAN, eccentricity, argument of perigee, mean anomaly, mean motion.
- `eci_to_geodetic(position_km, when_unix)` -> `dict | None`: TEME/ECI
  position to `{latitude, longitude, altitude_km}` with GMST rotation.
- `kepler_subsatellite_point(line1, line2, when_unix)` -> `dict | None`:
  two-body fallback, accurate enough for map display.
- `subsatellite_point(line1, line2, when_unix)` -> `dict | None`: SGP4
  when the optional `sgp4` package is installed, Kepler fallback
  otherwise. Never raises.
- `normalize_opensky_states(payload)` -> `list[dict]`: OpenSky state
  vectors into the common aircraft record.
- `normalize_adsblol_aircraft(payload)` -> `list[dict]`: adsb.lol v2
  records into the same common aircraft record (knots/feet converted).
- `normalize_opensky_track(payload)` -> `dict`: one aircraft track.
- `normalize_adsbdb(payload)` -> `dict`: aircraft or callsign route.
- `normalize_launch_library(payload)` -> `list[dict]`: launches with
  pad coordinates.
- `cap_records(records, limit)` -> `list[dict]`: deterministic payload
  bound; `limit <= 0` returns `[]`.

Common aircraft record:

```
icao24, callsign, origin_country, latitude, longitude,
baro_altitude_m, geo_altitude_m, on_ground, velocity_mps,
heading_deg, vertical_rate_mps, squawk, spi, position_source,
category, type_code, registration, description, owner,
aircraft_class, emergency, db_flags, observed_at, source
```

`aircraft_class` is the display class from
:mod:`estorides_core.aviation`, `emergency` is the transponder state
(or `None`) and `db_flags` the decoded readsb bitfield (or `None`).
OpenSky never supplies a type designator, so its records lean on the
emitter category; adsb.lol supplies `t`, `r`, `ownOp` and `dbFlags`.

Every normaliser is total: `None`, strings, integers, empty objects,
lists and truncated rows all return an empty container or an empty
value, never raise. Coordinates outside WGS84 bounds are dropped.

## Module: `estorides_core/aviation.py`

Pure aircraft-intelligence helpers. No network, no filesystem.

- `classify_aircraft(type_code, category=None)` -> class slug
  (`light`, `glider`, `balloon`, `turboprop`, `airliner`, `widebody`,
  `quadjet`, `helicopter`, `fastjet`, `bizjet`, `uav`, `ground`,
  `space`, `unknown`). ICAO type designators are matched by exact set
  and by family prefix, helicopter/UAV/fast-jet first so a prefix can
  never steal a designator from a narrower table. An uncurated
  designator falls back to the ADS-B emitter category (`A3`, OpenSky
  integer) and then to `unknown` — never to a guessed `airliner`.
- `aircraft_class_label(slug)` -> human label.
- `normalize_squawk(value)` -> four octal digits or `None`.
- `emergency_status(squawk, emergency=None)` -> `{kind, label,
  severity, squawk, source}` or `None`. 7500 unlawful interference,
  7600 radio failure, 7700 general emergency; the ADS-B emergency field
  is a superset (`general`, `lifeguard`, `minfuel`, `nordo`,
  `unlawful`, `downed`). The most severe signal wins, the ADS-B field
  wins a tie, and `source` records which one named the status.
- `is_emergency(status)`, `emergency_phrase(status)`: the phrase quotes
  the squawk only when the squawk is the evidence
  (`broadcasting squawk 7700 (general emergency)` versus
  `ADS-B reports general emergency`).
- `decode_db_flags(value)` -> `{military, interesting, pia, ladd, raw}`
  from the readsb bitfield, or `None`.
- `haversine_km(...)`, `bbox_center_radius(bbox)`, `point_in_bbox(...)`.
- `normalize_hexdb_aircraft(payload)`, `normalize_hexdb_route(payload)`.

A squawk is what one poll broadcast. The module reports it and never
concludes that an incident happened or was resolved.

## Module: `estorides_core/airports.py`

Public-domain aerodrome reference data (OurAirports CSV) with a
one-degree grid index, so "which airport is this contact near?" costs a
handful of cells instead of a full scan.

- `parse_airports_csv(text, types=..., limit=0)` -> normalised airports
  (`large_airport`, `medium_airport`, `small_airport`; heliports, closed
  fields and seaplane bases are dropped). Bad coordinates and duplicate
  identifiers are dropped.
- `AirportIndex.nearest(lat, lon, max_km=50)` -> closest airport with
  `distance_km`, or `None`.
- `AirportIndex.by_code(code)` -> ICAO, IATA, GPS or local identifier.
- `AirportIndex.within_bbox(bbox)`, `airport_brief(airport)`.

The download and the on-disk cache live in `feeds.py`;
`ESTORIDES_AIRPORTS_ENRICH=1` opts in (a one-time ~13 MB fetch, monthly
refresh), `ESTORIDES_AIRPORTS_RADIUS_KM` (default 25) bounds the search.

## Feeds

| Feed name | Class | TTL | Upstream | Cap env |
| --- | --- | --- | --- | --- |
| `aircraft` | `AircraftFeed` | 5 min (60 s regional) | OpenSky global snapshot, adsb.lol `/v2/point` for a bbox | `ESTORIDES_AIRCRAFT_MAX` (default 3000) |
| `military_aircraft` | `MilitaryAircraftFeed` | 2 min | adsb.lol `/v2/mil` | `ESTORIDES_AIRCRAFT_MAX` |
| `aircraft_emergency` | `AircraftEmergencyFeed` | 60 s | adsb.lol `/v2/squawk/{7500,7600,7700}` | `ESTORIDES_EMERGENCY_MAX` (default 200) |
| `satellites` | `SatellitesFeed` | 10 min | CelesTrak groups | `ESTORIDES_SATELLITES_MAX` (default 1200) |
| `rocket_launches` | `RocketLaunchesFeed` | 60 min | Launch Library 2 | `ESTORIDES_LAUNCHES_MAX` (default 100) |

### Regional aircraft fetch

`GET /api/feeds?...&bbox=min_lon,min_lat,max_lon,max_lat` asks for a
region, not the world. `AircraftFeed` answers it from adsb.lol
`/v2/point/{lat}/{lon}/{radius}` (centre plus half-diagonal, capped at
the upstream's own 250 nm limit) when the box fits, and falls back to
the worldwide OpenSky snapshot when it does not. A regional answer is
cached under its own key (`aircraft-<bbox>.json`, quantised to 0.01°)
and refreshed every 60 s, so a narrow and a wide request never poison
each other. `ESTORIDES_AIRCRAFT_REGIONAL=0` forces the worldwide path.

`Feed.fetch(bbox=...)` is the generic hook: a feed that cannot answer a
box returns `None` from `_fetch_bbox()` and is fetched globally, then
clipped by `fetch_all()`. Only feeds that override `_fetch_bbox()` key
their cache by box (the rest would refetch the same world once per
viewport), and the newest 50 regional files are kept so a long session
cannot grow the cache without bound. The Map tab sends the current
viewport as `bbox` when it spans at most 20° per axis.

### Emergency layer

`aircraft_emergency` polls the three ICAO Mode A codes and merges the
results, deduplicating by ICAO address. Each point carries
`emergency` (kind, label, severity, source) and `emergency_phrase` in
`extra`, so the popup can quote the broadcast without turning it into
an incident report. One code failing upstream never empties the layer.

Satellite groups default to `stations,visual,gps-ops,glo-ops,galileo,geo`
and can be overridden with `ESTORIDES_SATELLITES_GROUPS`. The feed
deduplicates by NORAD id, propagates each TLE to the current instant
and emits a `FeedPoint(kind="satellite")` at the sub-satellite point
with `altitude_km` and `velocity_kms` in `extra`.

Each feed declares `attribution`; `list_feeds()` returns it so the UI
can render the required credits, and `GET /api/feeds` returns the same
list.

`fetch_all()` gains a keyword-only `names` filter. Unknown names are
ignored by the orchestrator-facing helper; the HTTP route validates
them and answers `400` with the valid names.

## Sources (`sources/21_aerospace/`)

| Source | Query | Endpoint |
| --- | --- | --- |
| `celestrak_satellite_by_catalog` | NORAD id | `gp.php?CATNR=` |
| `celestrak_satellite_by_name` | satellite name | `gp.php?NAME=` |
| `celestrak_group_catalog` | group slug | `gp.php?GROUP=` |
| `adsbdb_aircraft_lookup` | ICAO hex | `v0/aircraft/` |
| `adsbdb_callsign_lookup` | callsign | `v0/callsign/` |
| `opensky_aircraft_track` | ICAO hex | `api/tracks/all?icao24=` |
| `launch_library_search` | free text | `2.3.0/launches/?search=` |
| `adsblol_aircraft_by_hex` | ICAO hex | `v2/hex/` |
| `adsblol_aircraft_by_callsign` | callsign | `v2/callsign/` |
| `adsblol_aircraft_by_registration` | registration | `v2/reg/` |
| `adsblol_aircraft_by_type` | ICAO type designator | `v2/type/` |
| `adsblol_emergency_squawk` | `7500` / `7600` / `7700` | `v2/squawk/` |
| `hexdb_aircraft_lookup` | ICAO hex | `api/v1/aircraft/` |
| `hexdb_route_lookup` | ICAO callsign | `api/v1/route/icao/` |

All are `contact: none`, `requires_key: false`, `os: any`, and route on
`keyword` plus `username` (ICAO hex and callsigns are detected as
handles or free text).

## Map panel

`templates/index.html` gains an `estorides-aero-panel` overlay inside
the map canvas. `static/js/estorides.js` gains an aerospace layer
manager that:

- renders one Leaflet layer per feed with its own colour,
- fetches `/api/feeds?feeds=<enabled>` only for enabled layers, sending
  the current viewport as `bbox` when it spans at most 20° per axis,
- popup rows for identity (class, ICAO type, registration, owner), the
  transponder state and the nearest aerodrome,
- marks the emergency layer in red and shows the quotable phrase,
- persists toggles in `localStorage` under `estorides.aero.enabled`,
- refreshes on demand and every 90 s while the map tab is visible,
- shows the attribution line and the last successful refresh time,
- degrades quietly: an unavailable feed shows "unavailable" and never
  breaks the existing OSINT markers.

Panel title and every new class use the `estorides` / `lazy` branding
only (`estorides-aero-*`).

## Error table

| Condition | Behaviour |
| --- | --- |
| Upstream times out or returns 5xx | `Feed.fetch` serves the stale cache (up to 6 h), else `[]`; status shows unavailable |
| Malformed row inside a valid payload | Row dropped, other rows kept |
| TLE set truncated mid-way | The incomplete set is skipped, previous sets kept |
| `sgp4` not installed | Kepler fallback still returns a sub-satellite point |
| Satellite name not found upstream | Parser returns `{"satellites": [], "count": 0}` |
| Client requests an unknown feed name | `400 {"error": "unknown feed", "valid": [...]}` |
| Satellite propagation error | That satellite is skipped |
| One emergency squawk code fails upstream | The other codes are still returned; the layer logs and continues |
| bbox wider than the regional limit | `_fetch_bbox` returns `None`, the worldwide snapshot is fetched and clipped |
| Airport catalogue download fails | `_annotate_airports` keeps the stale index (or none); aircraft points are unchanged |

## Security guarantees

- No secrets: every upstream is keyless. No new environment variable
  holds a credential.
- SSRF: feed URLs are module constants, checked with `assert_safe`
  before the request. No user input reaches a feed URL. The one
  overridable URL (`ESTORIDES_AIRPORTS_URL`) is `assert_safe`-checked
  and the download is capped at 64 MiB.
- XSS: every popup value goes through the existing `escapeHTML` /
  `escapeAttr` helpers; no new `innerHTML` sink with raw upstream text.
- Bounded output: server caps per feed and the route accepts only a
  whitelisted feed-name list, so a caller cannot amplify upstream
  traffic. Regional caches are capped at 50 files per feed.

## Out of scope (candidates for a follow-up)

- OpenSky flight history (`/api/flights/aircraft`, arrivals,
  departures) — keyless, but needs relative time-window parameters,
  which the source YAML model does not template yet.
- FIRMS fire detections — free, but `MAP_KEY`-gated; the existing feed
  already reads it from `ESTORIDES_FIRMS_KEY`.
- OSM Overpass military installations — keyless, but the query is a
  bbox-scoped Overpass QL body, not a single `{query}` string.
- AIS vessels (needs an AISStream key; not keyless).
- Public CCTV catalogs and internet-radio stations — keyless, but they
  need their own map layers rather than aircraft records.
- SGP4 reimplementation (optional dependency, fallback documented).

## BDD Given-When-Then

### A1 — TLE parsing tolerates malformed sets
Given a catalog text with a truncated set between two valid sets
When `parse_tle_catalog` runs
Then the two valid sets are returned and the truncated one is not.

### A2 — Alpha-5 catalog numbers
Given TLE lines with catalog field `A0000`
When `tle_catalog_number` runs
Then it returns `100000`, and `I`/`O` are rejected.

### A3 — Sub-satellite point is physical
Given the ISS TLE
When `subsatellite_point` runs one minute after epoch
Then latitude is within ±90, longitude within ±180 and altitude is
between 300 and 500 km.

### A4 — SGP4 and Kepler agree near epoch
Given the ISS TLE and `sgp4` installed
When both propagators run 60 s after epoch
Then their sub-satellite points are within 1 degree.

### A5 — OpenSky normalisation drops invalid rows
Given a payload with one valid vector and rows with missing or
out-of-range positions
When `normalize_opensky_states` runs
Then only the valid vector is returned, with SI units and deduplicated
ICAO addresses.

### A6 — adsb.lol normalisation converts units
Given an adsb.lol aircraft with feet, knots and ft/min
When `normalize_adsblol_aircraft` runs
Then altitude, speed and vertical rate are metres, m/s and m/s, and
`alt_baro: "ground"` yields `on_ground=True` with no barometric
altitude.

### A7 — adsbdb handles both shapes
Given an aircraft payload and a flight-route payload
When `normalize_adsbdb` runs
Then both return a non-empty dict with `kind` set to `aircraft` and
`flightroute` respectively.

### A8 — Launch Library keeps pad coordinates
Given an LL2 payload with a pad that has latitude and longitude
When `normalize_launch_library` runs
Then the launch carries numeric coordinates, status, provider and
rocket.

### A9 — Every normaliser is total
Given `None`, a string, an integer, an empty list, an empty dict and a
truncated row
When any aerospace normaliser runs
Then it never raises and returns an empty container or empty value.

### A10 — Aircraft feed emits map points
Given a mocked OpenSky response with two aircraft
When `AircraftFeed._fetch` runs
Then two `FeedPoint(kind="aircraft")` are returned with valid
coordinates and callsign labels.

### A11 — Satellite feed deduplicates and propagates
Given two CelesTrak groups containing the same satellite and one
invalid TLE
When `SatellitesFeed._fetch` runs
Then one point is returned for that NORAD id and no exception escapes.

### A12 — Launch feed plots pad coordinates
Given a mocked LL2 response with one launch but no pad coordinates and
one with coordinates
When `RocketLaunchesFeed._fetch` runs
Then only the located launch becomes a point.

### A13 — Feed selection is validated
Given `GET /api/feeds?feeds=aircraft,nope`
When the route runs
Then it answers 400 and lists the valid feed names.

### A14 — Map panel uses Estorides branding only
Given `templates/index.html` and `static/js/estorides.js`
When the aerospace panel and layer manager are inspected
Then the strings `gods-eye-view`, `God's Eye View` and `godseye` do not
appear, and the panel id starts with `estorides-aero`.

### A15 — A bbox is answered by the regional endpoint
Given a mocked adsb.lol `/v2/point` response with one aircraft
When `AircraftFeed._fetch_bbox` runs for a box around Madrid
Then one point is returned from `adsb.lol`, the URL carries the box
centre and a radius no larger than 250 nm, and the point's `extra`
carries `aircraft_class`, `type_code` and `registration`.
And a box wider than the regional limit returns `None` without a
network call, so `fetch` falls back to the worldwide snapshot.
And a regional answer is cached under a bbox-specific file name.

### A16 — The emergency feed merges the three codes
Given mocked `/v2/squawk/7500`, `/7600` and `/7700` responses, one
aircraft appearing under two codes and one code answering 404
When `AircraftEmergencyFeed._fetch` runs
Then the aircraft appears once, every point is
`kind="aircraft_emergency"`, the 7700 contact carries
`emergency.kind="general"` and the phrase
`broadcasting squawk 7700 (general emergency)`, and no exception
escapes.

### A17 — Nearest-airport annotation is opt-in
Given `ESTORIDES_AIRPORTS_ENRICH` unset
When `_annotate_airports` runs on one aircraft point
Then no `nearest_airport` key is added and no download happens.
Given the flag set and a catalogue containing Madrid-Barajas
When the same point is annotated with `ESTORIDES_AIRPORTS_RADIUS_KM=25`
Then `nearest_airport.ident == "LEMD"` with a distance in kilometres.
And with `ESTORIDES_AIRPORTS_RADIUS_KM=1` the key is absent.

### A18 — Classification never guesses
Given an ICAO designator nobody curated and no category
When `classify_aircraft` runs
Then the answer is `unknown`, never `airliner`.
Given `"C172"`, `"B77W"`, `"A388"`, `"EC135"`, `"MQ9"` and `"F16C"`
Then the classes are light, widebody, quadjet, helicopter, uav and
fastjet respectively.

### A19 — Emergency status is a broadcast, not a finding
Given squawk `7700` and the ADS-B field `minfuel`
When `emergency_status` runs
Then the general emergency wins and `source` is `squawk`.
Given squawk `7700` and ADS-B `downed`
Then the ADS-B status wins the tie and `source` is `ads-b`.
Given squawk `1200` and ADS-B `none`
Then the status is `None`.

## Mutation testing

`[tool.mutmut]` includes `estorides_core/aerospace.py`,
`estorides_core/aviation.py` and `estorides_core/airports.py`, copies
the runtime data the tests read (`sources/`, `templates/`, `static/`)
and selects the aerospace, aviation and airport suites. Command:

```bash
mutmut run --max-children 3
mutmut results
```

Measured on this branch: **1162 killed / 1407 mutants = 82.6 % mutation
score**, 0 timeouts. The remaining survivors are concentrated in
optional-field `or` fallbacks and numeric tolerances (equivalent
mutants); a surviving mutant that changes observable behaviour means a
test does not actually pin the behaviour, and the fix is a stronger
test, never an exclusion.


- 3D globe/Cesium rendering (the Estorides map is Leaflet 2D).
- Live ADS-B receivers on the LAN (separate LAN consent surface).
