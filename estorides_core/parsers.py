"""
estorides_core.parsers
======================
A small library of structured parsers. Each parser knows how to take
a raw response from a specific OSINT source and pull out the things
the rest of the pipeline cares about: domain, IP, geolocation, etc.

The `parser` field of each YAML source selects one of these functions
via the `PARSERS` registry. New parsers are added with
`@register_parser("name")` or by appending to `PARSERS` directly.
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

# A parser takes whatever the HTTP client produced (dict / list / str /
# None) and returns the structured view. Parsers MUST be total: any
# unrecognised input must return an empty container, not raise. The
# orchestrator trusts this contract.
ParserFunc = Callable[[Any], Any]
ParserSpec = Union[ParserFunc, Tuple[ParserFunc, str]]  # (func, description)

log = logging.getLogger("estorides.parsers")


# --------------------------------------------------------------------- utils
def _flat(obj: Any) -> List[Any]:
    """Recursively flatten a dict/list into a list of leaf values."""
    out: List[Any] = []
    if isinstance(obj, dict):
        for v in obj.values():
            out.extend(_flat(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(_flat(v))
    else:
        out.append(obj)
    return out


def _first(obj: Any, *keys: str) -> Optional[Any]:
    """Recursively dig into a JSON-ish structure to find the first matching key."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys:
                return v
            sub = _first(v, *keys)
            if sub is not None:
                return sub
    elif isinstance(obj, list):
        for v in obj:
            sub = _first(v, *keys)
            if sub is not None:
                return sub
    return None


# ----------------------------------------------------------------- specific
def parse_dns_json(payload: Any) -> Dict[str, Any]:
    """Google/Cloudflare DNS-over-HTTPS response."""
    out: Dict[str, Any] = {"answers": [], "records": {}}
    if not isinstance(payload, dict):
        return out
    for ans in payload.get("Answer", []) or []:
        out["answers"].append(ans)
        rtype = ans.get("type")
        data = ans.get("data")
        if rtype is None or data is None:
            continue
        out["records"].setdefault(str(rtype), []).append(data)
    return out


def parse_crtsh_json(payload: Any) -> Dict[str, Any]:
    """crt.sh CT log response."""
    domains: List[str] = []
    issuers: List[str] = []
    if isinstance(payload, list):
        for cert in payload:
            if isinstance(cert, dict):
                name = cert.get("name_value") or cert.get("common_name")
                if name:
                    for n in str(name).split("\n"):
                        n = n.strip().lstrip("*.")
                        if n:
                            domains.append(n)
                if cert.get("issuer_name"):
                    issuers.append(str(cert["issuer_name"]))
    return {"subdomains": sorted(set(domains)), "issuers": sorted(set(issuers))}


def parse_rdap(payload: Any) -> Dict[str, Any]:
    """RDAP (RFC 7483) domain object.

    Returns a flat dict with registrar, registry handle, status flags,
    event dates, and any nameserver / entity hints. The structured
    result feeds two goals:

      1. Surface the registrar as an `entity` so the resolver can
         later ask "which other domains does MarkMonitor manage"
         (or whichever registrar came back) and fan out into the
         shared-infrastructure lane.
      2. Save the create / expire / updated dates so the timeline
         view can render them without a second pass.

    Defensive against missing fields — RDAP responses vary across
    registries and the spec allows a lot of optional bits.
    """
    if not isinstance(payload, dict):
        return {}
    out: Dict[str, Any] = {
        "handle": payload.get("handle"),
        "ldhName": payload.get("ldhName") or payload.get("unicodeName"),
        "status": payload.get("status") or [],
        "events": payload.get("events") or [],
        "registrar": None,
        "registrar_iana_id": None,
        "nameservers": [],
        "entities": [],
    }
    # Events: events[].eventAction -> eventDate.
    for ev in out["events"]:
        action = (ev.get("eventAction") or "").lower()
        if action in ("registration", "expiration", "last changed",
                      "last update of rdap database", "transfer"):
            out.setdefault("event_dates", {})[action] = ev.get("eventDate")
    # Entities: entities[].roles + vcardArray[1] (jCard-style list).
    for ent in payload.get("entities") or []:
        roles = ent.get("roles") or []
        vcard = (ent.get("vcardArray") or [None, []])[1] or []
        flat: Dict[str, Any] = {"roles": roles}
        for item in vcard:
            # jCard: [name, params, value-type, value]
            if not isinstance(item, list) or len(item) < 4:
                continue
            key = item[0]
            val = item[3]
            if key == "fn":
                flat["fn"] = val
            elif key == "email":
                flat["email"] = val
            elif key == "org":
                flat["org"] = val
            elif key == "tel":
                flat["phone"] = val
            elif key == "adr":
                flat["address"] = val
            elif key == "kind":
                # jCard "kind" tells us if this is an org, person, etc.
                flat["kind"] = val
        out["entities"].append(flat)
        if "registrar" in roles and flat.get("fn"):
            out["registrar"] = flat["fn"]
        # IANA registrar id lives in the publicIds array of the
        # registrar entity (per RFC 7483 §4.5).
        for pid in ent.get("publicIds") or []:
            if pid.get("type") == "IANA Registrar ID":
                out["registrar_iana_id"] = pid.get("identifier")
    # Nameservers.
    for ns in payload.get("nameservers") or []:
        ldh = ns.get("ldhName") or ns.get("unicodeName")
        if ldh:
            out["nameservers"].append(ldh)
    return out


def parse_ipapi(payload: Any) -> Dict[str, Any]:
    """ip-api.com response."""
    if not isinstance(payload, dict):
        return {}
    if payload.get("status") != "success":
        return {"error": payload.get("message", "no result")}
    return {
        "ip": payload.get("query"),
        "country": payload.get("country"),
        "countryCode": payload.get("countryCode"),
        "region": payload.get("regionName"),
        "city": payload.get("city"),
        "zip": payload.get("zip"),
        "lat": payload.get("lat"),
        "lon": payload.get("lon"),
        "timezone": payload.get("timezone"),
        "isp": payload.get("isp"),
        "org": payload.get("org"),
        "as": payload.get("as"),
        "reverse": payload.get("reverse"),
        "proxy": payload.get("proxy"),
        "hosting": payload.get("hosting"),
        "mobile": payload.get("mobile"),
    }


def parse_ipinfo(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict) or "ip" not in payload:
        return {"error": "no result"}
    return {
        "ip": payload.get("ip"),
        "city": payload.get("city"),
        "region": payload.get("region"),
        "country": payload.get("country"),
        "loc": payload.get("loc"),
        "org": payload.get("org"),
        "postal": payload.get("postal"),
        "timezone": payload.get("timezone"),
    }


def parse_ipapi_co(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict) or payload.get("error"):
        return {"error": str(payload.get("reason") or payload.get("error") or "no result")}
    return {k: payload.get(k) for k in (
        "ip", "city", "region", "country_name", "country_code", "continent_code",
        "latitude", "longitude", "timezone", "asn", "org", "currency", "languages",
    ) if k in payload}


def parse_shodan_internetdb(payload: Any) -> Dict[str, Any]:
    """internetdb.shodan.io — IP service summary."""
    if not isinstance(payload, dict) or "ip" not in payload:
        return {"error": "no result"}
    return {
        "ip": payload.get("ip"),
        "ports": payload.get("ports", []),
        "cpes": payload.get("cpes", []),
        "hostnames": payload.get("hostnames", []),
        "cves": payload.get("vulns", []),
        "tags": payload.get("tags", []),
    }


def parse_greynoise(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict) or "ip" not in payload:
        return {"error": "no result"}
    return {
        "ip": payload.get("ip"),
        "noise": payload.get("noise"),
        "riot": payload.get("riot"),
        "classification": payload.get("classification"),
        "name": payload.get("name"),
        "link": payload.get("link"),
        "last_seen": payload.get("last_seen"),
        "message": payload.get("message"),
    }


def parse_ipwhois(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict) or not payload.get("success", True):
        return {"error": str(payload.get("message", "no result"))}
    return {
        "ip": payload.get("ip"),
        "country": payload.get("country"),
        "region": payload.get("region"),
        "city": payload.get("city"),
        "latitude": payload.get("latitude"),
        "longitude": payload.get("longitude"),
        "asn": payload.get("asn"),
        "org": payload.get("org"),
        "isp": payload.get("isp"),
        "timezone": payload.get("timezone_name"),
        "type": payload.get("type"),
    }


def parse_abuseipdb(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict) or "data" not in payload:
        return {"error": "no result"}
    d = payload["data"]
    return {
        "ip": d.get("ipAddress"),
        "abuseConfidenceScore": d.get("abuseConfidenceScore"),
        "countryCode": d.get("countryCode"),
        "isp": d.get("isp"),
        "domain": d.get("domain"),
        "totalReports": d.get("totalReports"),
        "lastReportedAt": d.get("lastReportedAt"),
        "usageType": d.get("usageType"),
    }


def _vt_stats(attrs: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten VirusTotal v3 last_analysis_stats into a compact dict."""
    stats = attrs.get("last_analysis_stats") or {}
    if not isinstance(stats, dict):
        stats = {}
    return {
        "malicious": int(stats.get("malicious", 0) or 0),
        "suspicious": int(stats.get("suspicious", 0) or 0),
        "harmless": int(stats.get("harmless", 0) or 0),
        "undetected": int(stats.get("undetected", 0) or 0),
        "timeout": int(stats.get("timeout", 0) or 0),
    }


def parse_vt_ip(payload: Any) -> Dict[str, Any]:
    """VirusTotal v3 — IP address object."""
    if not isinstance(payload, dict) or "data" not in payload:
        return {"error": "no result"}
    data = payload["data"]
    attrs = data.get("attributes", {}) if isinstance(data, dict) else {}
    stats = _vt_stats(attrs)
    return {
        "ip": data.get("id"),
        "asn": attrs.get("asn"),
        "as_owner": attrs.get("as_owner"),
        "country": attrs.get("country"),
        "network": attrs.get("network"),
        "reputation": attrs.get("reputation"),
        "tags": attrs.get("tags", []),
        "malicious": stats["malicious"],
        "suspicious": stats["suspicious"],
        "last_analysis_stats": stats,
    }


def parse_vt_domain(payload: Any) -> Dict[str, Any]:
    """VirusTotal v3 — domain object."""
    if not isinstance(payload, dict) or "data" not in payload:
        return {"error": "no result"}
    data = payload["data"]
    attrs = data.get("attributes", {}) if isinstance(data, dict) else {}
    stats = _vt_stats(attrs)
    categories = attrs.get("categories", {})
    if isinstance(categories, dict):
        categories = sorted(set(str(v) for v in categories.values() if v))
    records = attrs.get("last_dns_records", []) or []
    ips = [r.get("value") for r in records
           if isinstance(r, dict) and r.get("type") in ("A", "AAAA") and r.get("value")]
    return {
        "domain": data.get("id"),
        "registrar": attrs.get("registrar"),
        "categories": categories,
        "creation_date": attrs.get("creation_date"),
        "reputation": attrs.get("reputation"),
        "resolved_ips": ips,
        "tags": attrs.get("tags", []),
        "malicious": stats["malicious"],
        "suspicious": stats["suspicious"],
        "last_analysis_stats": stats,
    }


def parse_vt_file(payload: Any) -> Dict[str, Any]:
    """VirusTotal v3 — file object."""
    if not isinstance(payload, dict) or "data" not in payload:
        return {"error": "no result"}
    data = payload["data"]
    attrs = data.get("attributes", {}) if isinstance(data, dict) else {}
    stats = _vt_stats(attrs)
    names = attrs.get("names", []) or []
    return {
        "sha256": attrs.get("sha256") or data.get("id"),
        "md5": attrs.get("md5"),
        "sha1": attrs.get("sha1"),
        "file_type": attrs.get("type_description") or attrs.get("type_tag"),
        "file_name": attrs.get("meaningful_name") or (names[0] if names else None),
        "names": names[:10],
        "size": attrs.get("size"),
        "reputation": attrs.get("reputation"),
        "tags": attrs.get("tags", []),
        "malicious": stats["malicious"],
        "suspicious": stats["suspicious"],
        "last_analysis_stats": stats,
    }


def parse_ripe_stat(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    records = payload.get("data", {}).get("records", [])
    out = []
    for r in records:
        if isinstance(r, list) and len(r) >= 2:
            out.append(r[0])
    return {"records": out, "irr_records": payload.get("data", {}).get("irr_records", [])}


def parse_nominatim(payload: Any) -> List[Dict[str, Any]]:
    if not isinstance(payload, list):
        return []
    out = []
    for hit in payload[:5]:
        if not isinstance(hit, dict):
            continue
        out.append({
            "display_name": hit.get("display_name"),
            "lat": hit.get("lat"),
            "lon": hit.get("lon"),
            "type": hit.get("type"),
            "category": hit.get("category"),
            "address": hit.get("address", {}),
        })
    return out


def parse_urlscan(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    out = {"results": [], "stats": {}}
    for r in payload.get("results", []) or []:
        if not isinstance(r, dict):
            continue
        page = r.get("page", {}) or {}
        out["results"].append({
            "url": page.get("url"),
            "domain": page.get("domain"),
            "ip": page.get("ip"),
            "country": page.get("country"),
            "server": page.get("server"),
            "tls_issuer": (page.get("tls") or {}).get("issuer") if isinstance(page.get("tls"), dict) else None,
            "screenshot": r.get("screenshot"),
            "submittedAt": r.get("task", {}).get("submittedAt") if isinstance(r.get("task"), dict) else None,
            "technologies": [t.get("app") for t in (r.get("tech") or []) if isinstance(t, dict)],
        })
    return out


def parse_wayback_cdx(payload: Any) -> List[Dict[str, Any]]:
    """CDX returns a list where the first row is the header."""
    if not isinstance(payload, list) or not payload:
        return []
    header = payload[0]
    out = []
    for row in payload[1:50]:
        if not isinstance(row, list):
            continue
        out.append(dict(zip(header, row)))
    return out


def parse_wayback_avail(payload: Any) -> Dict[str, Any]:
    snap = ((payload or {}).get("archived_snapshots") or {}).get("closest") or {}
    return {
        "available": bool(snap.get("available")),
        "url": snap.get("url"),
        "timestamp": snap.get("timestamp"),
    }


def parse_threatfox(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "query_status": payload.get("query_status"),
        "iocs": payload.get("data", []) or [],
    }


def parse_urlhaus(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "query_status": payload.get("query_status"),
        "urls": payload.get("urls", []) or [],
    }


def parse_urlhaus_payloads(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "query_status": payload.get("query_status"),
        "payloads": payload.get("payloads", []) or [],
    }


def parse_malwarebazaar(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "query_status": payload.get("query_status"),
        "samples": payload.get("data", []) or [],
    }


def parse_otx(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    pulses = payload.get("results", []) or []
    return {
        "count": payload.get("count", 0),
        "pulses": [
            {
                "id": p.get("id"),
                "name": p.get("name"),
                "description": p.get("description"),
                "adversary": p.get("adversary"),
                "targeted_countries": p.get("targeted_countries"),
                "malware_families": p.get("malware_families"),
                "attack_ids": p.get("attack_ids"),
                "indicators_count": len(p.get("indicators", []) or []),
                "tags": p.get("tags"),
                "created": p.get("created"),
            }
            for p in pulses
        ],
    }


def parse_hibp_breach(payload: Any) -> List[Dict[str, Any]]:
    if not isinstance(payload, list):
        return []
    return [
        {
            "Name": b.get("Name"),
            "Domain": b.get("Domain"),
            "BreachDate": b.get("BreachDate"),
            "PwnCount": b.get("PwnCount"),
            "DataClasses": b.get("DataClasses"),
            "IsSensitive": b.get("IsSensitive"),
            "Description": (b.get("Description") or "")[:300],
        }
        for b in payload
        if isinstance(b, dict)
    ]


def parse_hibp_paste(payload: Any) -> List[Dict[str, Any]]:
    if not isinstance(payload, list):
        return []
    return [
        {
            "Source": p.get("Source"),
            "Id": p.get("Id"),
            "Title": p.get("Title"),
            "Date": p.get("Date"),
            "EmailCount": p.get("EmailCount"),
        }
        for p in payload
        if isinstance(p, dict)
    ]


def parse_phonebook(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "total": payload.get("total"),
        "results": [
            {
                "name": r.get("name"),
                "domain": r.get("domain"),
                "type": r.get("type"),
                "firstname": r.get("firstname"),
                "lastname": r.get("lastname"),
                "department": r.get("department"),
                "position": r.get("position"),
            }
            for r in (payload.get("results") or [])
            if isinstance(r, dict)
        ],
    }


def parse_wikipedia(payload: Any) -> List[Dict[str, Any]]:
    hits = (((payload or {}).get("query") or {}).get("search") or [])
    return [
        {"title": h.get("title"), "snippet": re.sub("<.*?>", "", h.get("snippet", "")),
         "timestamp": h.get("timestamp")}
        for h in hits if isinstance(h, dict)
    ]


def parse_wikidata(payload: Any) -> List[Dict[str, Any]]:
    hits = ((payload or {}).get("search") or [])
    return [
        {
            "id": h.get("id"),
            "label": h.get("label"),
            "description": h.get("description") or h.get("match", {}).get("text"),
        }
        for h in hits if isinstance(h, dict)
    ]


def parse_openalex(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    results = payload.get("results", []) or []
    return {
        "meta": payload.get("meta", {}),
        "results": [
            {
                "id": r.get("id"),
                "doi": r.get("doi"),
                "title": r.get("title") or r.get("display_name"),
                "publication_year": r.get("publication_year"),
                "cited_by_count": r.get("cited_by_count"),
                "authors": [a.get("author", {}).get("display_name") for a in (r.get("authorships") or []) if isinstance(a, dict)],
            }
            for r in results
        ],
    }


def parse_crossref(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    items = ((payload.get("message") or {}).get("items") or [])
    return {
        "items": [
            {
                "DOI": i.get("DOI"),
                "title": (i.get("title") or [""])[0],
                "container_title": (i.get("container-title") or [""])[0],
                "publisher": i.get("publisher"),
                "type": i.get("type"),
                "URL": i.get("URL"),
                "is_referenced_by_count": i.get("is-referenced-by-count"),
            }
            for i in items if isinstance(i, dict)
        ]
    }


def parse_arxiv(payload: Any) -> List[Dict[str, Any]]:
    """arXiv returns Atom XML; we expect callers to have converted to a dict."""
    if isinstance(payload, dict):
        payload = payload.get("entries", [])
    if not isinstance(payload, list):
        return []
    out = []
    for e in payload:
        if not isinstance(e, dict):
            continue
        out.append({
            "id": e.get("id"),
            "title": re.sub(r"\s+", " ", (e.get("title") or "")).strip(),
            "summary": (e.get("summary") or "")[:500],
            "authors": [a.get("name") for a in (e.get("authors") or []) if isinstance(a, dict)],
            "published": e.get("published"),
            "categories": e.get("categories") or [],
        })
    return out


def parse_nvd_cve(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    vulns = payload.get("vulnerabilities", []) or []
    return {
        "totalResults": payload.get("totalResults"),
        "items": [
            {
                "cve": c.get("cve", {}).get("id"),
                "published": c.get("cve", {}).get("published"),
                "descriptions": [
                    d.get("value") for d in ((c.get("cve", {}).get("descriptions") or []))
                    if isinstance(d, dict) and d.get("lang") == "en"
                ],
                "metrics": c.get("cve", {}).get("metrics", {}),
                "references_count": len(c.get("cve", {}).get("references", []) or []),
            }
            for c in vulns if isinstance(c, dict)
        ],
    }


def parse_github_advisories(payload: Any) -> List[Dict[str, Any]]:
    if not isinstance(payload, list):
        return []
    return [
        {
            "ghsa_id": a.get("ghsa_id"),
            "cve_id": a.get("cve_id"),
            "severity": a.get("severity"),
            "summary": a.get("summary"),
            "description": (a.get("description") or "")[:300],
            "published_at": a.get("published_at"),
            "vulnerabilities": [
                {
                    "package": v.get("package", {}).get("name"),
                    "ecosystem": v.get("package", {}).get("ecosystem"),
                    "vulnerable_version_range": v.get("vulnerable_version_range"),
                }
                for v in (a.get("vulnerabilities") or [])
            ],
        }
        for a in payload if isinstance(a, dict)
    ]


def parse_blockchain_btc(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "address": payload.get("address"),
        "balance": payload.get("final_balance"),
        "total_received": payload.get("total_received"),
        "total_sent": payload.get("total_sent"),
        "n_tx": payload.get("n_tx"),
        "txs": [
            {"hash": t.get("hash"), "time": t.get("time"), "result": t.get("result")}
            for t in (payload.get("txs") or [])[:10]
        ],
    }


def parse_blockstream(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    chain = payload.get("chain_stats", {}) or {}
    return {
        "address": payload.get("address"),
        "chain_stats": {
            "funded_txo_count": chain.get("funded_txo_count"),
            "spent_txo_count": chain.get("spent_txo_count"),
            "funded_txo_sum": chain.get("funded_txo_sum"),
            "spent_txo_sum": chain.get("spent_txo_sum"),
        },
        "mempool_stats": payload.get("mempool_stats", {}),
    }


def parse_ethplorer(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "address": payload.get("address"),
        "ETH": (payload.get("ETH") or {}).get("balance"),
        "countTxs": payload.get("countTxs"),
        "tokens": [
            {"symbol": t.get("tokenInfo", {}).get("symbol"),
             "name": t.get("tokenInfo", {}).get("name"),
             "balance": t.get("balance")}
            for t in (payload.get("tokens") or [])
        ],
    }


def parse_microlink(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    status = payload.get("status", "unknown")
    data = payload.get("data", {}) or {}
    if status != "success":
        return {"status": status}
    return {
        "url": data.get("url"),
        "title": data.get("title"),
        "description": data.get("description"),
        "lang": data.get("lang"),
        "author": data.get("author"),
        "publisher": data.get("publisher"),
        "image": (data.get("image") or {}).get("url") if isinstance(data.get("image"), dict) else data.get("image"),
        "logo": (data.get("logo") or {}).get("url") if isinstance(data.get("logo"), dict) else data.get("logo"),
        "screenshot": (data.get("screenshot") or {}).get("url") if isinstance(data.get("screenshot"), dict) else None,
    }


def parse_github_user(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict) or "login" not in payload:
        return {"error": "no result"}
    return {
        "login": payload.get("login"),
        "name": payload.get("name"),
        "bio": payload.get("bio"),
        "email": payload.get("email"),
        "company": payload.get("company"),
        "location": payload.get("location"),
        "blog": payload.get("blog"),
        "twitter": payload.get("twitter_username"),
        "avatar": payload.get("avatar_url"),
        "followers": payload.get("followers"),
        "public_repos": payload.get("public_repos"),
        "created_at": payload.get("created_at"),
        "html_url": payload.get("html_url"),
    }


def parse_github_search(payload: Any) -> List[Dict[str, Any]]:
    items = ((payload or {}).get("items") or [])
    return [
        {
            "name": i.get("name") or i.get("path"),
            "full_name": i.get("full_name") or i.get("html_url"),
            "description": i.get("description"),
            "language": i.get("language"),
            "stars": i.get("stargazers_count"),
            "url": i.get("html_url") or i.get("url"),
        }
        for i in items if isinstance(i, dict)
    ][:30]


def parse_reddit(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    data = (payload.get("data") or {})
    if "children" in data:
        # listing
        children = data.get("children", [])
        return {
            "kind": "listing",
            "count": len(children),
            "items": [
                ((c.get("data") or {}).get("title"),
                 (c.get("data") or {}).get("url"),
                 (c.get("data") or {}).get("subreddit"),
                 (c.get("data") or {}).get("created_utc"))
                for c in children if isinstance(c, dict)
            ],
        }
    # user about
    return {
        "kind": "user",
        "name": data.get("name"),
        "link_karma": data.get("link_karma"),
        "comment_karma": data.get("comment_karma"),
        "created_utc": data.get("created_utc"),
        "is_mod": data.get("is_mod"),
        "is_gold": data.get("is_gold"),
    }


def parse_mastodon(payload: Any) -> List[Dict[str, Any]]:
    accounts = ((payload or {}).get("accounts") or [])
    return [
        {
            "id": a.get("id"),
            "username": a.get("username"),
            "display_name": a.get("display_name"),
            "url": a.get("url"),
            "instance": (a.get("url") or "").split("/@")[-1].split("/")[0] if a.get("url") else None,
            "followers_count": a.get("followers_count"),
            "note": re.sub("<.*?>", "", a.get("note") or "")[:200],
        }
        for a in accounts if isinstance(a, dict)
    ]


def parse_keybase(payload: Any) -> Dict[str, Any]:
    them = ((payload or {}).get("them") or [])
    if not them:
        return {"error": "no result"}
    p = them[0] or {}
    proofs = p.get("proofs_summary", {}) or {}
    return {
        "username": p.get("basics", {}).get("username"),
        "full_name": p.get("profile", {}).get("full_name"),
        "bio": p.get("profile", {}).get("bio"),
        "location": p.get("profile", {}).get("location"),
        "twitter": proofs.get("twitter", [{}])[0].get("service_url") if proofs.get("twitter") else None,
        "github": proofs.get("github", [{}])[0].get("service_url") if proofs.get("github") else None,
        "public_keys": [
            {"bundle": k.get("bundle"), "key_fingerprint": k.get("key_fingerprint")}
            for k in (p.get("public_keys", {}) or {}).get("primary", []) or []
        ],
        "devices": [
            {"name": d.get("device", {}).get("name"), "type": d.get("device", {}).get("type")}
            for d in (p.get("devices", []) or [])
        ],
    }


def parse_hackernews(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict) or "id" not in payload:
        return {"error": "no result"}
    return {
        "id": payload.get("id"),
        "created": payload.get("created"),
        "karma": payload.get("karma"),
        "about": payload.get("about"),
        "submitted_count": len(payload.get("submitted", []) or []),
    }


def parse_reddit_search(payload: Any) -> List[Dict[str, Any]]:
    children = (((payload or {}).get("data") or {}).get("children") or [])
    return [
        {
            "name": (c.get("data") or {}).get("display_name"),
            "title": (c.get("data") or {}).get("title"),
            "subscribers": (c.get("data") or {}).get("subscribers"),
            "url": (c.get("data") or {}).get("url"),
            "public_description": (c.get("data") or {}).get("public_description"),
        }
        for c in children if isinstance(c, dict)
    ]


def parse_dev_to(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict) or "username" not in payload:
        return {"error": "no result"}
    return {
        "username": payload.get("username"),
        "name": payload.get("name"),
        "summary": payload.get("summary"),
        "location": payload.get("location"),
        "website_url": payload.get("website_url"),
        "github_username": payload.get("github_username"),
        "twitter_username": payload.get("twitter_username"),
        "joined_at": payload.get("joined_at"),
    }


def parse_text_lines(payload: Any) -> List[str]:
    """Generic: split raw_text by newlines, drop empties."""
    if isinstance(payload, dict) and "raw_text" in payload:
        return [ln for ln in (payload.get("raw_text") or "").splitlines() if ln.strip()]
    if isinstance(payload, list):
        return [str(x) for x in payload]
    if isinstance(payload, str):
        return [ln for ln in payload.splitlines() if ln.strip()]
    return []


def parse_raw_text(payload: Any) -> str:
    if isinstance(payload, dict) and "raw_text" in payload:
        return payload.get("raw_text", "")
    if isinstance(payload, (str, int, float)):
        return str(payload)
    return json.dumps(payload, ensure_ascii=False)


def parse_http_headers(payload: Any) -> Dict[str, str]:
    """hackertarget returns text; expect a one-line-per-header response."""
    if isinstance(payload, dict) and "raw_text" in payload:
        text = payload["raw_text"]
    elif isinstance(payload, str):
        text = payload
    else:
        return {}
    out: Dict[str, str] = {}
    for line in text.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def parse_whois_text(payload: Any) -> Dict[str, str]:
    out: Dict[str, str] = {}
    if isinstance(payload, dict) and "raw_text" in payload:
        text = payload["raw_text"]
    elif isinstance(payload, str):
        text = payload
    else:
        return out
    for line in text.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


# ------------------------------------------------------------- registry ----
PARSERS = {
    "dns_json": parse_dns_json,
    "crtsh_json": parse_crtsh_json,
    "rdap_domain": parse_rdap,
    "ipapi": parse_ipapi,
    "ipinfo": parse_ipinfo,
    "ipapi_co": parse_ipapi_co,
    "shodan_internetdb": parse_shodan_internetdb,
    "greynoise": parse_greynoise,
    "ipwhois": parse_ipwhois,
    "abuseipdb": parse_abuseipdb,
    "vt_ip": parse_vt_ip,
    "vt_domain": parse_vt_domain,
    "vt_file": parse_vt_file,
    "ripe_stat": parse_ripe_stat,
    "nominatim": parse_nominatim,
    "urlscan": parse_urlscan,
    "wayback_cdx": parse_wayback_cdx,
    "wayback_avail": parse_wayback_avail,
    "threatfox": parse_threatfox,
    "urlhaus": parse_urlhaus,
    "urlhaus_payloads": parse_urlhaus_payloads,
    "malwarebazaar": parse_malwarebazaar,
    "otx": parse_otx,
    "hibp_breach": parse_hibp_breach,
    "hibp_paste": parse_hibp_paste,
    "phonebook": parse_phonebook,
    "wikipedia": parse_wikipedia,
    "wikidata": parse_wikidata,
    "openalex": parse_openalex,
    "crossref": parse_crossref,
    "arxiv": parse_arxiv,
    "nvd_cve": parse_nvd_cve,
    "github_advisories": parse_github_advisories,
    "blockchain_btc": parse_blockchain_btc,
    "blockstream": parse_blockstream,
    "ethplorer": parse_ethplorer,
    "microlink": parse_microlink,
    "github_user": parse_github_user,
    "github_search": parse_github_search,
    "reddit": parse_reddit,
    "mastodon": parse_mastodon,
    "keybase": parse_keybase,
    "hackernews": parse_hackernews,
    "reddit_search": parse_reddit_search,
    "dev_to": parse_dev_to,
    "text_lines": parse_text_lines,
    "raw_text": parse_raw_text,
    "http_headers": parse_http_headers,
    "whois_text": parse_whois_text,
    "dehashed": lambda x: x,
    "intelx": lambda x: x,
    "wigle": lambda x: x,
    "opensky": lambda x: x,
    "n2yo": lambda x: x,
    "screenshot": lambda x: x,
    "exif": lambda x: x,
    "openphish": parse_text_lines,
    "phishtank": lambda x: x,
    "abuse": parse_text_lines,
    "feodo": parse_text_lines,
    "sslbl": parse_text_lines,
    "ddg_html": parse_raw_text,
    "http_probe": parse_raw_text,
    "openweather_geo": lambda x: x,
    "timezone": lambda x: x,
    "opengraph": parse_microlink,  # best-effort reuse
    "blockchain_tx": parse_raw_text,
    "cve_circl": parse_raw_text,
    "exploitdb": parse_text_lines,
    "blocklist": parse_text_lines,
}


def get_parser(name: str) -> ParserFunc:
    """Return the parser function for `name`, or a passthrough lambda.

    Unknown parser names deliberately fall through to `parse_raw_text`
    so a source YAML with a typo in the `parser` field never crashes
    the run — it just produces a less-structured observation.
    """
    spec = PARSERS.get(name, parse_raw_text)
    if isinstance(spec, tuple):
        return spec[0]
    return spec


def register_parser(name: str, description: str = "") -> ParserFunc:
    """Decorator: register `func` as a parser under `name`.

    Used by addon authors and tests to extend the catalog without
    touching the central `PARSERS` dict. Idempotent: re-registering
    the same name overwrites the previous entry, with a debug log so
    a typo doesn't silently drop a parser.
    """
    def deco(func: ParserFunc) -> ParserFunc:
        if name in PARSERS:
            log.debug("re-registering parser %r (overwrites previous)", name)
        PARSERS[name] = (func, description) if description else func
        return func
    return deco


def list_parsers() -> List[Tuple[str, str]]:
    """Return (name, description) tuples for every registered parser.

    Used by the CLI `status` endpoint to advertise the available
    parser names, and by tests to assert that a custom parser made it
    into the registry.
    """
    out: List[Tuple[str, str]] = []
    for name, spec in PARSERS.items():
        if isinstance(spec, tuple):
            out.append((name, spec[1]))
        else:
            out.append((name, spec.__doc__ or ""))
    return sorted(out)
