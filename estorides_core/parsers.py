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
