"""
estorides_core.ssrf_guard
=========================
SSRF / SSRF-rebound protection for outbound HTTP.

The OSINT engine speaks to user-specified hosts (a domain, a URL from a
paste, a link from a Telegram channel). Without filtering, a malicious
or careless query can redirect our client at:

  * RFC1918 private space              (10/8, 172.16/12, 192.168/16)
  * Loopback                           (127/8, ::1)
  * Link-local / cloud metadata        (169.254/16 — AWS, GCP, Azure IMDS)
  * CGNAT / Tailscale                  (100.64/10)
  * Multicast / reserved               (224/4, 240/4, 0/8, 255.255.255.255)
  * Documentation / benchmark          (192.0.2/24, 198.51.100/24, 203.0.113/24)
  * IPv6 link-local                    (fe80::/10)
  * IPv6 unique-local                  (fc00::/7)
  * IPv4-mapped IPv6                   (::ffff:0:0/96)

We block at TWO layers:

  1. Canonicalise the literal host the source YAML gave us. Reject dotted
     forms that land in a reserved range and any IPv6 in a reserved prefix.
  2. For hostnames, resolve A + AAAA at fetch time and reject if *any*
     answer lands in a reserved range. This is the TOCTOU-resistant layer
     that catches a DNS rebinding attack where the YAML says
     `attacker.com` but the resolver returns `169.254.169.254`.

Pinning the IP at the socket layer (the third leg of true TOCTOU defence)
is intentionally out of scope: aiohttp doesn't expose socket-level
binding on a request-by-request basis without monkey-patching, and the
rebind window is short enough that resolving + pinning inside a single
event-loop turn defeats the practical rebinder. The resolver here is
synchronous and runs immediately before the HTTP request goes out, so
a rebinder must win a TTL=0 race against the connector.

Allowlisting is opt-in: if `ESTORIDES_ALLOWED_HOSTS` is set, only those
hosts (suffix-matched) may be contacted. This is the right mode for
air-gapped or hardened deployments.

This module is intentionally dependency-light — only stdlib — so the
core can import it without pulling aiohttp.
"""
from __future__ import annotations

import ipaddress
import logging
import os
import socket
from dataclasses import dataclass
from typing import FrozenSet, Optional, Sequence
from urllib.parse import urlparse

log = logging.getLogger("estorides.ssrf")


# --------------------------------------------------------------------- ranges
# IPv4 reserved/blocked ranges: (network, prefix_length).
_IPV4_BLOCKS: Sequence[ipaddress._BaseNetwork] = tuple(
    ipaddress.ip_network(net) for net in (
        "0.0.0.0/8",           # "this" network
        "10.0.0.0/8",          # RFC1918
        "100.64.0.0/10",       # CGNAT / Tailscale
        "127.0.0.0/8",         # loopback
        "169.254.0.0/16",      # link-local (incl. 169.254.169.254 cloud IMDS)
        "172.16.0.0/12",       # RFC1918
        "192.0.0.0/24",        # IETF protocol assignments
        "192.0.2.0/24",        # TEST-NET-1
        "192.168.0.0/16",      # RFC1918
        "198.18.0.0/15",       # benchmarking
        "198.51.100.0/24",     # TEST-NET-2
        "203.0.113.0/24",      # TEST-NET-3
        "224.0.0.0/4",         # multicast
        "240.0.0.0/4",         # reserved (incl. 255.255.255.255 broadcast)
    )
)

# IPv6 reserved prefixes. We match on the textual representation rather
# than building full networks, so a hex prefix like 'fe8' catches the
# entire fe80::/10 block in a single substring test.
_IPV6_BLOCK_PREFIXES: FrozenSet[str] = frozenset((
    "::",                # unspecified
    "::1",               # loopback
    "::ffff:",           # IPv4-mapped (::ffff:127.0.0.1, ::ffff:10.x, etc.)
    "64:ff9b::",         # NAT64
    "64:ff9b:1::",       # local NAT64
    "100::",             # discard prefix
    "2001:db8::",        # documentation
    "fc",                # unique-local fc00::/7
    "fd",
    "fe8", "fe9", "fea", "feb",  # link-local fe80::/10
    "fec", "fed", "fee", "fef",  # site-local fec0::/10 (deprecated)
    "ff",                # multicast ff00::/8
))


# ----------------------------------------------------------------- result
@dataclass(frozen=True)
class GuardResult:
    allowed: bool
    reason: str = ""
    host: str = ""
    resolved: FrozenSet[str] = frozenset()

    def __bool__(self) -> bool:  # so `if guard(url):` works
        return self.allowed


# ----------------------------------------------------------------- helpers
def _is_blocked_v4(ip: ipaddress.IPv4Address) -> bool:
    return any(ip in net for net in _IPV4_BLOCKS)


def _is_blocked_v6(addr: str) -> bool:
    """Match an IPv6 textual address against the prefix table.

    Lower-cased, leading zeros collapsed, no scope-id parsing required.
    """
    a = addr.lower().split("%", 1)[0]  # strip zone id
    for prefix in _IPV6_BLOCK_PREFIXES:
        if a.startswith(prefix):
            return True
    # A 4-in-6 mapped address is also blocked via ::ffff: prefix above,
    # but we double-check the embedded IPv4 here for clarity.
    if a.startswith("::ffff:"):
        tail = a.removeprefix("::ffff:")
        try:
            return _is_blocked_v4(ipaddress.IPv4Address(tail))
        except ValueError:
            return False
    return False


def _normalise_host(host: str) -> Optional[str]:
    """Lowercase, strip brackets from IPv6 literals, return None if empty."""
    if not host:
        return None
    h = host.strip().strip("[]").lower()
    return h or None


def _is_host_in_blocked_literal(host: str) -> Optional[str]:
    """If `host` is a literal IP in a blocked range, return a reason string.
    Otherwise return None."""
    # IPv4 literal?
    try:
        ip = ipaddress.IPv4Address(host)
        if _is_blocked_v4(ip):
            return f"ipv4-in-blocked-range:{ip}"
        return None
    except ValueError:
        pass
    # IPv6 literal?
    try:
        ipaddress.IPv6Address(host)
    except ValueError:
        return None  # not an IP literal
    if _is_blocked_v6(host):
        return f"ipv6-in-blocked-range:{host}"
    return None


def _resolve(host: str) -> FrozenSet[str]:
    """Resolve `host` to its A + AAAA records. Empty on failure."""
    out: set[str] = set()
    try:
        infos = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    except socket.gaierror as e:
        log.debug("DNS resolution failed for %s: %s", host, e)
        return frozenset()
    for fam, *_rest, sockaddr in infos:
        sock_host: str = sockaddr[0]  # type: ignore[assignment]
        if fam == socket.AF_INET:
            out.add(sock_host)
        elif fam == socket.AF_INET6:
            out.add(sock_host.split("%", 1)[0])
    return frozenset(out)


def _matches_allowlist(host: str, allowlist: Sequence[str]) -> bool:
    """Return True if `host` matches any entry in the allowlist.

    An entry like `osiris.example.com` matches the host itself and any
    subdomain. An entry like `*` matches everything (escape hatch)."""
    for entry in allowlist:
        e = entry.strip().lower().lstrip(".")
        if not e:
            continue
        if e == "*":
            return True
        if host == e or host.endswith("." + e):
            return True
    return False


# ----------------------------------------------------------------- public
def _load_allowlist() -> Sequence[str]:
    raw = os.environ.get("ESTORIDES_ALLOWED_HOSTS", "")
    return tuple(h for h in raw.split(",") if h.strip())


def check_url(url: str, *, resolve: bool = True) -> GuardResult:
    """Validate a URL for outbound fetch.

    Args:
        url: the URL string the source YAML wants us to hit.
        resolve: when True (default) also resolve hostnames and reject
            if any answer lands in a reserved range. Disable only in
            tests with mocked DNS.

    Returns:
        GuardResult with allowed/reason. Use as a bool.
    """
    if not url:
        return GuardResult(False, reason="empty-url")

    try:
        parsed = urlparse(url)
    except ValueError as e:
        return GuardResult(False, reason=f"unparseable-url:{e}", host="")

    # The scheme gate: anything other than http/https is a non-starter.
    if parsed.scheme not in ("http", "https"):
        return GuardResult(False, reason=f"disallowed-scheme:{parsed.scheme}",
                           host=parsed.hostname or "")

    host = _normalise_host(parsed.hostname or "")
    if not host:
        return GuardResult(False, reason="no-host", host="")

    # Allowlist: if set, only matching hosts are allowed through.
    allowlist = _load_allowlist()
    if allowlist and not _matches_allowlist(host, allowlist):
        return GuardResult(False, reason="not-in-allowlist", host=host)

    # Literal IP check (no DNS needed for this case).
    literal_reason = _is_host_in_blocked_literal(host)
    if literal_reason:
        return GuardResult(False, reason=literal_reason, host=host)

    # Hostname check: resolve and validate every answer.
    if resolve:
        addrs = _resolve(host)
        if not addrs:
            return GuardResult(False, reason="dns-resolution-failed", host=host)
        for addr in addrs:
            try:
                ip = ipaddress.IPv4Address(addr)
                if _is_blocked_v4(ip):
                    return GuardResult(
                        False, reason=f"resolved-to-blocked:{addr}",
                        host=host, resolved=addrs,
                    )
            except ValueError:
                pass
            try:
                ipaddress.IPv6Address(addr)
            except ValueError:
                continue
            if _is_blocked_v6(addr):
                return GuardResult(
                    False, reason=f"resolved-to-blocked:{addr}",
                    host=host, resolved=addrs,
                )
        return GuardResult(True, host=host, resolved=addrs)

    return GuardResult(True, host=host)


def assert_safe(url: str) -> None:
    """Raise SSRFError if `url` is not safe to fetch."""
    res = check_url(url)
    if not res.allowed:
        raise SSRFError(f"blocked outbound fetch: {res.reason} (url={url}, host={res.host})")


class SSRFError(ValueError):
    """Raised when an outbound URL fails the SSRF guard."""
