"""
estorides_core.lan_policy
=========================
Authorization and contact ceiling for LAN discovery runs.

Single enforcement point for the web active-scan checkbox and the
blocking consent gate. Pure: no I/O, no sockets, no subprocess.
"""
from __future__ import annotations

import ipaddress
from dataclasses import asdict, dataclass
from typing import Any

from .envutil import env_bool

LAN_ALLOW_ACTIVE_ENV = "ESTORIDES_LAN_ALLOW_ACTIVE"

VALID_CONTACTS = ("none", "broker", "active")

CONSENT_NOTICE = (
    "Local network scanning may only run on networks you own or where "
    "you hold explicit written permission from the network owner. "
    "Unauthorized scanning may violate local law and acceptable use "
    "policies. Confirm ownership or permission before continuing."
)


@dataclass(frozen=True)
class LanPolicyRequest:
    """Caller intent for a LAN discovery run."""

    consent: Any = False
    allow_active: Any = False
    scope_cidr: str | None = None
    requested_contact: str = "none"


@dataclass(frozen=True)
class LanPolicyDecision:
    """Outcome of policy evaluation. JSON serializable via to_dict."""

    allowed: bool
    max_contact: str
    active_permitted: bool
    block_reason: str | None
    message: str
    scope_cidr: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def requires_consent() -> str:
    """Return the canonical consent notice for the blocking modal."""
    return CONSENT_NOTICE


def _env_ceiling() -> bool:
    # Default allow: authorization is the blocking consent modal plus
    # the explicit checkbox (double opt-in). The env flag is a server
    # kill-switch (set 0 to force passive), not a second lock.
    return env_bool(LAN_ALLOW_ACTIVE_ENV, True)


def _strict_bool(value: Any) -> bool:
    return value is True


def _normalize_scope(raw: str | None) -> tuple[str | None, str | None]:
    """Validate scope CIDR. Returns (normalized, error_code)."""
    if raw is None:
        return None, None
    text = raw.strip() if isinstance(raw, str) else ""
    if not text:
        return None, None
    try:
        net = ipaddress.ip_network(text, strict=False)
    except ValueError:
        return None, "scope_invalid"
    if net.is_loopback or net.is_multicast or net.is_reserved:
        return None, "scope_invalid"
    if isinstance(net, ipaddress.IPv4Network):
        if not net.is_private:
            return None, "scope_invalid"
        if net.prefixlen < 8:
            return None, "scope_invalid"
    else:
        if not (net.is_private or net.is_link_local or net.is_site_local):
            if not str(net.network_address).lower().startswith(("fd", "fc")):
                return None, "scope_invalid"
        if net.prefixlen < 32:
            return None, "scope_invalid"
    return str(net), None


def max_contact_for(allow_active: bool, consent: bool) -> str:
    """Return active only on the triple gate, else none."""
    if consent is True and allow_active is True and _env_ceiling():
        return "active"
    return "none"


def evaluate(request: LanPolicyRequest) -> LanPolicyDecision:
    """Evaluate a LAN policy request. Never raises on bad input."""
    try:
        consent_ok = _strict_bool(request.consent)
    except Exception:
        consent_ok = False
    if not consent_ok:
        return LanPolicyDecision(
            allowed=False,
            max_contact="none",
            active_permitted=False,
            block_reason="consent_required",
            message="LAN scan blocked: explicit ownership or written "
            "permission is required.",
            scope_cidr=None,
        )
    scope_norm, scope_err = _normalize_scope(request.scope_cidr)
    if scope_err is not None:
        return LanPolicyDecision(
            allowed=False,
            max_contact="none",
            active_permitted=False,
            block_reason=scope_err,
            message="LAN scan blocked: scope must be a private local "
            "network in CIDR notation.",
            scope_cidr=None,
        )
    raw_contact = (
        request.requested_contact.strip().lower()
        if isinstance(request.requested_contact, str)
        else ""
    )
    if raw_contact not in VALID_CONTACTS:
        return LanPolicyDecision(
            allowed=False,
            max_contact="none",
            active_permitted=False,
            block_reason="contact_denied",
            message="Unknown contact class, treated as active and denied.",
            scope_cidr=scope_norm,
        )
    checkbox = _strict_bool(request.allow_active)
    ceiling = max_contact_for(checkbox, True)
    active_permitted = ceiling == "active"
    if raw_contact == "active" and not active_permitted:
        return LanPolicyDecision(
            allowed=False,
            max_contact="none",
            active_permitted=False,
            block_reason="contact_denied",
            message="Active scanning is disabled: enable the checkbox "
            "and server policy.",
            scope_cidr=scope_norm,
        )
    if raw_contact == "broker" and not active_permitted:
        capped: str = "none"
        return LanPolicyDecision(
            allowed=True,
            max_contact=capped,
            active_permitted=False,
            block_reason=None,
            message="LAN scan permitted with passive contact only.",
            scope_cidr=scope_norm,
        )
    final_contact = raw_contact if raw_contact != "broker" else "none"
    if raw_contact == "active":
        final_contact = "active"
    return LanPolicyDecision(
        allowed=True,
        max_contact=final_contact,
        active_permitted=active_permitted,
        block_reason=None,
        message="LAN scan permitted.",
        scope_cidr=scope_norm,
    )
