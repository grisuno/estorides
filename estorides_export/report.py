"""
estorides_export.report
=======================

Markdown report generation for finished cases.

Design choices
--------------
* Pure function. The report builder takes a case dict + a list of
  entities + (optionally) a previous case id, and returns a Markdown
  string. No I/O happens here — the caller (CLI, web, scheduled job)
  decides where the report lands. This keeps the formatter unit-
  testable in isolation.
* Progressive disclosure. The first 30 lines carry the TL;DR so a
  reviewer can decide in 10 seconds whether the case is worth a deep
  read. Full IOCs and source roster come after a `---` separator.
* Diff support. When `previous_case_id` is supplied, the report
  includes a "what's new since last run" section that mirrors
  `CaseStore.diff_entities` — same keys, no double bookkeeping.
* No LLM dependency. A separate LLM-narrative step can be wired on
  top, but the baseline report must work even when no LLM backend
  is configured (the engine returns a stub analysis in that case).
"""
from __future__ import annotations

import datetime as _dt
import logging
from collections import Counter
from typing import Any, Dict, Iterable, List, Optional

log = logging.getLogger("estorides.export.report")


# --------------------------------------------------------------------------- #
# Section builders                                                            #
# --------------------------------------------------------------------------- #
def _tldr(case: Dict[str, Any], entities: List[Dict[str, Any]],
          sources_queried: int, sources_succeeded: int,
          diff: Optional[Dict[str, Any]]) -> List[str]:
    """Top-of-page executive summary. 6-10 lines max."""
    out: List[str] = []
    out.append(f"# {case.get('query', 'unknown')} — OSINT Report")
    out.append("")
    out.append(
        f"**Case ID:** `{case.get('id', '?')}` · "
        f"**Status:** `{case.get('status', '?')}` · "
        f"**Type:** `{case.get('query_type', '?')}`"
    )
    created = case.get("created_at")
    if created:
        out.append(
            f"**Generated:** {_dt.datetime.fromtimestamp(float(created)).isoformat(timespec='seconds')}"
        )
    out.append("")
    out.append("## TL;DR")
    out.append("")
    out.append(
        f"- **{len(entities)}** entities discovered across "
        f"**{sources_succeeded}/{sources_queried}** sources"
    )
    type_counts = Counter(e.get("type", "?") for e in entities)
    top_types = ", ".join(f"`{t}` ({n})" for t, n in type_counts.most_common(5))
    if top_types:
        out.append(f"- Top entity types: {top_types}")
    if diff:
        out.append(
            f"- Diff vs `{diff.get('case_a')}`: "
            f"**+{diff.get('added_count', 0)}** new, "
            f"**-{diff.get('removed_count', 0)}** dropped, "
            f"**{diff.get('common_count', 0)}** common"
        )
    if case.get("notes"):
        out.append(f"- Notes: {case['notes']}")
    return out


def _iocs(entities: Iterable[Dict[str, Any]]) -> List[str]:
    """The sections the next responder (CTI team, SOC) actually pastes
    into a ticket. Domains, IPs, emails, hashes, CVEs, crypto addresses."""
    bucket: Dict[str, List[str]] = {
        "domains": [], "ips": [], "emails": [],
        "hashes": [], "cves": [], "crypto": [],
    }
    for e in entities:
        t = e.get("type", "")
        v = e.get("value", "")
        if not v:
            continue
        if t == "domain":
            bucket["domains"].append(v)
        elif t in ("ipv4", "ipv6"):
            bucket["ips"].append(v)
        elif t == "email":
            bucket["emails"].append(v)
        elif t in ("md5", "sha1", "sha256"):
            bucket["hashes"].append(v)
        elif t == "cve":
            bucket["cves"].append(v)
        elif t in ("btc_address", "eth_address"):
            bucket["crypto"].append(v)
    out: List[str] = []
    out.append("## IOCs")
    out.append("")
    for label, key in (
        ("Domains", "domains"), ("IPs", "ips"),
        ("Emails", "emails"), ("Hashes", "hashes"),
        ("CVEs", "cves"), ("Crypto addresses", "crypto"),
    ):
        vals = sorted(set(bucket[key]))
        if not vals:
            continue
        out.append(f"### {label} ({len(vals)})")
        for v in vals[:50]:  # cap to keep the report readable
            out.append(f"- `{v}`")
        if len(vals) > 50:
            out.append(f"- … and {len(vals) - 50} more")
        out.append("")
    return out


def _diff_section(diff: Optional[Dict[str, Any]]) -> List[str]:
    """The "what's new since last run" block. Empty when no baseline."""
    if not diff:
        return []
    out: List[str] = []
    out.append("## Diff vs previous run")
    out.append("")
    out.append(
        f"Compared to `{diff['case_a']}` → `{diff['case_b']}`: "
        f"+{diff['added_count']} added, -{diff['removed_count']} removed, "
        f"{diff['common_count']} common."
    )
    out.append("")
    by_type = diff.get("by_type", {})
    if by_type.get("added"):
        out.append("### Added by type")
        for t, n in sorted(by_type["added"].items(), key=lambda x: -x[1]):
            out.append(f"- `{t}`: {n}")
        out.append("")
    if by_type.get("removed"):
        out.append("### Removed by type")
        for t, n in sorted(by_type["removed"].items(), key=lambda x: -x[1]):
            out.append(f"- `{t}`: {n}")
        out.append("")
    sample = diff.get("added", [])[:20]
    if sample:
        out.append("### Sample of new entities")
        for e in sample:
            out.append(f"- `{e['type']}`: {e['value']}")
        if len(diff.get("added", [])) > 20:
            out.append(f"- … and {len(diff['added']) - 20} more")
        out.append("")
    return out


def _analysis(case: Dict[str, Any]) -> List[str]:
    """The LLM analysis (or stub) embedded verbatim in a code block."""
    out: List[str] = []
    raw = case.get("analysis_json")
    if not raw:
        return out
    out.append("## LLM analysis")
    out.append("")
    out.append("```")
    # The store stores it as a JSON string (could be dict or string).
    if isinstance(raw, str):
        out.append(raw.strip())
    else:
        # Best-effort: prefer "content" if present, else stringify.
        content = (raw or {}).get("content") if isinstance(raw, dict) else None
        out.append((content or str(raw)).strip())
    out.append("```")
    out.append("")
    return out


def _meta_footer(case: Dict[str, Any], sources_queried: int,
                 sources_succeeded: int) -> List[str]:
    out: List[str] = []
    out.append("---")
    out.append("")
    out.append(
        f"_Report generated by Estorides · sources queried: {sources_queried} · "
        f"succeeded: {sources_succeeded} · "
        f"entities: {case.get('entity_count', 0)} · "
        f"observations: {case.get('obs_count', 0)}_"
    )
    return out


# --------------------------------------------------------------------------- #
# Public entry point                                                          #
# --------------------------------------------------------------------------- #
def render_markdown_report(
    case: Dict[str, Any],
    entities: Optional[List[Dict[str, Any]]] = None,
    sources_queried: int = 0,
    sources_succeeded: int = 0,
    diff: Optional[Dict[str, Any]] = None,
) -> str:
    """Build a Markdown report for `case`.

    Parameters
    ----------
    case
        The case row, as returned by `CaseStore.get_case`. `analysis_json`
        is optional; if present it is embedded verbatim.
    entities
        The full entity list. If omitted, only the counts in the case
        row are used (TL;DR still works, IOC section is empty).
    diff
        Optional output of `CaseStore.diff_entities(a, b)`. When given,
        a "what's new" section is appended before the analysis.

    Returns
    -------
    str
        The full Markdown document. UTF-8, LF newlines, no trailing
        newline (callers add their own if writing to a file).
    """
    entities = entities or []
    sections: List[List[str]] = [
        _tldr(case, entities, sources_queried, sources_succeeded, diff),
        ["---", ""],
        _iocs(entities),
    ]
    if diff:
        sections.append(_diff_section(diff))
    sections.append(_analysis(case))
    sections.append(_meta_footer(case, sources_queried, sources_succeeded))
    return "\n".join(line for section in sections for line in section).rstrip() + "\n"
