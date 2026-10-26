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

The polled map layers (aircraft, military aircraft, satellites, rocket
launches) live in `estorides_core/feeds.py` and are served by
`GET /api/feeds?feeds=aircraft,satellites`. The UI panel is branded
`Estorides Aerospace`; no upstream project name is used in the
interface.

See `spec/aerospace.md` for the full design, the BDD scenarios and the
mutation-testing gate.
