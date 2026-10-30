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
from collections.abc import Callable
from typing import Any, Union

# A parser takes whatever the HTTP client produced (dict / list / str /
# None) and returns the structured view. Parsers MUST be total: any
# unrecognised input must return an empty container, not raise. The
# orchestrator trusts this contract.
ParserFunc = Callable[[Any], Any]
ParserSpec = Union[ParserFunc, tuple[ParserFunc, str]]  # (func, description)

log = logging.getLogger("estorides.parsers")


# --------------------------------------------------------------------- utils
def _d(obj: Any) -> dict[str, Any]:
    """Return `obj` as a dict, or an empty dict when it is anything else.

    Remote JSON frequently puts `null`/a string where a nested object is
    expected. Coercing here keeps every parser total (the module contract).
    """
    return obj if isinstance(obj, dict) else {}


def _first_dict(items: Any) -> dict[str, Any]:
    """Return the first dict element of `items`, else an empty dict."""
    if isinstance(items, list) and items:
        return _d(items[0])
    return {}


def _list(obj: Any) -> list[Any]:
    """Return `obj` as a list, or [] when it is anything else.

    Guards the very common `...get("items") or []` idiom, which is NOT
    safe against a truthy non-iterable (a remote `"items": true`).
    """
    return obj if isinstance(obj, list) else []


def _text(obj: Any) -> str:
    """Return `obj` as a string, or "" when it is anything else."""
    return obj if isinstance(obj, str) else ""


# ----------------------------------------------------------------- specific
def parse_dns_json(payload: Any) -> dict[str, Any]:
    """Google/Cloudflare DNS-over-HTTPS response."""
    out: dict[str, Any] = {"answers": [], "records": {}}
    if not isinstance(payload, dict):
        return out
    for raw_ans in _list(payload.get("Answer")):
        ans = _d(raw_ans)
        out["answers"].append(raw_ans)
        rtype = ans.get("type")
        data = ans.get("data")
        if rtype is None or data is None:
            continue
        out["records"].setdefault(str(rtype), []).append(data)
    return out


def parse_crtsh_json(payload: Any) -> dict[str, Any]:
    """crt.sh CT log response."""
    domains: list[str] = []
    issuers: list[str] = []
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


def parse_rdap(payload: Any) -> dict[str, Any]:
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
    out: dict[str, Any] = {
        "handle": payload.get("handle"),
        "ldhName": payload.get("ldhName") or payload.get("unicodeName"),
        "status": payload.get("status") or [],
        "events": _list(payload.get("events")),
        "registrar": None,
        "registrar_iana_id": None,
        "nameservers": [],
        "entities": [],
    }
    # Events: events[].eventAction -> eventDate.
    for raw_ev in out["events"]:
        ev = _d(raw_ev)
        action = _text(ev.get("eventAction")).lower()
        if action in ("registration", "expiration", "last changed",
                      "last update of rdap database", "transfer"):
            out.setdefault("event_dates", {})[action] = ev.get("eventDate")
    # Entities: entities[].roles + vcardArray[1] (jCard-style list).
    for raw_ent in _list(payload.get("entities")):
        ent = _d(raw_ent)
        roles = ent.get("roles") or []
        vcard_raw = ent.get("vcardArray")
        vcard = _list(vcard_raw[1]) if isinstance(vcard_raw, list) and len(vcard_raw) > 1 else []
        flat: dict[str, Any] = {"roles": roles}
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
        if isinstance(roles, list) and "registrar" in roles and flat.get("fn"):
            out["registrar"] = flat["fn"]
        # IANA registrar id lives in the publicIds array of the
        # registrar entity (per RFC 7483 §4.5).
        for raw_pid in _list(ent.get("publicIds")):
            pid = _d(raw_pid)
            if pid.get("type") == "IANA Registrar ID":
                out["registrar_iana_id"] = pid.get("identifier")
    # Nameservers.
    for raw_ns in _list(payload.get("nameservers")):
        ns = _d(raw_ns)
        ldh = ns.get("ldhName") or ns.get("unicodeName")
        if ldh:
            out["nameservers"].append(ldh)
    return out


def parse_ipapi(payload: Any) -> dict[str, Any]:
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


def parse_ipinfo(payload: Any) -> dict[str, Any]:
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


def parse_ipapi_co(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or payload.get("error"):
        data = _d(payload)
        return {"error": str(data.get("reason") or data.get("error") or "no result")}
    return {k: payload.get(k) for k in (
        "ip", "city", "region", "country_name", "country_code", "continent_code",
        "latitude", "longitude", "timezone", "asn", "org", "currency", "languages",
    ) if k in payload}


def parse_shodan_internetdb(payload: Any) -> dict[str, Any]:
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


def parse_greynoise(payload: Any) -> dict[str, Any]:
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


def parse_ipwhois(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or not payload.get("success", True):
        return {"error": str(_d(payload).get("message", "no result"))}
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


def parse_abuseipdb(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or "data" not in payload:
        return {"error": "no result"}
    d = _d(payload.get("data"))
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


def _vt_stats(attrs: dict[str, Any]) -> dict[str, Any]:
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


def parse_vt_ip(payload: Any) -> dict[str, Any]:
    """VirusTotal v3 — IP address object."""
    if not isinstance(payload, dict) or "data" not in payload:
        return {"error": "no result"}
    data = _d(payload.get("data"))
    attrs = _d(data.get("attributes"))
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


def parse_vt_domain(payload: Any) -> dict[str, Any]:
    """VirusTotal v3 — domain object."""
    if not isinstance(payload, dict) or "data" not in payload:
        return {"error": "no result"}
    data = _d(payload.get("data"))
    attrs = _d(data.get("attributes"))
    stats = _vt_stats(attrs)
    categories = attrs.get("categories", {})
    if isinstance(categories, dict):
        categories = sorted(set(str(v) for v in categories.values() if v))
    records = _list(attrs.get("last_dns_records"))
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


def parse_vt_file(payload: Any) -> dict[str, Any]:
    """VirusTotal v3 — file object."""
    if not isinstance(payload, dict) or "data" not in payload:
        return {"error": "no result"}
    data = _d(payload.get("data"))
    attrs = _d(data.get("attributes"))
    stats = _vt_stats(attrs)
    names = _list(attrs.get("names"))
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


def parse_bgpview(payload: Any) -> dict[str, Any]:
    """BGPView IP/ASN response (keyless). Total: never raises."""
    empty: dict[str, Any] = {"prefixes": [], "asns": [], "rir": "", "allocation": ""}
    if not isinstance(payload, dict):
        return empty
    if payload.get("status") != "ok":
        return empty
    data = _d(payload.get("data"))
    prefixes: list[Any] = []
    asns: list[Any] = []
    for p in _list(data.get("prefixes"))[:20]:
        pd = _d(p)
        if pd.get("prefix"):
            prefixes.append(pd.get("prefix"))
        asn = _d(pd.get("asn")).get("asn")
        if asn is not None and asn not in asns:
            asns.append(asn)
    for key in ("asns", "asns_ipv4", "asns_ipv6"):
        for a in _list(data.get(key))[:20]:
            ad = _d(a)
            asn = ad.get("asn", a if isinstance(a, int) else None)
            if asn is not None and asn not in asns:
                asns.append(asn)
    rir = _d(data.get("rir_allocation"))
    return {
        "prefixes": prefixes,
        "asns": asns,
        "rir": rir.get("rir_name", ""),
        "allocation": rir.get("prefix", ""),
    }


def parse_cisa_kev(payload: Any) -> dict[str, Any]:
    """CISA KEV catalog (keyless). Capped at 20 items. Total: never raises."""
    if not isinstance(payload, dict):
        return {"vulnerabilities": [], "total": 0}
    vulns = _list(payload.get("vulnerabilities"))
    out: list[Any] = []
    for v in vulns[:20]:
        vd = _d(v)
        out.append({
            "cveID": vd.get("cveID", ""),
            "vendorProject": vd.get("vendorProject", ""),
            "product": vd.get("product", ""),
            "vulnerabilityName": vd.get("vulnerabilityName", ""),
            "dateAdded": vd.get("dateAdded", ""),
            "dueDate": vd.get("dueDate", ""),
        })
    return {"vulnerabilities": out, "total": len(vulns)}


def parse_ripe_stat(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    data = _d(payload.get("data"))
    out = []
    for r in _list(data.get("records")):
        if isinstance(r, list) and len(r) >= 2:
            out.append(r[0])
    return {"records": out, "irr_records": _list(data.get("irr_records"))}


def parse_nominatim(payload: Any) -> list[dict[str, Any]]:
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


def parse_urlscan(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    out = {"results": [], "stats": {}}
    for r in _list(payload.get("results")):
        if not isinstance(r, dict):
            continue
        page = _d(r.get("page"))
        out["results"].append({
            "url": page.get("url"),
            "domain": page.get("domain"),
            "ip": page.get("ip"),
            "country": page.get("country"),
            "server": page.get("server"),
            "tls_issuer": _d(page.get("tls")).get("issuer"),
            "screenshot": r.get("screenshot"),
            "submittedAt": _d(r.get("task")).get("submittedAt"),
            "technologies": [t.get("app") for t in _list(r.get("tech")) if isinstance(t, dict)],
        })
    return out


def parse_wayback_cdx(payload: Any) -> list[dict[str, Any]]:
    """CDX returns a list where the first row is the header."""
    if not isinstance(payload, list) or not payload:
        return []
    header = payload[0]
    if not isinstance(header, list) or not all(isinstance(h, str) for h in header):
        return []
    out = []
    for row in payload[1:50]:
        if not isinstance(row, list):
            continue
        out.append(dict(zip(header, row)))
    return out


def parse_wayback_avail(payload: Any) -> dict[str, Any]:
    snap = _d(_d(payload).get("archived_snapshots")).get("closest") or {}
    snap = _d(snap)
    return {
        "available": bool(snap.get("available")),
        "url": snap.get("url"),
        "timestamp": snap.get("timestamp"),
    }


def parse_threatfox(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "query_status": payload.get("query_status"),
        "iocs": _list(payload.get("data")),
    }


def parse_urlhaus(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "query_status": payload.get("query_status"),
        "urls": _list(payload.get("urls")),
    }


def parse_urlhaus_payloads(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "query_status": payload.get("query_status"),
        "payloads": payload.get("payloads", []) or [],
    }


def parse_malwarebazaar(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "query_status": payload.get("query_status"),
        "samples": payload.get("data", []) or [],
    }


def parse_otx(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    pulses = _list(payload.get("results"))
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
                "indicators_count": len(p.get("indicators") or []),
                "tags": p.get("tags"),
                "created": p.get("created"),
            }
            for p in pulses
            if isinstance(p, dict)
        ],
    }


def parse_hibp_breach(payload: Any) -> list[dict[str, Any]]:
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


def parse_hibp_paste(payload: Any) -> list[dict[str, Any]]:
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


def parse_phonebook(payload: Any) -> dict[str, Any]:
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
            for r in _list(payload.get("results"))
            if isinstance(r, dict)
        ],
    }


def parse_wikipedia(payload: Any) -> list[dict[str, Any]]:
    hits = _list(_d(_d(payload).get("query")).get("search"))
    return [
        {"title": h.get("title"), "snippet": re.sub("<.*?>", "", _text(h.get("snippet"))),
         "timestamp": h.get("timestamp")}
        for h in hits if isinstance(h, dict)
    ]


def parse_wikidata(payload: Any) -> list[dict[str, Any]]:
    hits = _list(_d(payload).get("search"))
    return [
        {
            "id": h.get("id"),
            "label": h.get("label"),
            "description": h.get("description") or _d(h.get("match")).get("text"),
        }
        for h in hits if isinstance(h, dict)
    ]


def parse_openalex(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    results = _list(payload.get("results"))
    return {
        "meta": _d(payload.get("meta")),
        "results": [
            {
                "id": r.get("id"),
                "doi": r.get("doi"),
                "title": r.get("title") or r.get("display_name"),
                "publication_year": r.get("publication_year"),
                "cited_by_count": r.get("cited_by_count"),
                "authors": [
                    _d(a.get("author")).get("display_name")
                    for a in _list(r.get("authorships"))
                    if isinstance(a, dict)
                ],
            }
            for r in results
            if isinstance(r, dict)
        ],
    }


def parse_crossref(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    items = _list(_d(payload.get("message")).get("items"))
    return {
        "items": [
            {
                "DOI": i.get("DOI"),
                "title": (_list(i.get("title")) or [""])[0],
                "container_title": (_list(i.get("container-title")) or [""])[0],
                "publisher": i.get("publisher"),
                "type": i.get("type"),
                "URL": i.get("URL"),
                "is_referenced_by_count": i.get("is-referenced-by-count"),
            }
            for i in items if isinstance(i, dict)
        ]
    }


def parse_arxiv(payload: Any) -> list[dict[str, Any]]:
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
            "title": re.sub(r"\s+", " ", _text(e.get("title"))).strip(),
            "summary": _text(e.get("summary"))[:500],
            "authors": [a.get("name") for a in _list(e.get("authors")) if isinstance(a, dict)],
            "published": e.get("published"),
            "categories": _list(e.get("categories")),
        })
    return out


def parse_nvd_cve(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    items = []
    for c in _list(payload.get("vulnerabilities")):
        if not isinstance(c, dict):
            continue
        cve = _d(c.get("cve"))
        items.append({
            "cve": cve.get("id"),
            "published": cve.get("published"),
            "descriptions": [
                d.get("value") for d in _list(cve.get("descriptions"))
                if isinstance(d, dict) and d.get("lang") == "en"
            ],
            "metrics": _d(cve.get("metrics")),
            "references_count": len(_list(cve.get("references"))),
        })
    return {"totalResults": payload.get("totalResults"), "items": items}


def parse_github_advisories(payload: Any) -> list[dict[str, Any]]:
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
                    "package": _d(v.get("package")).get("name"),
                    "ecosystem": _d(v.get("package")).get("ecosystem"),
                    "vulnerable_version_range": v.get("vulnerable_version_range"),
                }
                for v in (a.get("vulnerabilities") or [])
                if isinstance(v, dict)
            ],
        }
        for a in payload if isinstance(a, dict)
    ]


def parse_blockchain_btc(payload: Any) -> dict[str, Any]:
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
            for t in _list(payload.get("txs"))[:10]
            if isinstance(t, dict)
        ],
    }


def parse_blockstream(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    chain = _d(payload.get("chain_stats"))
    return {
        "address": payload.get("address"),
        "chain_stats": {
            "funded_txo_count": chain.get("funded_txo_count"),
            "spent_txo_count": chain.get("spent_txo_count"),
            "funded_txo_sum": chain.get("funded_txo_sum"),
            "spent_txo_sum": chain.get("spent_txo_sum"),
        },
        "mempool_stats": _d(payload.get("mempool_stats")),
    }


def parse_ethplorer(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "address": payload.get("address"),
        "ETH": _d(payload.get("ETH")).get("balance"),
        "countTxs": payload.get("countTxs"),
        "tokens": [
            {"symbol": _d(t.get("tokenInfo")).get("symbol"),
             "name": _d(t.get("tokenInfo")).get("name"),
             "balance": t.get("balance")}
            for t in _list(payload.get("tokens"))
            if isinstance(t, dict)
        ],
    }


def parse_microlink(payload: Any) -> dict[str, Any]:
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


def parse_github_user(payload: Any) -> dict[str, Any]:
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


def parse_github_search(payload: Any) -> list[dict[str, Any]]:
    items = _list(_d(payload).get("items"))
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


def parse_reddit(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    data = _d(payload.get("data"))
    if "children" in data:
        # listing
        children = _list(data.get("children"))
        return {
            "kind": "listing",
            "count": len(children),
            "items": [
                (_d(c.get("data")).get("title"),
                 _d(c.get("data")).get("url"),
                 _d(c.get("data")).get("subreddit"),
                 _d(c.get("data")).get("created_utc"))
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


def parse_mastodon(payload: Any) -> list[dict[str, Any]]:
    accounts = _list(_d(payload).get("accounts"))
    return [
        {
            "id": a.get("id"),
            "username": a.get("username"),
            "display_name": a.get("display_name"),
            "url": a.get("url"),
            "instance": _text(a.get("url")).split("/@")[-1].split("/")[0] if _text(a.get("url")) else None,
            "followers_count": a.get("followers_count"),
            "note": re.sub("<.*?>", "", _text(a.get("note")))[:200],
        }
        for a in accounts if isinstance(a, dict)
    ]


def parse_keybase(payload: Any) -> dict[str, Any]:
    them = _list(_d(payload).get("them"))
    if not them:
        return {"error": "no result"}
    p = _d(them[0])
    proofs = _d(p.get("proofs_summary"))
    basics = _d(p.get("basics"))
    profile = _d(p.get("profile"))
    primary_keys = _d(p.get("public_keys")).get("primary") or []
    return {
        "username": basics.get("username"),
        "full_name": profile.get("full_name"),
        "bio": profile.get("bio"),
        "location": profile.get("location"),
        "twitter": _first_dict(proofs.get("twitter")).get("service_url"),
        "github": _first_dict(proofs.get("github")).get("service_url"),
        "public_keys": [
            {"bundle": k.get("bundle"), "key_fingerprint": k.get("key_fingerprint")}
            for k in primary_keys
            if isinstance(k, dict)
        ],
        "devices": [
            {"name": _d(d.get("device")).get("name"), "type": _d(d.get("device")).get("type")}
            for d in (p.get("devices") or [])
            if isinstance(d, dict)
        ],
    }


def parse_hackernews(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or "id" not in payload:
        return {"error": "no result"}
    return {
        "id": payload.get("id"),
        "created": payload.get("created"),
        "karma": payload.get("karma"),
        "about": payload.get("about"),
        "submitted_count": len(_list(payload.get("submitted"))),
    }


def parse_reddit_search(payload: Any) -> list[dict[str, Any]]:
    children = _list(_d(_d(payload).get("data")).get("children"))
    return [
        {
            "name": _d(c.get("data")).get("display_name"),
            "title": _d(c.get("data")).get("title"),
            "subscribers": _d(c.get("data")).get("subscribers"),
            "url": _d(c.get("data")).get("url"),
            "public_description": _d(c.get("data")).get("public_description"),
        }
        for c in children if isinstance(c, dict)
    ]


def parse_dev_to(payload: Any) -> dict[str, Any]:
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


def parse_text_lines(payload: Any) -> list[str]:
    """Generic: split raw_text by newlines, drop empties."""
    if isinstance(payload, dict) and "raw_text" in payload:
        return [ln for ln in _text(payload.get("raw_text")).splitlines() if ln.strip()]
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


def parse_http_headers(payload: Any) -> dict[str, str]:
    """hackertarget returns text; expect a one-line-per-header response."""
    if isinstance(payload, dict) and "raw_text" in payload:
        text = _text(payload.get("raw_text"))
    elif isinstance(payload, str):
        text = payload
    else:
        return {}
    out: dict[str, str] = {}
    for line in text.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def parse_whois_text(payload: Any) -> dict[str, str]:
    out: dict[str, str] = {}
    if isinstance(payload, dict) and "raw_text" in payload:
        text = _text(payload.get("raw_text"))
    elif isinstance(payload, str):
        text = payload
    else:
        return out
    for line in text.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


# ============================================================= SOCMINT parsers


def parse_twitter_user(payload: Any) -> dict[str, Any]:
    """Twitter/X API v2 user by username.

    Expects the v2 JSON shape: {"data": {"id": ..., "name": ..., "username": ..., ...}}
    Returns flat dict with the core profile fields.
    """
    if not isinstance(payload, dict):
        return {"error": "unexpected_response"}
    data = payload.get("data")
    if not isinstance(data, dict):
        errors = _list(payload.get("errors"))
        if errors:
            first = errors[0]
            detail = first.get("detail", "unknown") if isinstance(first, dict) else str(first)
            return {"error": "not_found", "detail": detail}
        return {"error": "not_found"}
    metrics = _d(data.get("public_metrics"))
    return {
        "kind": "twitter_user",
        "id": data.get("id"),
        "name": data.get("name"),
        "username": data.get("username"),
        "description": data.get("description"),
        "location": data.get("location"),
        "verified": bool(data.get("verified", False)),
        "followers_count": int(metrics.get("followers_count", 0) or 0),
        "following_count": int(metrics.get("following_count", 0) or 0),
        "tweet_count": int(metrics.get("tweet_count", 0) or 0),
        "listed_count": int(metrics.get("listed_count", 0) or 0),
        "created_at": data.get("created_at"),
        "profile_image_url": data.get("profile_image_url"),
        "url": data.get("url"),
        "protected": bool(data.get("protected", False)),
    }


def parse_youtube_user(payload: Any) -> dict[str, Any]:
    """YouTube Data API v3 channel by handle.

    Expects: {"items": [{"id": ..., "snippet": {...}, "statistics": {...}}]}
    Returns a flat profile dict with channel metadata.
    """
    if not isinstance(payload, dict):
        return {"error": "unexpected_response"}
    items = payload.get("items") or []
    if not items or not isinstance(items, list):
        return {"error": "not_found"}
    channel = items[0]
    if not isinstance(channel, dict):
        return {"error": "not_found"}
    snippet = channel.get("snippet") or {}
    statistics = channel.get("statistics") or {}
    topic_details = channel.get("topicDetails") or {}
    branding = channel.get("brandingSettings") or {}
    image = branding.get("image") or {} if isinstance(branding, dict) else {}
    return {
        "kind": "youtube_channel",
        "channel_id": channel.get("id"),
        "title": snippet.get("title"),
        "description": (snippet.get("description") or "")[:500],
        "custom_url": snippet.get("customUrl"),
        "published_at": snippet.get("publishedAt"),
        "country": snippet.get("country"),
        "view_count": int(statistics.get("viewCount", 0) or 0),
        "subscriber_count": int(statistics.get("subscriberCount", 0) or 0),
        "video_count": int(statistics.get("videoCount", 0) or 0),
        "avatar_url": (snippet.get("thumbnails") or {}).get("default", {}).get("url") if isinstance(snippet.get("thumbnails"), dict) else None,
        "banner_url": image.get("bannerExternalUrl"),
        "topic_ids": topic_details.get("topicIds", []) or [],
        "keywords": (branding.get("channel") or {}).get("keywords", "").split("\"") if isinstance(branding.get("channel"), dict) else None,
    }


def parse_twitch_user(payload: Any) -> dict[str, Any]:
    """Twitch Helix API user by login.

    Expects: {"data": [{"id": ..., "login": ..., "display_name": ..., ...}]}
    Returns a flat profile dict with core Twitch metadata.
    """
    if not isinstance(payload, dict):
        return {"error": "unexpected_response"}
    data_list = payload.get("data")
    if not isinstance(data_list, list) or not data_list:
        # Check for error response
        error = payload.get("error")
        if error:
            return {"error": "api_error", "detail": payload.get("message", str(error))}
        return {"error": "not_found"}
    user = data_list[0]
    if not isinstance(user, dict):
        return {"error": "not_found"}
    return {
        "kind": "twitch_user",
        "id": user.get("id"),
        "login": user.get("login"),
        "display_name": user.get("display_name"),
        "description": user.get("description"),
        "type": user.get("type"),
        "broadcaster_type": user.get("broadcaster_type"),
        "view_count": int(user.get("view_count", 0) or 0),
        "created_at": user.get("created_at"),
        "offline_image_url": user.get("offline_image_url"),
        "profile_image_url": user.get("profile_image_url"),
    }


def parse_discord_discovery(payload: Any) -> dict[str, Any]:
    """Discord server discovery via discords.com API.

    Expected shape: a list of server dicts with name, description,
    member_count, etc. Or a dict with a 'results' or 'servers' key.
    """
    if payload is None:
        return {"results": [], "total": 0}
    if isinstance(payload, list):
        servers = [_normalise_discord_server(s) for s in payload if isinstance(s, dict)]
        return {"results": servers, "total": len(servers)}
    if isinstance(payload, dict):
        # Try common response shapes
        servers_raw = payload.get("results") or payload.get("servers") or payload.get("guilds") or []
        if isinstance(servers_raw, list):
            servers = [_normalise_discord_server(s) for s in servers_raw if isinstance(s, dict)]
            return {"results": servers, "total": len(servers)}
    return {"results": [], "total": 0}


def _normalise_discord_server(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalise a single raw Discord server dict into a standard shape."""
    return {
        "kind": "discord_server",
        "id": str(raw.get("id") or raw.get("guild_id") or ""),
        "name": raw.get("name"),
        "description": raw.get("description") or raw.get("short_description"),
        "approximate_member_count": int(raw.get("approximate_member_count") or raw.get("members", 0) or 0),
        "approximate_presence_count": int(raw.get("approximate_presence_count") or raw.get("online", 0) or 0),
        "vanity_url_code": raw.get("vanity_url_code"),
        "features": raw.get("features", []) or [],
        "icon_url": (raw.get("icon") or "") if isinstance(raw.get("icon"), str) and raw.get("icon").startswith("http") else None,
    }


# ------------------------------------------------------ aerospace parsers ----
def parse_celestrak_tle(payload: Any) -> dict[str, Any]:
    """CelesTrak GP three-line TLE catalog (text or ``{"raw_text": ...}``)."""
    from .aerospace import parse_tle_catalog

    satellites = parse_tle_catalog(payload)
    return {"satellites": satellites, "count": len(satellites)}


def parse_opensky_states(payload: Any) -> dict[str, Any]:
    """OpenSky Network state vectors -> common aircraft records."""
    from .aerospace import normalize_opensky_states

    aircraft = normalize_opensky_states(payload)
    return {"aircraft": aircraft, "count": len(aircraft)}


def parse_adsblol_aircraft(payload: Any) -> dict[str, Any]:
    """adsb.lol v2 aircraft snapshot -> common aircraft records."""
    from .aerospace import normalize_adsblol_aircraft

    aircraft = normalize_adsblol_aircraft(payload)
    return {"aircraft": aircraft, "count": len(aircraft)}


def parse_opensky_track(payload: Any) -> dict[str, Any]:
    """OpenSky Network aircraft track with waypoints."""
    from .aerospace import normalize_opensky_track

    return normalize_opensky_track(payload)


def parse_adsbdb(payload: Any) -> dict[str, Any]:
    """adsbdb aircraft or callsign flight route."""
    from .aerospace import normalize_adsbdb

    return normalize_adsbdb(payload)


def parse_launch_library(payload: Any) -> dict[str, Any]:
    """Launch Library 2 launches with pad coordinates when present."""
    from .aerospace import normalize_launch_library

    launches = normalize_launch_library(payload)
    return {"launches": launches, "count": len(launches)}


def parse_hexdb_aircraft(payload: Any) -> dict[str, Any]:
    """hexdb.io aircraft record by ICAO address (registration, type, owner)."""
    from .aviation import normalize_hexdb_aircraft

    aircraft = normalize_hexdb_aircraft(payload)
    return {"aircraft": aircraft, "count": 1 if aircraft else 0}


def parse_hexdb_route(payload: Any) -> dict[str, Any]:
    """hexdb.io flight route by callsign (origin and destination)."""
    from .aviation import normalize_hexdb_route

    return normalize_hexdb_route(payload)


# ------------------------------------------- keyless origins parsers (v1.5)
def _to_float(value: Any) -> float | None:
    """Return `value` as float, or None when it is not numeric."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: Any) -> int | None:
    """Return `value` as int, or None when it is not numeric."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _first_text(items: Any, key: str) -> str:
    """First non-empty `key` across a list of dicts, as text."""
    for raw in _list(items):
        val = _text(_d(raw).get(key))
        if val:
            return val
    return ""


def parse_epss(payload: Any) -> dict[str, Any]:
    """FIRST EPSS exploit-prediction score for a CVE (``data[0]``)."""
    empty: dict[str, Any] = {"cve": None, "epss": None, "percentile": None, "date": None}
    rec = _first_dict(_d(payload).get("data"))
    if not rec:
        return empty
    return {
        "cve": rec.get("cve"),
        "epss": _to_float(rec.get("epss")),
        "percentile": _to_float(rec.get("percentile")),
        "date": rec.get("date"),
    }


def parse_osv(payload: Any) -> dict[str, Any]:
    """OSV.dev vulnerability record: aliases, severities, affected packages."""
    out: dict[str, Any] = {
        "id": None, "summary": "", "published": None, "modified": None,
        "aliases": [], "cvss": "", "severity": "", "ecosystems": [],
        "packages": [], "repos": [], "fixed": [], "references": [], "count": 0,
    }
    if not isinstance(payload, dict) or not payload.get("id"):
        return out
    out["id"] = payload.get("id")
    out["summary"] = _text(payload.get("summary"))[:400]
    out["published"] = payload.get("published")
    out["modified"] = payload.get("modified")
    out["aliases"] = [str(a) for a in _list(payload.get("aliases"))[:20]]
    sev = _first_dict(payload.get("severity"))
    out["cvss"] = _text(sev.get("score"))
    out["severity"] = _text(sev.get("type"))
    for raw_aff in _list(payload.get("affected"))[:20]:
        aff = _d(raw_aff)
        pkg = _d(aff.get("package"))
        eco = _text(pkg.get("ecosystem"))
        name = _text(pkg.get("name"))
        if eco and eco not in out["ecosystems"]:
            out["ecosystems"].append(eco)
        if name:
            out["packages"].append(f"{eco}/{name}" if eco else name)
        for raw_range in _list(aff.get("ranges")):
            rng = _d(raw_range)
            repo = _text(rng.get("repo"))
            if repo and repo not in out["repos"]:
                out["repos"].append(repo)
            for raw_ev in _list(rng.get("events")):
                fixed = _text(_d(raw_ev).get("fixed"))
                if fixed and fixed not in out["fixed"]:
                    out["fixed"].append(fixed)
    for raw_ref in _list(payload.get("references"))[:20]:
        url = _text(_d(raw_ref).get("url"))
        if url:
            out["references"].append(url)
    out["count"] = len(out["packages"])
    return out


def _cvss_from_containers(containers: Any) -> tuple[str, str, float | None]:
    """Return (vector, severity, base score) from a CVE 5.x metrics list."""
    for raw_metric in _list(containers):
        for key, val in _d(raw_metric).items():
            if not key.lower().startswith("cvss"):
                continue
            cvss = _d(val)
            if not cvss:
                continue
            return (
                _text(cvss.get("vectorString")),
                _text(cvss.get("baseSeverity")),
                _to_float(cvss.get("baseScore")),
            )
    return "", "", None


def parse_cve_record(payload: Any) -> dict[str, Any]:
    """CVE.org CVE 5.x record (cveMetadata + containers.cna)."""
    out: dict[str, Any] = {
        "cve_id": None, "state": None, "assigner": None, "published": None,
        "updated": None, "title": "", "description": "", "cvss_vector": "",
        "severity": "", "cvss_score": None, "cwe": [], "products": [],
        "versions": [], "references": [], "count": 0,
    }
    if not isinstance(payload, dict):
        return out
    meta = _d(payload.get("cveMetadata"))
    cna = _d(_d(payload.get("containers")).get("cna"))
    if not meta and not cna:
        return out
    out["cve_id"] = meta.get("cveId")
    out["state"] = meta.get("state")
    out["assigner"] = meta.get("assignerShortName") or meta.get("assignerOrgId")
    out["published"] = meta.get("datePublished")
    out["updated"] = meta.get("dateUpdated")
    out["title"] = _text(cna.get("title"))[:300]
    out["description"] = _first_text(cna.get("descriptions"), "value")[:600]
    vector, severity, score = _cvss_from_containers(cna.get("metrics"))
    out["cvss_vector"], out["severity"], out["cvss_score"] = vector, severity, score
    for raw_pt in _list(cna.get("problemTypes"))[:10]:
        for raw_desc in _list(_d(raw_pt).get("descriptions")):
            cwe = _text(_d(raw_desc).get("cweId")) or _text(_d(raw_desc).get("description"))
            if cwe and cwe not in out["cwe"]:
                out["cwe"].append(cwe)
    for raw_aff in _list(cna.get("affected"))[:20]:
        aff = _d(raw_aff)
        product = _text(aff.get("product")) or _text(aff.get("packageName"))
        vendor = _text(aff.get("vendor"))
        if product:
            label = f"{vendor}/{product}" if vendor else product
            if label not in out["products"]:
                out["products"].append(label)
        for raw_ver in _list(aff.get("versions"))[:20]:
            ver = _text(_d(raw_ver).get("version"))
            if ver and ver not in out["versions"]:
                out["versions"].append(ver)
    for raw_ref in _list(cna.get("references"))[:20]:
        url = _text(_d(raw_ref).get("url"))
        if url:
            out["references"].append(url)
    out["count"] = len(out["products"])
    return out


def parse_ransomware_live(payload: Any) -> dict[str, Any]:
    """ransomware.live recent-victims feed (list of leak-site claims)."""
    out: dict[str, Any] = {
        "count": 0, "groups": [], "countries": [], "sectors": [], "victims": [],
    }
    victims = _list(payload)
    if not victims:
        return out
    for raw in victims[:60]:
        item = _d(raw)
        victim = {
            "group": _text(item.get("group")),
            "victim": _text(item.get("victim")) or _text(item.get("post_title")),
            "country": _text(item.get("country")),
            "sector": _text(item.get("activity")),
            "date": _text(item.get("attackdate"))[:10],
            "claim_url": _text(item.get("claim_url")),
            "description": _text(item.get("description"))[:300],
        }
        out["victims"].append(victim)
        for bucket, key in (("groups", "group"), ("countries", "country"), ("sectors", "sector")):
            val = victim[key]
            if val and val not in out[bucket]:
                out[bucket].append(val)
    out["count"] = len(victims)
    return out


def parse_yaraify(payload: Any) -> dict[str, Any]:
    """abuse.ch YARAify sample search result."""
    out: dict[str, Any] = {
        "status": "", "searched_scope": "", "count": 0, "samples": [],
    }
    body = _d(payload)
    out["status"] = _text(body.get("query_status"))
    info = _d(body.get("query_info"))
    out["searched_scope"] = _text(info.get("search_scope"))
    out["count"] = _to_int(info.get("result_count")) or 0
    for raw in _list(body.get("data"))[:20]:
        item = _d(raw)
        out["samples"].append({
            "sha256": _text(item.get("sha256_hash")),
            "md5": _text(item.get("md5_hash")),
            "sha1": _text(item.get("sha1_hash")),
            "mime_type": _text(item.get("mime_type")),
            "file_size": _to_int(item.get("file_size")),
            "first_seen": _text(item.get("first_seen")),
            "last_seen": _text(item.get("last_seen")),
            "imphash": _text(item.get("imphash")),
        })
    return out


def parse_sans_isc_ip(payload: Any) -> dict[str, Any]:
    """SANS ISC honeypot record for an IP (attacks, ASN, threat feeds)."""
    out: dict[str, Any] = {
        "ip": None, "attacks": None, "maxrisk": None, "asn": None,
        "as_name": None, "as_country": None, "network": None,
        "abuse_contact": None, "comment": "", "threat_feeds": [],
        "first_seen": None, "last_seen": None,
    }
    record = _d(_d(payload).get("ip"))
    if not record:
        return out
    out["ip"] = record.get("number")
    out["attacks"] = _to_int(record.get("attacks"))
    out["maxrisk"] = _to_int(record.get("maxrisk"))
    out["asn"] = record.get("as")
    out["as_name"] = record.get("asname")
    out["as_country"] = record.get("ascountry")
    out["network"] = record.get("network")
    out["abuse_contact"] = record.get("asabusecontact")
    out["comment"] = _text(record.get("comment"))[:300]
    out["first_seen"] = record.get("mindate")
    out["last_seen"] = record.get("maxdate")
    for name, raw in _d(record.get("threatfeeds")).items():
        seen = _d(raw)
        out["threat_feeds"].append({
            "name": _text(name),
            "first_seen": _text(seen.get("firstseen")),
            "last_seen": _text(seen.get("lastseen")),
        })
    return out


def parse_ip_guide(payload: Any) -> dict[str, Any]:
    """ip.guide network object (cidr, autonomous system, location)."""
    out: dict[str, Any] = {
        "ip": None, "cidr": None, "range_start": None, "range_end": None,
        "asn": None, "as_name": "", "organization": "", "as_country": "",
        "rir": "", "city": None, "country": "", "timezone": "", "latitude": None,
        "longitude": None,
    }
    body = _d(payload)
    if not body.get("ip"):
        return out
    net = _d(body.get("network"))
    hosts = _d(net.get("hosts"))
    asn = _d(net.get("autonomous_system"))
    loc = _d(body.get("location"))
    out.update({
        "ip": body.get("ip"),
        "cidr": net.get("cidr"),
        "range_start": hosts.get("start"),
        "range_end": hosts.get("end"),
        "asn": asn.get("asn"),
        "as_name": _text(asn.get("name")),
        "organization": _text(asn.get("organization")),
        "as_country": _text(asn.get("country")),
        "rir": _text(asn.get("rir")),
        "city": loc.get("city"),
        "country": _text(loc.get("country")),
        "timezone": _text(loc.get("timezone")),
        "latitude": _to_float(loc.get("latitude")),
        "longitude": _to_float(loc.get("longitude")),
    })
    return out


def parse_dbip_ip(payload: Any) -> dict[str, Any]:
    """DB-IP free geolocation record for one IP."""
    out: dict[str, Any] = {
        "ip": None, "continent": "", "country": "", "country_code": "",
        "state": "", "city": "", "latitude": None, "longitude": None,
    }
    body = _d(payload)
    if not body.get("ipAddress"):
        return out
    out.update({
        "ip": body.get("ipAddress"),
        "continent": _text(body.get("continentName")),
        "country": _text(body.get("countryName")),
        "country_code": _text(body.get("countryCode")),
        "state": _text(body.get("stateProv")),
        "city": _text(body.get("city")),
        "latitude": _to_float(body.get("latitude")),
        "longitude": _to_float(body.get("longitude")),
    })
    return out


def parse_geojs_ip(payload: Any) -> dict[str, Any]:
    """geojs.io IP geolocation/ASN record."""
    out: dict[str, Any] = {
        "ip": None, "asn": None, "organization": "", "country": "",
        "country_code": "", "region": "", "city": "", "latitude": None,
        "longitude": None, "timezone": "", "accuracy": None,
    }
    body = _d(payload)
    if not body.get("ip"):
        return out
    out.update({
        "ip": body.get("ip"),
        "asn": _to_int(body.get("asn")),
        "organization": _text(body.get("organization_name")) or _text(body.get("organization")),
        "country": _text(body.get("country")),
        "country_code": _text(body.get("country_code")),
        "region": _text(body.get("region")),
        "city": _text(body.get("city")),
        "latitude": _to_float(body.get("latitude")),
        "longitude": _to_float(body.get("longitude")),
        "timezone": _text(body.get("timezone")),
        "accuracy": _to_int(body.get("accuracy")),
    })
    return out


def parse_ipapi_is(payload: Any) -> dict[str, Any]:
    """ipapi.is record: company, ASN, flags and location."""
    out: dict[str, Any] = {
        "ip": None, "asn": "", "company": "", "city": "", "region": "",
        "country": "", "latitude": None, "longitude": None, "timezone": "",
        "is_datacenter": None, "is_tor": None, "is_proxy": None, "is_abuser": None,
    }
    body = _d(payload)
    if not body.get("ip"):
        return out
    out.update({
        "ip": body.get("ip"),
        "asn": _text(body.get("asn")),
        "company": _text(body.get("company")),
        "city": _text(body.get("city")),
        "region": _text(body.get("region")),
        "country": _text(body.get("country")),
        "latitude": _to_float(body.get("lat")),
        "longitude": _to_float(body.get("lon")),
        "timezone": _text(body.get("timezone")),
        "is_datacenter": body.get("is_datacenter"),
        "is_tor": body.get("is_tor"),
        "is_proxy": body.get("is_proxy"),
        "is_abuser": body.get("is_abuser"),
    })
    return out


def parse_maclookup(payload: Any) -> dict[str, Any]:
    """maclookup.app OUI record for a MAC address / prefix."""
    out: dict[str, Any] = {
        "found": False, "mac_prefix": None, "company": "", "address": "",
        "country": "", "block_start": None, "block_end": None, "block_type": "",
        "updated": None, "is_private": None,
    }
    body = _d(payload)
    if not body:
        return out
    out.update({
        "found": bool(body.get("found")),
        "mac_prefix": body.get("macPrefix"),
        "company": _text(body.get("company")),
        "address": _text(body.get("address"))[:200],
        "country": _text(body.get("country")),
        "block_start": body.get("blockStart"),
        "block_end": body.get("blockEnd"),
        "block_type": _text(body.get("blockType")),
        "updated": body.get("updated"),
        "is_private": body.get("isPrivate"),
    })
    return out


def parse_peeringdb_net(payload: Any) -> dict[str, Any]:
    """PeeringDB network record(s) for an ASN."""
    out: dict[str, Any] = {
        "asn": None, "name": "", "aka": "", "website": "", "looking_glass": "",
        "irr_as_set": "", "policy_general": "", "type": "", "org_id": None,
        "ix_count": 0, "netixlan_count": 0, "count": 0,
    }
    records = _list(_d(payload).get("data"))
    net = _first_dict(records)
    if not net:
        return out
    out.update({
        "asn": net.get("asn"),
        "name": _text(net.get("name")),
        "aka": _text(net.get("aka"))[:200],
        "website": _text(net.get("website")),
        "looking_glass": _text(net.get("looking_glass")),
        "irr_as_set": _text(net.get("irr_as_set")),
        "policy_general": _text(net.get("policy_general")),
        "type": _text(net.get("info_type")),
        "org_id": net.get("org_id"),
        "ix_count": _to_int(net.get("ix_count")) or 0,
        "netixlan_count": _to_int(net.get("netixlan_count")) or 0,
        "count": len(records),
    })
    return out


def parse_tranco_rank(payload: Any) -> dict[str, Any]:
    """Tranco list rank history for a domain (latest first)."""
    out: dict[str, Any] = {"rank": None, "date": None, "history": [], "count": 0}
    ranks = _list(_d(payload).get("ranks"))
    if not ranks:
        return out
    latest = _d(ranks[0])
    out["rank"] = _to_int(latest.get("rank"))
    out["date"] = latest.get("date")
    for raw in ranks[:30]:
        item = _d(raw)
        out["history"].append({"date": item.get("date"), "rank": _to_int(item.get("rank"))})
    out["count"] = len(ranks)
    return out


def parse_hudsonrock(payload: Any) -> dict[str, Any]:
    """Hudson Rock Cavalier infostealer exposure for an email/username."""
    out: dict[str, Any] = {
        "message": "", "stealer_count": 0, "corporate_services": 0,
        "user_services": 0, "first_compromised": None, "last_compromised": None,
        "computers": [], "operating_systems": [], "malware_paths": [],
        "antiviruses": [], "ip_prefixes": [],
    }
    body = _d(payload)
    message = _text(body.get("message"))
    stealers = _list(body.get("stealers"))
    if not body or (not message and not stealers):
        return out
    out["message"] = message[:400]
    out["stealer_count"] = len(stealers)
    dates: list[str] = []
    for raw in stealers[:20]:
        item = _d(raw)
        out["corporate_services"] += _to_int(item.get("total_corporate_services")) or 0
        out["user_services"] += _to_int(item.get("total_user_services")) or 0
        date = _text(item.get("date_compromised"))
        if date:
            dates.append(date)
        for bucket, key in (
            ("computers", "computer_name"),
            ("operating_systems", "operating_system"),
            ("malware_paths", "malware_path"),
            ("ip_prefixes", "ip"),
        ):
            val = _text(item.get(key))
            if val and val != "Not Found" and val not in out[bucket] and len(out[bucket]) < 10:
                out[bucket].append(val)
        for av in _list(item.get("antiviruses")):
            av_text = _text(av)
            if av_text and av_text not in out["antiviruses"]:
                out["antiviruses"].append(av_text)
    if dates:
        out["first_compromised"] = min(dates)[:10]
        out["last_compromised"] = max(dates)[:10]
    return out


def parse_disify(payload: Any) -> dict[str, Any]:
    """disify.com email deliverability/disposable record."""
    out: dict[str, Any] = {
        "format": None, "domain": "", "disposable": None, "dns": None,
        "whitelist": None, "free": None, "role": None, "gravatar": None,
    }
    body = _d(payload)
    if not body:
        return out
    out.update({
        "format": body.get("format"),
        "domain": _text(body.get("domain")),
        "disposable": body.get("disposable"),
        "dns": body.get("dns"),
        "whitelist": body.get("whitelist"),
        "free": body.get("free"),
        "role": body.get("role"),
        "gravatar": body.get("gravatar"),
    })
    return out


def parse_gravatar(payload: Any) -> dict[str, Any]:
    """Gravatar profile entry for an md5/sha256 hash (public JSON)."""
    out: dict[str, Any] = {
        "found": False, "hash": None, "display_name": "", "about_me": "",
        "profile_url": "", "thumbnail_url": "", "location": "",
        "accounts": [], "urls": [],
    }
    if _text(payload) == "User not found":
        return out
    body = _d(payload)
    entry = _first_dict(body.get("entry"))
    if not entry:
        return out
    out.update({
        "found": True,
        "hash": body.get("hash") or entry.get("hash"),
        "display_name": _text(entry.get("displayName")) or _text(entry.get("name")),
        "about_me": _text(entry.get("aboutMe"))[:400],
        "profile_url": _text(entry.get("profileUrl")),
        "thumbnail_url": _text(entry.get("thumbnailUrl")),
        "location": _text(entry.get("currentLocation")),
    })
    for raw in _list(entry.get("accounts"))[:20]:
        acc = _d(raw)
        out["accounts"].append({
            "shortname": _text(acc.get("shortname")),
            "username": _text(acc.get("username")),
            "url": _text(acc.get("url")),
        })
    for raw in _list(entry.get("urls"))[:20]:
        url = _text(_d(raw).get("value"))
        if url:
            out["urls"].append(url)
    return out


def parse_cidr_ranges(payload: Any) -> dict[str, Any]:
    """Collect every CIDR in a provider IP-range document (Cloudflare/GCP)."""
    out: dict[str, Any] = {"count": 0, "cidrs": []}
    found: list[str] = []

    def _walk(node: Any, depth: int = 0) -> None:
        if depth > 6 or len(found) >= 400:
            return
        if isinstance(node, dict):
            for value in node.values():
                _walk(value, depth + 1)
        elif isinstance(node, list):
            for value in node:
                _walk(value, depth + 1)
        elif isinstance(node, str) and "/" in node and not node.startswith("http"):
            head, _, tail = node.partition("/")
            if tail.isdigit() and head and all(c in "0123456789abcdefABCDEF.:" for c in head):
                found.append(node)

    _walk(payload)
    out["cidrs"] = found
    out["count"] = len(found)
    return out


def parse_hstspreload(payload: Any) -> dict[str, Any]:
    """hstspreload.org status/preloadable response."""
    out: dict[str, Any] = {
        "domain": "", "status": "", "bulk": None, "preloaded_domain": "",
        "errors": [], "error_count": 0,
    }
    body = _d(payload)
    if not body:
        return out
    out.update({
        "domain": _text(body.get("name")) or _text(body.get("domain")),
        "status": _text(body.get("status")),
        "bulk": body.get("bulk"),
        "preloaded_domain": _text(body.get("preloadedDomain")),
    })
    for raw in _list(body.get("errors"))[:20]:
        err = _d(raw)
        out["errors"].append({
            "code": _text(err.get("code")),
            "summary": _text(err.get("summary"))[:200],
        })
    out["error_count"] = len(_list(body.get("errors")))
    return out


def parse_ssl_labs(payload: Any) -> dict[str, Any]:
    """Qualys SSL Labs analyze response (grade and endpoints)."""
    out: dict[str, Any] = {
        "host": "", "status": "", "grade": "", "endpoint_count": 0,
        "endpoints": [], "has_warnings": None, "test_time": None,
    }
    body = _d(payload)
    if not body:
        return out
    out["host"] = _text(body.get("host"))
    out["status"] = _text(body.get("status"))
    out["test_time"] = body.get("testTime")
    endpoints = _list(body.get("endpoints"))
    out["endpoint_count"] = len(endpoints)
    grades: list[str] = []
    for raw in endpoints[:10]:
        ep = _d(raw)
        grade = _text(ep.get("grade"))
        if grade:
            grades.append(grade)
        out["endpoints"].append({
            "ip": _text(ep.get("ipAddress")),
            "grade": grade,
            "has_warnings": ep.get("hasWarnings"),
            "status_message": _text(ep.get("statusMessage"))[:200],
        })
    if grades:
        # Worst grade wins: sorting descending puts "B" before "A".
        out["grade"] = sorted(grades, reverse=True)[0]
    out["has_warnings"] = any(bool(_d(ep).get("hasWarnings")) for ep in endpoints)
    return out


def parse_bluesky_profile(payload: Any) -> dict[str, Any]:
    """AT Protocol (Bluesky) public profile."""
    out: dict[str, Any] = {
        "did": None, "handle": None, "display_name": "", "description": "",
        "followers": None, "follows": None, "posts": None, "created_at": None,
        "avatar": "", "labels": [],
    }
    body = _d(payload)
    if not body.get("did"):
        return out
    out.update({
        "did": body.get("did"),
        "handle": body.get("handle"),
        "display_name": _text(body.get("displayName"))[:200],
        "description": _text(body.get("description"))[:600],
        "followers": _to_int(body.get("followersCount")),
        "follows": _to_int(body.get("followsCount")),
        "posts": _to_int(body.get("postsCount")),
        "created_at": body.get("createdAt"),
        "avatar": _text(body.get("avatar")),
    })
    for raw in _list(body.get("labels"))[:10]:
        val = _text(_d(raw).get("val"))
        if val:
            out["labels"].append(val)
    return out


def parse_lemmy_user(payload: Any) -> dict[str, Any]:
    """Lemmy (v3 API) public user profile."""
    out: dict[str, Any] = {
        "username": None, "display_name": "", "bio": "", "matrix_user": "",
        "posts": 0, "comments": 0, "is_admin": None, "published": None,
        "actor_id": "", "avatar": "",
    }
    body = _d(payload)
    if body.get("error"):
        return out
    person = _d(_d(body.get("person_view")).get("person")) or _d(body.get("person"))
    if not person.get("name"):
        return out
    counts = _d(_d(body.get("person_view")).get("counts")) or _d(body.get("counts"))
    out.update({
        "username": person.get("name"),
        "display_name": _text(person.get("display_name"))[:200],
        "bio": _text(person.get("bio"))[:600],
        "matrix_user": _text(person.get("matrix_user_id")),
        "posts": _to_int(counts.get("post_count")) or 0,
        "comments": _to_int(counts.get("comment_count")) or 0,
        "is_admin": _d(body.get("person_view")).get("is_admin"),
        "published": person.get("published"),
        "actor_id": _text(person.get("actor_id")),
        "avatar": _text(person.get("avatar")),
    })
    return out


def parse_gitlab_user(payload: Any) -> dict[str, Any]:
    """GitLab v4 user search result (first match)."""
    out: dict[str, Any] = {
        "id": None, "username": None, "name": "", "state": "", "bio": "",
        "location": "", "public_email": "", "website_url": "", "created_at": None,
        "followers": None, "count": 0,
    }
    users = _list(payload)
    user = _first_dict(users)
    if not user:
        return out
    out.update({
        "id": user.get("id"),
        "username": user.get("username"),
        "name": _text(user.get("name"))[:200],
        "state": _text(user.get("state")),
        "bio": _text(user.get("bio"))[:600],
        "location": _text(user.get("location")),
        "public_email": _text(user.get("public_email")),
        "website_url": _text(user.get("website_url")),
        "created_at": user.get("created_at"),
        "followers": _to_int(user.get("followers")),
        "count": len(users),
    })
    return out


def parse_forgejo_user(payload: Any) -> dict[str, Any]:
    """Gitea/Forgejo (Codeberg) public user record."""
    out: dict[str, Any] = {
        "id": None, "login": None, "full_name": "", "email": "", "website": "",
        "location": "", "bio": "", "followers": 0, "following": 0, "created": None,
        "is_admin": None,
    }
    body = _d(payload)
    if not body.get("login"):
        return out
    out.update({
        "id": body.get("id"),
        "login": body.get("login"),
        "full_name": _text(body.get("full_name"))[:200],
        "email": _text(body.get("email")),
        "website": _text(body.get("website")),
        "location": _text(body.get("location")),
        "bio": _text(body.get("bio") or body.get("description"))[:600],
        "followers": _to_int(body.get("followers_count")) or 0,
        "following": _to_int(body.get("following_count")) or 0,
        "created": body.get("created"),
        "is_admin": body.get("is_admin"),
    })
    return out


def parse_openlibrary(payload: Any) -> dict[str, Any]:
    """Open Library search response."""
    out: dict[str, Any] = {"count": 0, "works": []}
    body = _d(payload)
    out["count"] = _to_int(body.get("numFound")) or 0
    for raw in _list(body.get("docs"))[:10]:
        doc = _d(raw)
        out["works"].append({
            "key": _text(doc.get("key")),
            "title": _text(doc.get("title"))[:250],
            "authors": [_text(a) for a in _list(doc.get("author_name"))[:5]],
            "first_publish_year": _to_int(doc.get("first_publish_year")),
            "editions": _to_int(doc.get("edition_count")),
            "subjects": [_text(s) for s in _list(doc.get("subject"))[:5]],
        })
    return out


def parse_pubmed(payload: Any) -> dict[str, Any]:
    """NCBI E-utilities esearch response."""
    out: dict[str, Any] = {"count": 0, "pmids": [], "query_translation": ""}
    body = _d(payload)
    result = _d(body.get("esearchresult"))
    if not result:
        return out
    out["count"] = _to_int(result.get("count")) or 0
    out["pmids"] = [_text(p) for p in _list(result.get("idlist"))[:20]]
    out["query_translation"] = _text(result.get("querytranslation"))[:300]
    return out


def parse_europepmc(payload: Any) -> dict[str, Any]:
    """Europe PMC search response."""
    out: dict[str, Any] = {"count": 0, "articles": []}
    body = _d(payload)
    out["count"] = _to_int(body.get("hitCount")) or 0
    for raw in _list(_d(body.get("resultList")).get("result"))[:10]:
        item = _d(raw)
        out["articles"].append({
            "id": _text(item.get("id")),
            "source": _text(item.get("source")),
            "doi": _text(item.get("doi")),
            "title": _text(item.get("title"))[:300],
            "authors": _text(item.get("authorString"))[:300],
            "year": _text(item.get("pubYear")),
            "journal": _text(_d(item.get("journalInfo")).get("journal", "")),
            "open_access": _text(item.get("isOpenAccess")) == "Y",
        })
    return out


def parse_doaj(payload: Any) -> dict[str, Any]:
    """DOAJ articles search response (bibjson envelope)."""
    out: dict[str, Any] = {"count": 0, "articles": []}
    body = _d(payload)
    out["count"] = _to_int(body.get("total")) or 0
    for raw in _list(body.get("results"))[:10]:
        bib = _d(_d(raw).get("bibjson"))
        journal = _d(bib.get("journal"))
        doi = ""
        for ident in _list(bib.get("identifier")):
            if _text(_d(ident).get("type")) == "doi":
                doi = _text(_d(ident).get("id"))
                break
        out["articles"].append({
            "title": _text(bib.get("title"))[:300],
            "authors": [_text(_d(a).get("name")) for a in _list(bib.get("author"))[:5]],
            "year": _text(bib.get("year")),
            "doi": doi,
            "journal": _text(journal.get("title"))[:200],
            "publisher": _text(journal.get("publisher"))[:200],
        })
    return out


def parse_gdelt(payload: Any) -> dict[str, Any]:
    """GDELT DOC 2.0 article list."""
    out: dict[str, Any] = {"count": 0, "articles": [], "domains": [], "languages": []}
    for raw in _list(_d(payload).get("articles"))[:25]:
        item = _d(raw)
        article = {
            "url": _text(item.get("url")),
            "title": _text(item.get("title"))[:300],
            "domain": _text(item.get("domain")),
            "language": _text(item.get("language")),
            "country": _text(item.get("sourcecountry")),
            "seen_date": _text(item.get("seendate")),
        }
        out["articles"].append(article)
        if article["domain"] and article["domain"] not in out["domains"]:
            out["domains"].append(article["domain"])
        if article["language"] and article["language"] not in out["languages"]:
            out["languages"].append(article["language"])
    out["count"] = len(out["articles"])
    return out


def parse_archive_org(payload: Any) -> dict[str, Any]:
    """Internet Archive advancedsearch response."""
    out: dict[str, Any] = {"count": 0, "items": []}
    body = _d(payload)
    response = _d(body.get("response"))
    out["count"] = _to_int(response.get("numFound")) or 0
    for raw in _list(response.get("docs"))[:10]:
        doc = _d(raw)
        out["items"].append({
            "identifier": _text(doc.get("identifier")),
            "title": _text(doc.get("title"))[:250],
            "creator": _text(doc.get("creator"))[:200],
            "year": _text(doc.get("year")),
            "mediatype": _text(doc.get("mediatype")),
            "url": f"https://archive.org/details/{_text(doc.get('identifier'))}",
        })
    return out


def parse_photon(payload: Any) -> dict[str, Any]:
    """Photon (Komoot) GeoJSON geocoder response."""
    out: dict[str, Any] = {"count": 0, "places": []}
    for raw in _list(_d(payload).get("features"))[:10]:
        feat = _d(raw)
        props = _d(feat.get("properties"))
        coords = _list(_d(feat.get("geometry")).get("coordinates"))
        lon = _to_float(coords[0]) if len(coords) > 0 else None
        lat = _to_float(coords[1]) if len(coords) > 1 else None
        out["places"].append({
            "name": _text(props.get("name"))[:200],
            "street": _text(props.get("street")),
            "city": _text(props.get("city")),
            "state": _text(props.get("state")),
            "country": _text(props.get("country")),
            "postcode": _text(props.get("postcode")),
            "osm_type": _text(props.get("osm_type")),
            "osm_id": props.get("osm_id"),
            "latitude": lat,
            "longitude": lon,
        })
    out["count"] = len(out["places"])
    return out


def parse_radio_browser(payload: Any) -> dict[str, Any]:
    """radio-browser.info station search list."""
    out: dict[str, Any] = {"count": 0, "stations": []}
    for raw in _list(payload)[:15]:
        item = _d(raw)
        out["stations"].append({
            "name": _text(item.get("name")).strip()[:200],
            "country": _text(item.get("country")),
            "language": _text(item.get("language")),
            "tags": _text(item.get("tags"))[:200],
            "bitrate": _to_int(item.get("bitrate")),
            "codec": _text(item.get("codec")),
            "homepage": _text(item.get("homepage")),
            "stream_url": _text(item.get("url_resolved")) or _text(item.get("url")),
            "votes": _to_int(item.get("votes")),
        })
    out["count"] = len(out["stations"])
    return out


def parse_npm_package(payload: Any) -> dict[str, Any]:
    """npm registry `/{pkg}/latest` manifest."""
    out: dict[str, Any] = {
        "name": None, "version": None, "description": "", "license": "",
        "homepage": "", "repository": "", "author": "", "dependencies": [],
        "maintainers": [], "keywords": [], "deprecated": False,
    }
    body = _d(payload)
    if not body.get("name"):
        return out
    repo = body.get("repository")
    if isinstance(repo, dict):
        repo = repo.get("url")
    author = body.get("author")
    if isinstance(author, dict):
        author = author.get("name")
    out.update({
        "name": body.get("name"),
        "version": body.get("version"),
        "description": _text(body.get("description"))[:500],
        "license": _text(body.get("license")),
        "homepage": _text(body.get("homepage")),
        "repository": _text(repo),
        "author": _text(author)[:200],
        "dependencies": sorted(_d(body.get("dependencies")).keys())[:30],
        "keywords": [_text(k) for k in _list(body.get("keywords"))[:15]],
        "deprecated": bool(body.get("deprecated")),
    })
    for raw in _list(body.get("maintainers"))[:10]:
        name = _text(_d(raw).get("name"))
        if name:
            out["maintainers"].append(name)
    return out


def parse_pypi_package(payload: Any) -> dict[str, Any]:
    """PyPI JSON API `/{pkg}/json`."""
    out: dict[str, Any] = {
        "name": None, "version": None, "summary": "", "license": "",
        "author": "", "author_email": "", "home_page": "", "project_urls": {},
        "requires_python": "", "classifiers": [], "releases": 0,
    }
    info = _d(_d(payload).get("info"))
    if not info.get("name"):
        return out
    urls = {
        str(k): _text(v)
        for k, v in _d(info.get("project_urls")).items()
        if _text(v)
    }
    out.update({
        "name": info.get("name"),
        "version": info.get("version"),
        "summary": _text(info.get("summary"))[:500],
        "license": _text(info.get("license"))[:200],
        "author": _text(info.get("author"))[:200],
        "author_email": _text(info.get("author_email")),
        "home_page": _text(info.get("home_page")),
        "project_urls": dict(list(urls.items())[:10]),
        "requires_python": _text(info.get("requires_python")),
        "classifiers": [_text(c) for c in _list(info.get("classifiers"))[:11]],
        "releases": len(_d(_d(payload).get("releases"))),
    })
    return out


def parse_dockerhub_search(payload: Any) -> dict[str, Any]:
    """Docker Hub repository search."""
    out: dict[str, Any] = {"count": 0, "repositories": []}
    body = _d(payload)
    out["count"] = _to_int(body.get("count")) or 0
    for raw in _list(body.get("results"))[:10]:
        item = _d(raw)
        out["repositories"].append({
            "name": _text(item.get("repo_name")),
            "description": _text(item.get("short_description"))[:250],
            "stars": _to_int(item.get("star_count")) or 0,
            "pulls": _to_int(item.get("pull_count")) or 0,
            "official": bool(item.get("is_official")),
            "owner": _text(item.get("repo_owner")),
        })
    return out


def parse_huggingface(payload: Any) -> dict[str, Any]:
    """Hugging Face hub model search."""
    out: dict[str, Any] = {"count": 0, "models": []}
    for raw in _list(payload)[:15]:
        item = _d(raw)
        out["models"].append({
            "id": _text(item.get("id")),
            "pipeline_tag": _text(item.get("pipeline_tag")),
            "likes": _to_int(item.get("likes")) or 0,
            "downloads": _to_int(item.get("downloads")) or 0,
            "library": _text(item.get("library_name")),
            "tags": [_text(t) for t in _list(item.get("tags"))[:10]],
            "created_at": item.get("createdAt"),
        })
    out["count"] = len(out["models"])
    return out


def parse_planespotters(payload: Any) -> dict[str, Any]:
    """Planespotters public photo API for a hex/registration."""
    out: dict[str, Any] = {"count": 0, "photos": []}
    for raw in _list(_d(payload).get("photos"))[:8]:
        item = _d(raw)
        out["photos"].append({
            "id": _text(item.get("id")),
            "link": _text(item.get("link")),
            "photographer": _text(item.get("photographer")),
            "thumbnail": _text(_d(item.get("thumbnail")).get("src")),
            "large": _text(_d(item.get("thumbnail_large")).get("src")),
        })
    out["count"] = len(out["photos"])
    return out


def parse_satnogs(payload: Any) -> dict[str, Any]:
    """SatNOGS DB satellite catalogue record(s) by NORAD id."""
    out: dict[str, Any] = {
        "count": 0, "satellites": [], "names": [], "norad_ids": [],
        "operators": [], "countries": [], "status": "",
    }
    for raw in _list(payload)[:10]:
        item = _d(raw)
        out["satellites"].append({
            "name": _text(item.get("name"))[:150],
            "norad_id": _to_int(item.get("norad_cat_id")),
            "status": _text(item.get("status")),
            "launched": _text(item.get("launched"))[:10],
            "operator": _text(item.get("operator"))[:120],
            "country": _text(item.get("country")),
            "website": _text(item.get("website")),
            "image": _text(item.get("image")),
        })
        for bucket, value in (
            ("names", _text(item.get("name"))),
            ("norad_ids", item.get("norad_cat_id")),
            ("operators", _text(item.get("operator"))),
            ("countries", _text(item.get("country"))),
        ):
            if value not in (None, "", 0) and value not in out[bucket]:
                out[bucket].append(value)
        if not out["status"]:
            out["status"] = _text(item.get("status"))
    out["count"] = len(out["satellites"])
    return out


def parse_spaceflightnews(payload: Any) -> dict[str, Any]:
    """Spaceflight News API v4 article search."""
    out: dict[str, Any] = {"count": 0, "articles": [], "sites": []}
    body = _d(payload)
    out["count"] = _to_int(body.get("count")) or 0
    for raw in _list(body.get("results"))[:10]:
        item = _d(raw)
        site = _text(item.get("news_site"))[:120]
        out["articles"].append({
            "title": _text(item.get("title"))[:300],
            "url": _text(item.get("url")),
            "published_at": _text(item.get("published_at"))[:19],
            "news_site": site,
            "summary": _text(item.get("summary"))[:300],
        })
        if site and site not in out["sites"]:
            out["sites"].append(site)
    return out


def parse_address_list(payload: Any) -> dict[str, Any]:
    """Whitespace/newline-delimited address list (OFAC SDN mirrors)."""
    if isinstance(payload, dict) and "raw_text" in payload:
        text = _text(payload.get("raw_text"))
    elif isinstance(payload, str):
        text = payload
    else:
        text = ""
    tokens = [tok.strip() for tok in text.replace("\n", " ").split(" ") if tok.strip()]
    addresses = [tok for tok in tokens if not tok.startswith(("#", ";", "//"))]
    return {"count": len(addresses), "addresses": addresses[:500]}


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
    "bgpview": parse_bgpview,
    "cisa_kev": parse_cisa_kev,
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
    # --- Recon parsers ---
    "tech_fingerprint": parse_raw_text,
    # --- SOCMINT parsers (v1.4) ---
    "twitter_user": parse_twitter_user,
    "youtube_user": parse_youtube_user,
    "twitch_user": parse_twitch_user,
    "discord_discovery": parse_discord_discovery,
    # --- Aerospace parsers (21_aerospace) ---
    "celestrak_tle": parse_celestrak_tle,
    "opensky_states": parse_opensky_states,
    "adsblol_aircraft": parse_adsblol_aircraft,
    "opensky_track": parse_opensky_track,
    "adsbdb": parse_adsbdb,
    "launch_library": parse_launch_library,
    "hexdb_aircraft": parse_hexdb_aircraft,
    "hexdb_route": parse_hexdb_route,
    # --- Keyless origins (v1.5) ---
    "epss": parse_epss,
    "osv": parse_osv,
    "cve_record": parse_cve_record,
    "ransomware_live": parse_ransomware_live,
    "yaraify": parse_yaraify,
    "sans_isc_ip": parse_sans_isc_ip,
    "ip_guide": parse_ip_guide,
    "dbip_ip": parse_dbip_ip,
    "geojs_ip": parse_geojs_ip,
    "ipapi_is": parse_ipapi_is,
    "maclookup": parse_maclookup,
    "peeringdb": parse_peeringdb_net,
    "tranco": parse_tranco_rank,
    "hudsonrock": parse_hudsonrock,
    "disify": parse_disify,
    "gravatar": parse_gravatar,
    "cidr_ranges": parse_cidr_ranges,
    "hstspreload": parse_hstspreload,
    "ssl_labs": parse_ssl_labs,
    "bluesky": parse_bluesky_profile,
    "lemmy": parse_lemmy_user,
    "gitlab_user": parse_gitlab_user,
    "forgejo_user": parse_forgejo_user,
    "openlibrary": parse_openlibrary,
    "pubmed": parse_pubmed,
    "europepmc": parse_europepmc,
    "doaj": parse_doaj,
    "gdelt": parse_gdelt,
    "archive_org": parse_archive_org,
    "photon": parse_photon,
    "radio_browser": parse_radio_browser,
    "npm_package": parse_npm_package,
    "pypi_package": parse_pypi_package,
    "dockerhub_search": parse_dockerhub_search,
    "huggingface": parse_huggingface,
    "planespotters": parse_planespotters,
    "satnogs": parse_satnogs,
    "spaceflightnews": parse_spaceflightnews,
    "address_list": parse_address_list,
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


def list_parsers() -> list[tuple[str, str]]:
    """Return (name, description) tuples for every registered parser.

    Used by the CLI `status` endpoint to advertise the available
    parser names, and by tests to assert that a custom parser made it
    into the registry.
    """
    out: list[tuple[str, str]] = []
    for name, spec in PARSERS.items():
        if isinstance(spec, tuple):
            out.append((name, spec[1]))
        else:
            out.append((name, spec.__doc__ or ""))
    return sorted(out)
