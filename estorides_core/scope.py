"""
estorides_core.scope
=====================
Bug-bounty scope classification.

Takes the assets a passive run surfaces (hosts, IPs, CIDRs) and decides,
for each one, whether it is in-scope, out-of-scope, or unknown against a
program's rules. Out-of-scope always wins so the operator never points
active tooling at an excluded asset — the fastest way to get removed from
a program.

Rule grammar (one rule per line, blank lines and `#` comments ignored):

    *.example.com        wildcard host suffix (matches sub.example.com and example.com)
    example.com          exact host
    192.0.2.0/24         CIDR network (IPv4 or IPv6)
    198.51.100.7         single IP address
    re:^api[0-9]+\\.ex   regex (prefix ``re:``), matched against the raw asset

A single rules file may carry both lists, divided by a line whose content
is ``## out-of-scope`` (case-insensitive); rules above the divider are
in-scope, rules below are out-of-scope. The two lists can also be supplied
independently when building a :class:`ScopeMatcher` directly.

The design is deliberately decoupled (SOLID): every grammar form is a
small :class:`ScopeRule` with one ``matches`` method, rules are produced
by an ordered list of detector factories (open/closed — add a form by
appending one factory), and :class:`ScopeMatcher` only knows the
out-beats-in precedence. No call site hard-codes a grammar.
"""
from __future__ import annotations

import ipaddress
import json
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence

log = logging.getLogger("estorides.scope")

IN_SCOPE = "in_scope"
OUT_OF_SCOPE = "out_of_scope"
UNKNOWN = "unknown"

OUT_OF_SCOPE_DIVIDER = "## out-of-scope"


# --------------------------------------------------------------- asset shape
def normalise_asset(raw: str) -> str:
    """Reduce a raw asset string to a comparable host or IP literal.

    Strips an optional scheme, any path/query, a port, surrounding
    whitespace and a trailing dot, and lowercases the result. A value that
    is already a bare host or IP passes through unchanged (bar casing)."""
    asset = raw.strip().lower()
    if not asset:
        return ""
    if "://" in asset:
        asset = asset.split("://", 1)[1]
    # Drop path, query and fragment.
    for sep in ("/", "?", "#"):
        if sep in asset:
            asset = asset.split(sep, 1)[0]
    # Drop credentials.
    if "@" in asset:
        asset = asset.rsplit("@", 1)[1]
    asset = asset.strip("[]")  # bracketed IPv6
    # Drop a trailing :port, but never the colons of an IPv6 literal.
    if asset.count(":") == 1:
        host, _, port = asset.partition(":")
        if port.isdigit():
            asset = host
    return asset.rstrip(".")


def is_ip(asset: str) -> bool:
    """True when `asset` parses as a bare IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(asset)
        return True
    except ValueError:
        return False


# ------------------------------------------------------------------- rules
class ScopeRule(ABC):
    """A single scope predicate. Implementations match exactly one grammar."""

    @abstractmethod
    def matches(self, asset: str) -> bool:
        """True when `asset` (already normalised) is covered by this rule."""

    @abstractmethod
    def describe(self) -> str:
        """Human-readable form of the rule, for reports and audit."""


@dataclass(frozen=True)
class WildcardRule(ScopeRule):
    """`*.example.com` — the apex and any subdomain of it."""

    suffix: str  # the part after the leading '*.', e.g. "example.com"

    def matches(self, asset: str) -> bool:
        if is_ip(asset):
            return False
        return asset == self.suffix or asset.endswith("." + self.suffix)

    def describe(self) -> str:
        return f"*.{self.suffix}"


@dataclass(frozen=True)
class ExactHostRule(ScopeRule):
    """A single fully-qualified host, matched verbatim."""

    host: str

    def matches(self, asset: str) -> bool:
        return not is_ip(asset) and asset == self.host

    def describe(self) -> str:
        return self.host


@dataclass(frozen=True)
class CidrRule(ScopeRule):
    """An IPv4/IPv6 network; matches any address inside it."""

    network: ipaddress._BaseNetwork

    def matches(self, asset: str) -> bool:
        if not is_ip(asset):
            return False
        try:
            return ipaddress.ip_address(asset) in self.network
        except ValueError:
            return False

    def describe(self) -> str:
        return str(self.network)


@dataclass(frozen=True)
class RegexRule(ScopeRule):
    """A compiled regex matched against the raw normalised asset."""

    pattern: "re.Pattern[str]"

    def matches(self, asset: str) -> bool:
        return self.pattern.search(asset) is not None

    def describe(self) -> str:
        return f"re:{self.pattern.pattern}"


# ----------------------------------------------------------- rule factories
def _wildcard_factory(text: str) -> Optional[ScopeRule]:
    if text.startswith("*."):
        suffix = normalise_asset(text[2:])
        return WildcardRule(suffix) if suffix else None
    return None


def _regex_factory(text: str) -> Optional[ScopeRule]:
    if text.startswith("re:"):
        body = text[3:].strip()
        try:
            return RegexRule(re.compile(body, re.IGNORECASE))
        except re.error as e:
            log.warning("invalid scope regex %r: %s", body, e)
            return None
    return None


def _cidr_factory(text: str) -> Optional[ScopeRule]:
    if "/" in text:
        try:
            return CidrRule(ipaddress.ip_network(text, strict=False))
        except ValueError:
            return None
    return None


def _ip_factory(text: str) -> Optional[ScopeRule]:
    if is_ip(text):
        # A bare IP is a /32 or /128 network so one code path covers it.
        return CidrRule(ipaddress.ip_network(text, strict=False))
    return None


def _exact_host_factory(text: str) -> Optional[ScopeRule]:
    host = normalise_asset(text)
    return ExactHostRule(host) if host else None


# Order matters: the first factory that claims a line wins. The exact-host
# fallback is last because it accepts almost anything.
_RULE_FACTORIES: Sequence[Callable[[str], Optional[ScopeRule]]] = (
    _wildcard_factory,
    _regex_factory,
    _cidr_factory,
    _ip_factory,
    _exact_host_factory,
)


def parse_rule(line: str) -> Optional[ScopeRule]:
    """Parse one rule line into a ScopeRule, or None for blank/comment/invalid."""
    text = line.strip()
    if not text or text.startswith("#"):
        return None
    for factory in _RULE_FACTORIES:
        rule = factory(text)
        if rule is not None:
            return rule
    return None


def parse_rules(lines: Iterable[str]) -> List[ScopeRule]:
    """Parse many rule lines, skipping blanks, comments and invalid entries."""
    rules: List[ScopeRule] = []
    for line in lines:
        rule = parse_rule(line)
        if rule is not None:
            rules.append(rule)
    return rules


# ------------------------------------------------------------------ matcher
class ScopeMatcher:
    """Classifies assets against in-scope and out-of-scope rule sets.

    Out-of-scope is evaluated first and wins outright, so an asset that
    matches both a broad in-scope wildcard and a narrow out-of-scope rule
    is reported as out-of-scope.
    """

    def __init__(
        self,
        in_scope: Sequence[ScopeRule],
        out_of_scope: Sequence[ScopeRule] = (),
    ) -> None:
        self._in = list(in_scope)
        self._out = list(out_of_scope)

    @property
    def in_rules(self) -> List[ScopeRule]:
        return list(self._in)

    @property
    def out_rules(self) -> List[ScopeRule]:
        return list(self._out)

    def classify(self, raw_asset: str) -> str:
        """Return IN_SCOPE, OUT_OF_SCOPE or UNKNOWN for a single asset."""
        asset = normalise_asset(raw_asset)
        if not asset:
            return UNKNOWN
        if any(rule.matches(asset) for rule in self._out):
            return OUT_OF_SCOPE
        if any(rule.matches(asset) for rule in self._in):
            return IN_SCOPE
        return UNKNOWN

    def partition(self, assets: Iterable[str]) -> Dict[str, List[str]]:
        """Bucket many assets, returning sorted, de-duplicated lists.

        Keys are IN_SCOPE, OUT_OF_SCOPE and UNKNOWN. De-duplication is on
        the normalised form so `HTTPS://Example.com/` and `example.com`
        collapse to one entry."""
        buckets: Dict[str, set] = {IN_SCOPE: set(), OUT_OF_SCOPE: set(), UNKNOWN: set()}
        for raw in assets:
            asset = normalise_asset(raw)
            if not asset:
                continue
            buckets[self.classify(asset)].add(asset)
        return {key: sorted(values) for key, values in buckets.items()}


# ------------------------------------------------------------- file loading
def load_rules_file(path: Path) -> ScopeMatcher:
    """Build a matcher from a rules file, honouring the out-of-scope divider.

    Lines above a ``## out-of-scope`` divider (case-insensitive) are
    in-scope; lines below are out-of-scope. A file with no divider is all
    in-scope."""
    in_lines: List[str] = []
    out_lines: List[str] = []
    current = in_lines
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().lower() == OUT_OF_SCOPE_DIVIDER:
            current = out_lines
            continue
        current.append(line)
    return ScopeMatcher(parse_rules(in_lines), parse_rules(out_lines))


# ----------------------------------------------------------- asset loading
def load_assets(path: Path) -> List[str]:
    """Read assets from a file: a discover surface JSON or a flat host list.

    A JSON document is mined for assets in `domains`, `entities` (values of
    host/ip types) and any top-level list of strings. Anything else is read
    as one asset per line."""
    text = path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if stripped.startswith(("{", "[")):
        try:
            return _assets_from_json(json.loads(text))
        except (json.JSONDecodeError, TypeError, ValueError):
            log.debug("asset file %s is not parseable JSON, reading as lines", path)
    return [line for line in (ln.strip() for ln in text.splitlines()) if line and not line.startswith("#")]


_HOST_ENTITY_TYPES = frozenset({"domain", "ipv4", "ipv6", "url", "host"})


def _assets_from_json(doc: object) -> List[str]:
    """Extract candidate assets from a parsed discover/result JSON document."""
    assets: List[str] = []
    if isinstance(doc, list):
        assets.extend(str(item) for item in doc if isinstance(item, (str, int)))
        return assets
    if isinstance(doc, dict):
        domains = doc.get("domains")
        if isinstance(domains, list):
            assets.extend(str(d) for d in domains)
        entities = doc.get("entities")
        if isinstance(entities, list):
            for ent in entities:
                if isinstance(ent, dict) and ent.get("type") in _HOST_ENTITY_TYPES:
                    value = ent.get("value")
                    if value:
                        assets.append(str(value))
    return assets


# ------------------------------------------------------------- flat export
@dataclass(frozen=True)
class ScopeReport:
    """Classified assets plus the flat lists an operator pipes onward."""

    in_scope: List[str]
    out_of_scope: List[str]
    unknown: List[str]

    @property
    def hosts(self) -> List[str]:
        """In-scope hostnames (everything in-scope that is not an IP)."""
        return [a for a in self.in_scope if not is_ip(a)]

    @property
    def ips(self) -> List[str]:
        """In-scope bare IP addresses."""
        return [a for a in self.in_scope if is_ip(a)]

    def to_dict(self) -> Dict[str, List[str]]:
        return {
            "in_scope": self.in_scope,
            "out_of_scope": self.out_of_scope,
            "unknown": self.unknown,
            "in_scope_hosts": self.hosts,
            "in_scope_ips": self.ips,
        }


def build_report(matcher: ScopeMatcher, assets: Iterable[str]) -> ScopeReport:
    """Classify `assets` with `matcher` and return a :class:`ScopeReport`."""
    buckets = matcher.partition(assets)
    return ScopeReport(
        in_scope=buckets[IN_SCOPE],
        out_of_scope=buckets[OUT_OF_SCOPE],
        unknown=buckets[UNKNOWN],
    )


def write_flat_lists(report: ScopeReport, out_dir: Path) -> Dict[str, Path]:
    """Write newline-delimited flat lists for piping into active tooling.

    Produces `in_scope_hosts.txt`, `in_scope_ips.txt` and `unknown.txt`
    under `out_dir`. Returns the map of label to written path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "in_scope_hosts": report.hosts,
        "in_scope_ips": report.ips,
        "unknown": report.unknown,
    }
    written: Dict[str, Path] = {}
    for label, items in files.items():
        target = out_dir / f"{label}.txt"
        target.write_text("\n".join(items) + ("\n" if items else ""), encoding="utf-8")
        written[label] = target
    return written
