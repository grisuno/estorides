"""
estorides_core.osiris_sources
=============================
Extra OSINT endpoints borrowed from the Osiris project
(simplifaisoul/osiris). Each function returns a Flask Response-ready
dict; the Blueprint in `estorides_web` wires them up to public routes.

Why a separate module:
  The main 99 sources are YAML-defined and go through the orchestrator
  pipeline (parser → entity extraction → KG). The Osiris-style
  endpoints are narrower: they hit a single free API and return a
  flat JSON response without going through the orchestrator. Mixing
  them into the YAML registry would force a parallel "raw passthrough"
  parser and bloat `parsers.py`. Keeping them here makes the boundary
  explicit and easy to audit.

Source map (Osiris → here):
  /api/osiris/bgp        bgpview.io (keyless)
  /api/osiris/mac        macvendors.co (keyless)
  /api/osiris/phone      local libphonenumber + region centroid table
  /api/osiris/github     api.github.com (keyless, rate-limited)
  /api/osiris/leaks      api.xposedornot.com (keyless, more detail than HIBP)
  /api/osiris/cisa-kev   cisa.gov KEV JSON feed
  /api/osiris/malware    feodotracker.abuse.ch + urlhaus-api.abuse.ch
"""
from __future__ import annotations

import csv
import io
import json
import logging
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

from .config import DATA_DIR
from .ssrf_guard import assert_safe

log = logging.getLogger("estorides.osiris")

# Local country centroid table — borrowed from Osiris' malware route.
# Used to jitter malware C2 markers around a country centroid so they
# don't all stack on the same pixel.
COUNTRY_CENTROIDS: Dict[str, Tuple[float, float]] = {
    "AF": (65, 33), "AL": (20, 41), "DZ": (3, 28), "AO": (18.5, -12.5),
    "AR": (-64, -34), "AM": (45, 40), "AU": (134, -25), "AT": (14, 47.5),
    "AZ": (50, 40.5), "BD": (90, 24), "BY": (28, 53), "BE": (4, 50.8),
    "BR": (-51, -10), "BG": (25.5, 42.7), "CA": (-96, 62), "CL": (-71, -30),
    "CN": (105, 35), "CO": (-72, 4), "HR": (16, 45.2), "CZ": (15.5, 49.8),
    "DK": (10, 56), "EG": (30, 27), "FI": (26, 64), "FR": (2, 46),
    "DE": (10, 51), "GR": (22, 39), "HK": (114.2, 22.3), "HU": (19.5, 47),
    "IN": (79, 22), "ID": (120, -5), "IR": (53, 32), "IQ": (44, 33),
    "IE": (-8, 53), "IL": (34.8, 31.5), "IT": (12.5, 42.8), "JP": (138, 36),
    "KZ": (67, 48), "KE": (38, 1), "KR": (128, 36), "LT": (28, 55.5),
    "MY": (112, 3), "MX": (-102, 23.5), "NL": (5.5, 52.5), "NZ": (174, -41),
    "NG": (8, 10), "NO": (8, 62), "PK": (70, 30), "PA": (-80, 9),
    "PH": (122, 12.5), "PL": (19.5, 52), "PT": (-8, 39.5), "RO": (25, 46),
    "RU": (100, 60), "SA": (45, 25), "SG": (103.8, 1.35), "ZA": (24, -29),
    "ES": (-4, 40), "SE": (16, 62), "CH": (8, 47), "TW": (121, 23.7),
    "TH": (103, 15), "TR": (35, 39), "UA": (32, 49), "AE": (54, 24),
    "GB": (-2, 54), "US": (-97, 38), "VN": (106, 16),
}

_UA = "Estorides/1.1 (+open-source OSINT platform; osiris_sources)"

# Cache directory for downloaded feeds (CISA KEV, malware lists).
CACHE_DIR: Path = Path(
    __import__("os").environ.get(
        "ESTORIDES_OSIRIS_CACHE", str(DATA_DIR / "osiris_cache")
    )
)
CACHE_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _cached_get(url: str, *, cache_name: str, ttl: int = 3600,
                params: Optional[Dict[str, Any]] = None) -> Optional[Any]:
    """GET with a small on-disk JSON cache. Returns parsed JSON or None.

    Used for the slow-changing feeds (CISA KEV, malware lists) so a
    burst of operator clicks doesn't hammer the upstream."""
    cache_path = CACHE_DIR / f"{cache_name}.json"
    if cache_path.exists() and (time.time() - cache_path.stat().st_mtime) < ttl:
        try:
            return json.loads(cache_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
    try:
        assert_safe(url)
    except Exception as e:  # noqa: BLE001
        log.debug("ssrf blocked %s: %s", url, e)
        return None
    try:
        r = requests.get(url, params=params, headers={"User-Agent": _UA}, timeout=10)
        if not r.ok:
            return None
        data = r.json() if "json" in r.headers.get("content-type", "") else r.text
        try:
            cache_path.write_text(
                json.dumps(data, ensure_ascii=False, default=str),
                encoding="utf-8",
            )
        except OSError:
            pass
        return data
    except Exception as e:  # noqa: BLE001
        log.debug("cached_get failed for %s: %s", url, e)
        return None


# ---------------------------------------------------------------------------
# BGP / ASN
# ---------------------------------------------------------------------------
def fetch_bgp(query: str) -> Dict[str, Any]:
    """Look up an IP or AS number against bgpview.io (free, no key)."""
    query = (query or "").strip()
    if not query:
        return {"error": "missing query"}

    is_ip = bool(re.match(r"^(\d{1,3}\.){3}\d{1,3}$", query))
    is_asn = bool(re.match(r"^(AS)?\d+$", query, re.IGNORECASE))

    out: Dict[str, Any] = {"query": query, "timestamp": time.time()}
    try:
        if is_ip:
            url = f"https://api.bgpview.io/ip/{query}"
            assert_safe(url)
            r = requests.get(url, headers={"User-Agent": _UA}, timeout=8)
            if r.ok:
                data = r.json()
                if data.get("status") == "ok":
                    out["ip"] = data.get("data")
                    out["type"] = "ip"
        elif is_asn:
            asn_num = re.sub(r"^AS", "", query, flags=re.IGNORECASE)
            urls = [
                f"https://api.bgpview.io/asn/{asn_num}",
                f"https://api.bgpview.io/asn/{asn_num}/prefixes",
                f"https://api.bgpview.io/asn/{asn_num}/peers",
            ]
            results: Dict[str, Any] = {}
            for u in urls:
                try:
                    assert_safe(u)
                    rr = requests.get(u, headers={"User-Agent": _UA}, timeout=8)
                    if rr.ok:
                        d = rr.json()
                        if d.get("status") == "ok":
                            results[u.rsplit("/", 1)[-1]] = d.get("data")
                except Exception as e:  # noqa: BLE001
                    log.debug("bgp partial %s: %s", u, e)
            if "asn" in results:
                out["asn"] = results["asn"]
            if "prefixes" in results:
                pv = results["prefixes"]
                out["prefixes"] = {
                    "ipv4": (pv.get("ipv4_prefixes") or [])[:20],
                    "ipv6": (pv.get("ipv6_prefixes") or [])[:10],
                    "total_v4": len(pv.get("ipv4_prefixes") or []),
                    "total_v6": len(pv.get("ipv6_prefixes") or []),
                }
            if "peers" in results:
                pp = results["peers"]
                out["peers"] = {
                    "upstream": (pp.get("ipv4_peers") or [])[:10],
                    "total": len(pp.get("ipv4_peers") or []),
                }
            out["type"] = "asn"
        else:
            return {"error": "unrecognised — use IPv4 or ASxxxxx", "query": query}
    except Exception as e:  # noqa: BLE001
        return {"error": f"bgp lookup failed: {e}", "query": query}
    return out


# ---------------------------------------------------------------------------
# MAC vendor
# ---------------------------------------------------------------------------
def fetch_mac(mac: str) -> Dict[str, Any]:
    """Look up a MAC address against macvendors.co (free, no key)."""
    mac = (mac or "").strip().upper()
    if not mac:
        return {"error": "missing mac"}
    clean = re.sub(r"[^A-F0-9:-]", "", mac)
    if not clean:
        return {"error": "invalid mac", "mac": mac}
    try:
        url = f"https://macvendors.co/api/{clean}"
        assert_safe(url)
        r = requests.get(url, headers={"User-Agent": _UA, "Accept": "application/json"},
                         timeout=8)
        if not r.ok:
            return {"error": f"macvendors http {r.status_code}", "mac": clean}
        data = r.json()
        result = (data or {}).get("result") or {}
        return {
            "mac": clean,
            "vendor": result.get("company") or "Not Found",
            "address": result.get("address"),
            "prefix": result.get("mac_prefix"),
        }
    except Exception as e:  # noqa: BLE001
        return {"error": f"mac lookup failed: {e}", "mac": clean}


# ---------------------------------------------------------------------------
# Phone (local — no remote)
# ---------------------------------------------------------------------------
# A representative region centroid table, sufficient for the line-type
# hint and country pinpoint. For more precision the libphonenumber
# library would be ideal, but pulling in a heavy dep just for this is
# not worth it. If you need exact geocoding, install
# `phonenumbers` (the PyPI libphonenumber port) and swap the
# `_phone_geo` body in for it.
_REGION_NAMES = {
    "US": "United States", "CA": "Canada", "GB": "United Kingdom",
    "AU": "Australia", "JP": "Japan", "CN": "China", "DE": "Germany",
    "FR": "France", "RU": "Russia", "BR": "Brazil", "IN": "India",
    "ZA": "South Africa", "KR": "South Korea", "ES": "Spain", "IT": "Italy",
    "MX": "Mexico", "NL": "Netherlands", "SE": "Sweden", "CH": "Switzerland",
    "PL": "Poland", "AR": "Argentina", "TR": "Türkiye", "UA": "Ukraine",
    "IL": "Israel", "SA": "Saudi Arabia", "AE": "United Arab Emirates",
}


def fetch_phone(number: str) -> Dict[str, Any]:
    """Best-effort phone geolocation.

    The implementation is intentionally simple (regex + region
    table). It does NOT replace libphonenumber; it provides a
    same-shape response without the dep so the API stays consistent
    with Osiris' /api/osint/phone."""
    number = (number or "").strip()
    if not number:
        return {"error": "missing number"}
    digits = re.sub(r"\D", "", number)
    # Auto-NANP: bare 10-digit US/CA numbers get +1.
    if len(digits) == 10 and not (number.startswith("+") or number.startswith("00")):
        digits = "1" + digits
    if not (7 <= len(digits) <= 15):
        return {"error": "phone length out of range", "number": number, "valid": False}
    # Country code: take the leading 1-3 digits and look it up in a
    # tiny static table of common codes. Anything we don't recognise
    # gets a generous "Unknown" rather than nothing.
    cc_map = {
        "1": "US", "44": "GB", "49": "DE", "33": "FR", "34": "ES",
        "39": "IT", "31": "NL", "46": "SE", "41": "CH", "48": "PL",
        "7": "RU", "86": "CN", "81": "JP", "82": "KR", "91": "IN",
        "55": "BR", "52": "MX", "54": "AR", "61": "AU", "64": "NZ",
        "27": "ZA", "972": "IL", "90": "TR", "380": "UA", "971": "AE",
        "966": "SA",
    }
    cc: Optional[str] = None
    for k in sorted(cc_map, key=len, reverse=True):
        if digits.startswith(k):
            cc = cc_map[k]
            digits = digits[len(k):]
            break
    region = _REGION_NAMES.get(cc or "", "Unknown")
    # NANP area code → coords (very rough, the big US/CA metros).
    coords: Optional[Tuple[float, float]] = None
    if cc == "US" and len(digits) == 10:
        area = digits[:3]
        # We only ship a handful of metro area codes here to keep
        # the table readable; the same pattern Osiris uses.
        big_metros = {
            "212": (40.7128, -74.0060), "310": (34.0522, -118.2437),
            "415": (37.7749, -122.4194), "312": (41.8781, -87.6298),
            "305": (25.7617, -80.1918), "702": (36.1699, -115.1398),
            "206": (47.6062, -122.3321), "202": (38.9072, -77.0369),
            "404": (33.7490, -84.3880), "617": (42.3601, -71.0589),
            "214": (32.7767, -96.7970), "713": (29.7604, -95.3698),
        }
        if area in big_metros:
            coords = big_metros[area]
    elif cc and cc in COUNTRY_CENTROIDS:
        coords = COUNTRY_CENTROIDS[cc]
    line_type = "MOBILE" if digits[:1] in ("7", "8", "9") else "LANDLINE"
    return {
        "query": number,
        "valid": True,
        "country_code": f"+{cc or '?'}",
        "region": region,
        "region_code": cc or "Unknown",
        "line_type": line_type,
        "national": digits,
        "lat": coords[0] if coords else None,
        "lng": coords[1] if coords else None,
    }


# ---------------------------------------------------------------------------
# GitHub user
# ---------------------------------------------------------------------------
def fetch_github_user(username: str) -> Dict[str, Any]:
    """Look up a GitHub user (keyless, rate-limited)."""
    username = (username or "").strip()
    if not username:
        return {"error": "missing user"}
    try:
        u = f"https://api.github.com/users/{username}"
        assert_safe(u)
        r1 = requests.get(u, headers={"User-Agent": "Estorides/1.1"}, timeout=8)
        if r1.status_code == 404:
            return {"error": "user not found", "username": username}
        if not r1.ok:
            return {"error": f"github http {r1.status_code}", "username": username}
        data = r1.json()
        repos: List[Dict[str, Any]] = []
        if data.get("public_repos", 0) > 0:
            try:
                u2 = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=5"
                assert_safe(u2)
                r2 = requests.get(u2, headers={"User-Agent": "Estorides/1.1"},
                                   timeout=8)
                if r2.ok:
                    arr = r2.json()
                    if isinstance(arr, list):
                        repos = [
                            {"name": x.get("name"), "language": x.get("language"),
                             "updated": x.get("updated_at")}
                            for x in arr
                        ]
            except Exception:  # noqa: BLE001
                pass
        return {
            "username": data.get("login"),
            "name": data.get("name"),
            "company": data.get("company"),
            "blog": data.get("blog"),
            "location": data.get("location"),
            "email": data.get("email"),
            "bio": data.get("bio"),
            "twitter": data.get("twitter_username"),
            "public_repos": data.get("public_repos"),
            "followers": data.get("followers"),
            "created_at": data.get("created_at"),
            "avatar_url": data.get("avatar_url"),
            "recent_repos": repos,
        }
    except Exception as e:  # noqa: BLE001
        return {"error": f"github lookup failed: {e}", "username": username}


# ---------------------------------------------------------------------------
# XposedOrNot leaks (alternative to HIBP with more detail)
# ---------------------------------------------------------------------------
def fetch_leaks(email: str) -> Dict[str, Any]:
    """Breach analytics for `email` via xposedornot (free, no key)."""
    email = (email or "").strip()
    if not email:
        return {"error": "missing email"}
    try:
        u = f"https://api.xposedornot.com/v1/breach-analytics?email={email}"
        assert_safe(u)
        r = requests.get(
            u,
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Estorides/1.1) Estorides/1.1",
            },
            timeout=10,
        )
        if r.status_code == 404:
            return {"email": email, "breached": False, "breaches": [], "data_exposed": []}
        if not r.ok:
            return {"error": f"xposedornot http {r.status_code}", "email": email}
        data = r.json()
        breach_list: List[str] = []
        if (data.get("BreachesSummary") or {}).get("site"):
            breach_list = [
                s for s in data["BreachesSummary"]["site"].split(";") if s
            ]
        exposed: set = set()
        for item in data.get("ExposedData") or []:
            for dc in item.get("data_classes") or []:
                exposed.add(dc)
        return {
            "email": email,
            "breached": bool(breach_list),
            "breaches": breach_list,
            "data_exposed": sorted(exposed),
        }
    except Exception as e:  # noqa: BLE001
        return {"error": f"leak lookup failed: {e}", "email": email}


# ---------------------------------------------------------------------------
# CISA Known Exploited Vulnerabilities
# ---------------------------------------------------------------------------
def fetch_cisa_kev(limit: int = 10, days: int = 30) -> Dict[str, Any]:
    """Recently-added CVEs from the CISA KEV feed (authoritative)."""
    limit = max(1, min(int(limit), 100))
    days = max(1, min(int(days), 365))
    data = _cached_get(
        "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
        cache_name="cisa_kev",
        ttl=3600,
    )
    if not isinstance(data, dict):
        return {"threats": [], "stats": {}, "error": "cisa feed unavailable"}
    vulns = data.get("vulnerabilities") or []
    cutoff = time.time() - days * 86400
    recent: List[Dict[str, Any]] = []
    for v in vulns:
        added = v.get("dateAdded") or ""
        try:
            ts = time.mktime(time.strptime(added, "%Y-%m-%d"))
        except (ValueError, TypeError):
            continue
        if ts < cutoff:
            continue
        recent.append({
            "id": v.get("cveID"),
            "name": v.get("vulnerabilityName"),
            "vendor": v.get("vendorProject"),
            "product": v.get("product"),
            "severity": "CRITICAL",
            "date": added,
            "due": v.get("dueDate"),
            "source": "CISA KEV",
        })
        if len(recent) >= limit:
            break
    return {
        "threats": recent,
        "stats": {
            "cisa_total": len(vulns),
            "recent_count": len(recent),
            "window_days": days,
            "threat_level": (
                "CRITICAL" if len(recent) >= 8
                else "HIGH" if len(recent) >= 4
                else "ELEVATED"
            ),
        },
    }


# ---------------------------------------------------------------------------
# Malware C2 (Feodo Tracker + URLhaus)
# ---------------------------------------------------------------------------
def fetch_malware_c2(limit: int = 200) -> Dict[str, Any]:
    """Active botnet C2 (Feodo) + recent malware URLs (URLhaus).

    Both abuse.ch, both keyless. Each entry is geolocated against the
    country centroid table with deterministic jitter so multiple
    threats in the same country don't stack on the same pixel."""
    limit = max(1, min(int(limit), 500))
    threats: List[Dict[str, Any]] = []
    nxt = 0

    # Feodo Tracker
    data = _cached_get(
        "https://feodotracker.abuse.ch/downloads/ipblocklist.json",
        cache_name="feodo_c2",
        ttl=900,
    )
    if isinstance(data, list):
        for entry in data[:limit]:
            cc = entry.get("country")
            if not cc or cc not in COUNTRY_CENTROIDS:
                continue
            lng, lat = COUNTRY_CENTROIDS[cc]
            j_lng = ((nxt * 173.7) % 200 - 100) / 100 * 4
            j_lat = ((nxt * 293.1) % 200 - 100) / 100 * 4
            threats.append({
                "id": f"feodo-{nxt}",
                "lat": lat + j_lat,
                "lng": lng + j_lng,
                "ip": entry.get("ip_address") or "unknown",
                "port": entry.get("dst_port") or 0,
                "malware": entry.get("malware") or "unknown",
                "status": entry.get("status") or "active",
                "first_seen": entry.get("first_seen"),
                "last_online": entry.get("last_online"),
                "country": cc,
                "threat_type": "botnet_c2",
            })
            nxt += 1
            if len(threats) >= limit:
                break

    # URLhaus
    if len(threats) < limit:
        try:
            u = "https://urlhaus-api.abuse.ch/v1/urls/recent/limit/200/"
            assert_safe(u)
            r = requests.get(u, headers={"User-Agent": _UA}, timeout=10)
            if r.ok:
                arr = (r.json() or {}).get("urls") or []
                for item in arr:
                    cc = item.get("country")
                    if not cc or cc not in COUNTRY_CENTROIDS:
                        continue
                    if len(threats) >= limit:
                        break
                    lng, lat = COUNTRY_CENTROIDS[cc]
                    j_lng = ((nxt * 173.7) % 200 - 100) / 100 * 4
                    j_lat = ((nxt * 293.1) % 200 - 100) / 100 * 4
                    threats.append({
                        "id": f"urlhaus-{nxt}",
                        "lat": lat + j_lat,
                        "lng": lng + j_lng,
                        "url": item.get("url"),
                        "threat": item.get("threat"),
                        "status": item.get("status"),
                        "date_added": item.get("date_added"),
                        "country": cc,
                        "threat_type": "malware_url",
                    })
                    nxt += 1
        except Exception as e:  # noqa: BLE001
            log.debug("urlhaus fetch failed: %s", e)

    return {"threats": threats, "count": len(threats), "fetched_at": time.time()}
