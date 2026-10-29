# 21. Aerospace

Free, keyless air-and-space sources for Estorides. Every source here is
`contact: none`: the query target never sees traffic and no API key is
required.

| Source | Query | Upstream | Terms |
| --- | --- | --- | --- |
| `celestrak_satellite_by_catalog` | NORAD catalog id | CelesTrak GP | Citation requested |
| `celestrak_satellite_by_name` | satellite name | CelesTrak GP | Citation requested |
| `celestrak_group_catalog` | group slug (`stations`, `gps-ops`, `geo`, `starlink`) | CelesTrak GP | Citation requested |
| `adsbdb_aircraft_lookup` | ICAO 24-bit hex | adsbdb | Courtesy credit |
| `adsbdb_callsign_lookup` | flight callsign | adsbdb | Courtesy credit |
| `opensky_aircraft_track` | ICAO 24-bit hex | OpenSky Network | Research/education terms |
| `launch_library_search` | free text | Launch Library 2 | Free tier, attribution |
| `adsblol_aircraft_by_hex` | ICAO 24-bit hex | adsb.lol `/v2/hex` | ODbL 1.0 |
| `adsblol_aircraft_by_callsign` | flight callsign | adsb.lol `/v2/callsign` | ODbL 1.0 |
| `adsblol_aircraft_by_registration` | tail number | adsb.lol `/v2/reg` | ODbL 1.0 |
| `adsblol_aircraft_by_type` | ICAO type designator | adsb.lol `/v2/type` | ODbL 1.0 |
| `adsblol_emergency_squawk` | `7500`, `7600` or `7700` | adsb.lol `/v2/squawk` | ODbL 1.0 |
| `hexdb_aircraft_lookup` | ICAO 24-bit hex | hexdb.io | Community data, courtesy credit |
| `hexdb_route_lookup` | ICAO callsign | hexdb.io | Community data, courtesy credit |

The adsb.lol lookups live where the records are densest: identity
(hex, registration) and fleet (type) answer from the community network
directly, while adsbdb and hexdb stay as independent enrichment. The
polled map layers (aircraft, military aircraft, emergency squawks,
satellites, rocket launches) live in `estorides_core/feeds.py` and are
served by `GET /api/feeds?feeds=aircraft,satellites`. A bbox on that
route switches the aircraft layer to the regional adsb.lol roster. The
UI panel is branded `Estorides Aerospace`; no upstream project name is
used in the interface.

See `spec/aerospace.md` for the full design, the BDD scenarios and the
mutation-testing gate.
