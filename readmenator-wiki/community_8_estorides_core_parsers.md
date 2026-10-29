# estorides_core: parsers

*Community 8 | 13 files | cohesion 0.49*

## Definition

This community groups 13 file(s) rooted at `estorides_core` with dominant language py (cohesion 0.49). Central symbols: `AircraftEmergencyFeed`, `AircraftFeed`, `AirportIndex`, `EarthquakesFeed`, `Feed`, `FeedPoint`, `FiresFeed`, `MilitaryAircraftFeed`. Core file: `tests/test_aerospace.py` (121 symbols). Documented purpose: estorides_core.aerospace.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/aerospace.py` | py | utility | 27 | yes |
| `estorides_core/airports.py` | py | utility | 13 | yes |
| `estorides_core/aviation.py` | py | utility | 18 | yes |
| `estorides_core/feeds.py` | py | utility | 42 | yes |
| `estorides_core/parsers.py` | py | utility | 73 | yes |
| `estorides_core/socmint.py` | py | utility | 12 | yes |
| `estorides_core/source_loader.py` | py | utility | 20 | yes |
| `tests/properties/test_parsers_properties.py` | py | testing | 1 | yes |
| `tests/test_aerospace.py` | py | testing | 121 | yes |
| `tests/test_keyless_sources.py` | py | testing | 7 | yes |
| `tests/test_opsec_contact.py` | py | testing | 14 | yes |
| `tests/test_socmint.py` | py | testing | 72 | yes |
| `tests/test_source_loader.py` | py | testing | 12 | yes |

## Key Symbols

- `celestrak_group_url` (function, `estorides_core/aerospace.py:55`) `def celestrak_group_url(group)` - Return the CelesTrak TLE URL for one catalog group.
- `_finite` (function, `estorides_core/aerospace.py:61`) `def _finite(value)` - Return ``value`` as a finite float, or ``None``.
- `_text` (function, `estorides_core/aerospace.py:75`) `def _text(value)`
- `_valid_coordinates` (function, `estorides_core/aerospace.py:79`) `def _valid_coordinates(latitude, longitude)`
- `_clean` (function, `estorides_core/aerospace.py:89`) `def _clean(value, limit)` - Normalise a text field: trimmed, bounded, ``None`` when empty.
- `_as_dict` (function, `estorides_core/aerospace.py:95`) `def _as_dict(value)` - Return ``value`` when it is a dict, else an empty dict.
- `_digits` (function, `estorides_core/aerospace.py:104`) `def _digits(value)` - True only for ASCII digits (``str.isdigit`` accepts superscripts).
- `decode_catalog_field` (function, `estorides_core/aerospace.py:109`) `def decode_catalog_field(field)` - Decode a TLE catalog field, including the Alpha-5 spelling.
- `tle_catalog_number` (function, `estorides_core/aerospace.py:133`) `def tle_catalog_number(line)` - Return the NORAD catalog number from TLE line 1 or line 2.
- `_text_payload` (function, `estorides_core/aerospace.py:141`) `def _text_payload(payload)`
- `parse_tle_catalog` (function, `estorides_core/aerospace.py:149`) `def parse_tle_catalog(payload)` - Parse three-line TLE text into ``{name, norad_id, line1, line2}``.
- `tle_epoch_unix` (function, `estorides_core/aerospace.py:192`) `def tle_epoch_unix(line1)` - Return the TLE epoch as Unix seconds, or ``None``.
- `tle_mean_elements` (function, `estorides_core/aerospace.py:212`) `def tle_mean_elements(line1, line2)` - Extract the mean orbital elements needed for propagation.
- `gmst_deg` (function, `estorides_core/aerospace.py:245`) `def gmst_deg(when_unix)` - Greenwich mean sidereal time in degrees for a Unix instant.
- `eci_to_geodetic` (function, `estorides_core/aerospace.py:259`) `def eci_to_geodetic(position_km, when_unix)` - Convert an ECI/TEME position in km to latitude, longitude, altitude.
- `kepler_subsatellite_point` (function, `estorides_core/aerospace.py:285`) `def kepler_subsatellite_point(line1, line2, when_unix)` - Two-body sub-satellite point from TLE mean elements.
- `_sgp4_point` (function, `estorides_core/aerospace.py:345`) `def _sgp4_point(line1, line2, when_unix)` - SGP4 sub-satellite point when the optional package is present.
- `subsatellite_point` (function, `estorides_core/aerospace.py:379`) `def subsatellite_point(line1, line2, when_unix)` - Sub-satellite point using SGP4 when available, Kepler otherwise.
- `_emitter_category` (function, `estorides_core/aerospace.py:402`) `def _emitter_category(value)` - Map an adsb.lol ``A3``-style category to the OpenSky integer.
- `_aircraft_record` (function, `estorides_core/aerospace.py:413`) `def _aircraft_record()` - Build one common aircraft record, or ``None`` when unusable.
- `normalize_opensky_states` (function, `estorides_core/aerospace.py:488`) `def normalize_opensky_states(payload)` - Normalise an OpenSky ``/api/states/all`` response.
- `_adsblol_now` (function, `estorides_core/aerospace.py:531`) `def _adsblol_now(payload)`
- `normalize_adsblol_aircraft` (function, `estorides_core/aerospace.py:540`) `def normalize_adsblol_aircraft(payload)` - Normalise an adsb.lol v2 ``/v2/...`` aircraft response.
- `normalize_opensky_track` (function, `estorides_core/aerospace.py:604`) `def normalize_opensky_track(payload)` - Normalise an OpenSky ``/api/tracks/all`` response.
- `normalize_adsbdb` (function, `estorides_core/aerospace.py:635`) `def normalize_adsbdb(payload)` - Normalise an adsbdb aircraft or callsign flight-route response.
- `normalize_launch_library` (function, `estorides_core/aerospace.py:677`) `def normalize_launch_library(payload)` - Normalise a Launch Library 2 ``/launches/`` response.
- `cap_records` (function, `estorides_core/aerospace.py:723`) `def cap_records(records, limit)` - Return at most ``limit`` records. A non-positive limit yields [].
- `_text` (function, `estorides_core/airports.py:43`) `def _text(value, limit)`
- `_coordinate` (function, `estorides_core/airports.py:50`) `def _coordinate(value)`
- `normalise_airport` (function, `estorides_core/airports.py:60`) `def normalise_airport(row)` - Normalise one OurAirports CSV row, or ``None`` when unusable.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 31
- Cross-boundary resolved imports (EXTRACTED): 20

## Connections

- [EXTRACTED] depends_on community 8 <-> 4 (strength 0.9): Extracted import edge crosses communities: estorides_core/feeds.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 6 <-> 8 (strength 0.9): Extracted import edge crosses communities: estorides_core/orchestrator.py imports estorides_core/parsers.py.

## Risks

- [taint medium] `estorides_core/feeds.py` -> `estorides_core/feeds.py` via `requests` (0 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/aerospace.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/airports.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/aviation.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/feeds.py` via `requests` (0 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/aerospace.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/airports.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/aviation.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/feeds.py` via `requests` (0 hops)
- [layer strict] `tests/test_aerospace.py` (testing) -> `estorides_web.py` (presentation)

## Open Questions

- Is the dangerous import `requests` in `estorides_core/feeds.py` still required, or can it be isolated?
- What would break if the most connected file in estorides_core: parsers changed?
- Should estorides_core: parsers be split, given cohesion 0.49?

## Sources

- `estorides_core/aerospace.py`
- `estorides_core/airports.py`
- `estorides_core/aviation.py`
- `estorides_core/feeds.py`
- `estorides_core/parsers.py`
- `estorides_core/socmint.py`
- `estorides_core/source_loader.py`
- `tests/properties/test_parsers_properties.py`
- `tests/test_aerospace.py`
- `tests/test_keyless_sources.py`
- `tests/test_opsec_contact.py`
- `tests/test_socmint.py`
- `tests/test_source_loader.py`
