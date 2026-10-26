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
| adsb.lol | `https://api.adsb.lol/v2/mil` | Military aircraft snapshot | ODbL 1.0, attribution |
| adsbdb | `https://api.adsbdb.com/v0/aircraft/{hex}`, `/v0/callsign/{callsign}` | Registration, type, operator, route | No published licence, courtesy credit |
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
category, observed_at, source
```

Every normaliser is total: `None`, strings, integers, empty objects,
lists and truncated rows all return an empty container or an empty
value, never raise. Coordinates outside WGS84 bounds are dropped.

## Feeds

| Feed name | Class | TTL | Upstream | Cap env |
| --- | --- | --- | --- | --- |
| `aircraft` | `AircraftFeed` | 5 min | OpenSky global snapshot | `ESTORIDES_AIRCRAFT_MAX` (default 3000) |
| `military_aircraft` | `MilitaryAircraftFeed` | 2 min | adsb.lol `/v2/mil` | `ESTORIDES_AIRCRAFT_MAX` |
| `satellites` | `SatellitesFeed` | 10 min | CelesTrak groups | `ESTORIDES_SATELLITES_MAX` (default 1200) |
| `rocket_launches` | `RocketLaunchesFeed` | 60 min | Launch Library 2 | `ESTORIDES_LAUNCHES_MAX` (default 100) |

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

All are `contact: none`, `requires_key: false`, `os: any`, and route on
`keyword` plus `username` (ICAO hex and callsigns are detected as
handles or free text).

## Map panel

`templates/index.html` gains an `estorides-aero-panel` overlay inside
the map canvas. `static/js/estorides.js` gains an aerospace layer
manager that:

- renders one Leaflet layer per feed with its own colour,
- fetches `/api/feeds?feeds=<enabled>` only for enabled layers,
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

## Security guarantees

- No secrets: every upstream is keyless. No new environment variable
  holds a credential.
- SSRF: feed URLs are module constants, checked with `assert_safe`
  before the request. No user input reaches a feed URL.
- XSS: every popup value goes through the existing `escapeHTML` /
  `escapeAttr` helpers; no new `innerHTML` sink with raw upstream text.
- Bounded output: server caps per feed and the route accepts only a
  whitelisted feed-name list, so a caller cannot amplify upstream
  traffic.

## Out of scope

- SGP4 reimplementation (optional dependency, fallback documented).
- AIS vessels (needs an AISStream key; not keyless).

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

## Mutation testing

`[tool.mutmut]` includes `estorides_core/aerospace.py`, copies the
runtime data the tests read (`sources/`, `templates/`, `static/`) and
selects the aerospace unit and property suites. Command:

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
