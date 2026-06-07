"""
estorides_core.mitre_attack
===========================
Lightweight MITRE ATT&CK mapper.

A small but curated lookup table that maps OSINT observation
categories to ATT&CK technique IDs. Used to stamp every knowledge-
graph observation with the techniques it might support, so the
LLM analyst stage can produce a more useful brief ("observations
from sources X, Y, Z suggest technique T1595 — Active Scanning").

The full ATT&CK STIX bundle is ~25 MB; we deliberately do NOT
download it. The lookup table here covers the ~20 techniques that
realistically surface in an OSINT-only context (the rest require
active exploitation evidence we don't collect).

This module is a soft enhancement: missing entries are not errors,
they just produce no mapping. The orchestrator can call
`map_observation(observation)` after the inference step and attach
the result to the observation dict.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple

log = logging.getLogger("estorides.mitre")


# ----------------------------------------------------------------- technique table
# Source-keyed (and observation-keyed) -> list of (technique_id, label)
# Curated; not exhaustive. Add new entries by appending to this table.
# Reference: https://attack.mitre.org/techniques/enterprise/
_TECHNIQUE_TABLE: Dict[str, List[Tuple[str, str]]] = {
    "shodan_internetdb": [
        ("T1595", "Active Scanning"),
        ("T1595.001", "Scanning IP Blocks"),
        ("T1046", "Network Service Discovery"),
    ],
    "abuseipdb_check": [
        ("T1589.002", "Gather Victim Network Information: DNS"),
    ],
    "greynoise_community": [
        ("T1595.001", "Scanning IP Blocks"),
    ],
    "alienvault_otx": [
        ("T1589", "Gather Victim Identity Information"),
        ("T1589.002", "Gather Victim Network Information: DNS"),
    ],
    "nvd_cve": [
        ("T1588.006", "Obtain Capabilities: Vulnerabilities"),
    ],
    "github_advisories": [
        ("T1588.006", "Obtain Capabilities: Vulnerabilities"),
    ],
    "cve_search_circl": [
        ("T1588.006", "Obtain Capabilities: Vulnerabilities"),
    ],
    "threatfox": [
        ("T1583.006", "Acquire Infrastructure: Web Services"),
        ("T1071.001", "Application Layer Protocol: Web Protocols"),
    ],
    "urlhaus": [
        ("T1566.002", "Phishing: Spearphishing Link"),
        ("T1102", "Web Service"),
    ],
    "feodo_tracker": [
        ("T1071.001", "Application Layer Protocol: Web Protocols"),
        ("T1102", "Web Service"),
    ],
    "openphish_feed": [
        ("T1566.002", "Phishing: Spearphishing Link"),
    ],
    "phishtank": [
        ("T1566.002", "Phishing: Spearphishing Link"),
    ],
    "sslbl": [
        ("T1573", "Encrypted Channel"),
    ],
    "blocklist": [
        ("T1071", "Application Layer Protocol"),
    ],
    "leakcheck_public": [
        ("T1078", "Valid Accounts"),
        ("T1003", "OS Credential Dumping"),
    ],
    "psbdmp_ws": [
        ("T1003", "OS Credential Dumping"),
        ("T1552.001", "Credentials in Files"),
    ],
    "hibp_breach": [
        ("T1078", "Valid Accounts"),
    ],
    "hibp_paste": [
        ("T1552.001", "Credentials in Files"),
        ("T1003", "OS Credential Dumping"),
    ],
    "gists_github_search": [
        ("T1552.001", "Credentials in Files"),
    ],
    "telegram_search_ligated": [
        ("T1102", "Web Service"),
        ("T1567", "Exfiltration Over Web Service"),
    ],
    "ransomwatch": [
        ("T1486", "Data Encrypted for Impact"),
    ],
    "otx_domain_passive": [
        ("T1583.001", "Acquire Infrastructure: Domains"),
    ],
    "blocklist_de_all": [
        ("T1071", "Application Layer Protocol"),
    ],
    "emergingthreats_compromised": [
        ("T1071", "Application Layer Protocol"),
    ],
    "feodo_tracker": [
        ("T1071.001", "Application Layer Protocol: Web Protocols"),
    ],
}


# Heuristic keyword patterns observed in parsed payloads.
# These are applied on top of the source-based table to catch
# "malware family" mentions, c2 framework names, etc.
_KEYWORD_PATTERNS: List[Tuple[str, str, str]] = [
    # (regex_substring, technique_id, technique_label) — case-insensitive
    ("cobalt strike", "T1071.001", "Application Layer Protocol: Web Protocols"),
    ("cobaltstrike", "T1071.001", "Application Layer Protocol: Web Protocols"),
    ("mimikatz",     "T1003.001", "OS Credential Dumping: LSASS Memory"),
    ("metasploit",   "T1588.001", "Obtain Capabilities: Malware"),
    ("covenant",     "T1071.001", "Application Layer Protocol: Web Protocols"),
    ("brute ratel",  "T1059.001", "Command and Scripting Interpreter: PowerShell"),
    ("sliver",       "T1071.001", "Application Layer Protocol: Web Protocols"),
    ("asyncrat",     "T1059.003", "Command and Scripting Interpreter: Windows Command Shell"),
    ("remcos",       "T1059.003", "Command and Scripting Interpreter: Windows Command Shell"),
    ("quasar",       "T1059.003", "Command and Scripting Interpreter: Windows Command Shell"),
    ("phishing",     "T1566",     "Phishing"),
    ("ransomware",   "T1486",     "Data Encrypted for Impact"),
    ("lockbit",      "T1486",     "Data Encrypted for Impact"),
    ("conti",        "T1486",     "Data Encrypted for Impact"),
    ("revil",        "T1486",     "Data Encrypted for Impact"),
    ("sodinokibi",   "T1486",     "Data Encrypted for Impact"),
    ("blackcat",     "T1486",     "Data Encrypted for Impact"),
    ("alphv",        "T1486",     "Data Encrypted for Impact"),
    ("ddos",         "T1498",     "Network Denial of Service"),
    ("botnet",       "T1071",     "Application Layer Protocol"),
    ("stealer",      "T1005",     "Data from Local System"),
    ("redline",      "T1005",     "Data from Local System"),
    ("vidar",        "T1005",     "Data from Local System"),
    ("raccoon",      "T1005",     "Data from Local System"),
    ("lumma",        "T1005",     "Data from Local System"),
]


def _scan_keywords(text: str) -> List[Tuple[str, str]]:
    """Scan a text blob for ATT&CK-relevant keywords."""
    if not text:
        return []
    lower = text.lower()
    out: List[Tuple[str, str]] = []
    seen: set[str] = set()
    for needle, tid, label in _KEYWORD_PATTERNS:
        if needle in lower and tid not in seen:
            seen.add(tid)
            out.append((tid, label))
    return out


def map_observation(observation: Dict[str, Any]) -> Dict[str, Any]:
    """Return ATT&CK techniques associated with an observation.

    Output:
        {
          "techniques": [
            {"id": "T1595", "label": "Active Scanning", "via": "source:shodan_internetdb"},
            ...
          ],
          "tactic_ids": ["TA0043"],  # not populated yet — future
        }
    """
    src = observation.get("source", "")
    techniques: List[Dict[str, str]] = []
    seen: set[str] = set()

    for tid, label in _TECHNIQUE_TABLE.get(src, []):
        if tid in seen:
            continue
        seen.add(tid)
        techniques.append({"id": tid, "label": label, "via": f"source:{src}"})

    # Keyword scan on the raw + parsed payloads.
    import json
    blob_parts: List[str] = []
    for k in ("raw", "parsed"):
        v = observation.get(k)
        if v is None:
            continue
        try:
            blob_parts.append(json.dumps(v, ensure_ascii=False, default=str)[:20000])
        except (TypeError, ValueError):
            blob_parts.append(str(v)[:20000])
    blob = "\n".join(blob_parts)
    for tid, label in _scan_keywords(blob):
        if tid in seen:
            continue
        seen.add(tid)
        techniques.append({"id": tid, "label": label, "via": "keyword"})

    return {"techniques": techniques}


def map_observations(observations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Bulk mapper. Stamps each observation in place with `_mitre` key.

    Returns the list of observations (for chaining). Mutates in place
    for performance — the orchestrator doesn't keep references to the
    pre-mapping list, so a side effect is safe.
    """
    for obs in observations:
        try:
            obs["mitre"] = map_observation(obs)
        except Exception as e:  # noqa: BLE001
            log.debug("mitre mapping failed for %s: %s", obs.get("source"), e)
            obs["mitre"] = {"techniques": [], "error": str(e)}
    return observations


def all_techniques_for(observations: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Aggregate: unique techniques across all observations, sorted by id."""
    seen: Dict[str, Dict[str, str]] = {}
    for obs in observations:
        for t in obs.get("mitre", {}).get("techniques", []):
            tid = t["id"]
            if tid not in seen:
                seen[tid] = t
    return sorted(seen.values(), key=lambda x: x["id"])
