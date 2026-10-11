"""
estorides_core.lan_web
======================
Backend guard for LAN discovery runs from the web layer.

Thin mapping over lan_policy: the route hands the request body to
guard() and returns the verdict status on denial. Pure, no I/O.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from . import lan_policy


@dataclass(frozen=True)
class LanWebVerdict:
    """HTTP-ready outcome of the LAN consent gate."""

    permitted: bool
    status: int
    error: str | None
    message: str
    max_contact: str
    scope_cidr: str | None = None
    notice: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_response(self) -> tuple[dict[str, Any], int]:
        """Return (body, status) for the Flask route."""
        if self.permitted:
            body: dict[str, Any] = {
                "max_contact": self.max_contact,
                "scope_cidr": self.scope_cidr,
            }
            if self.notice is not None:
                body["notice"] = self.notice
                body["message"] = self.message
            return (body, self.status)
        return (
            {"error": self.error or "lan-denied",
             "message": self.message},
            self.status,
        )


def is_lan_request(body: Any, query: str = "") -> bool:
    """True when a run targets the local network. Never raises."""
    try:
        if isinstance(body, dict):
            for key in ("lan_consent", "allow_active", "scope_cidr"):
                if key in body:
                    return True
            scope = body.get("scope_cidr")
            if isinstance(scope, str) and scope.strip():
                return True
        text = query.strip() if isinstance(query, str) else ""
        if not text:
            return False
        import ipaddress as _ip

        try:
            net = _ip.ip_network(text, strict=False)
        except ValueError:
            try:
                addr = _ip.ip_address(text)
            except ValueError:
                return False
            return addr.is_private and not addr.is_loopback
        if net.is_loopback or net.is_multicast or net.is_reserved:
            return True
        return net.is_private or net.prefixlen <= 32
    except Exception:
        return False


def scope_payload(interfaces: Any) -> dict[str, Any]:
    """Build the scope response from interface addresses. Never raises."""
    try:
        from . import lan_scope as _scope

        items = interfaces if isinstance(interfaces, list) else []
        cidrs = _scope.select_private_cidrs(items)
    except Exception:
        cidrs = []
    return {"cidrs": cidrs, "scope": cidrs[0] if cidrs else None}


def guard(body: Any) -> LanWebVerdict:
    """Validate a run request body for LAN consent. Never raises."""
    if not isinstance(body, dict):
        return LanWebVerdict(
            permitted=False,
            status=403,
            error="lan-consent-required",
            message="LAN scan blocked: explicit ownership or written "
            "permission is required.",
            max_contact="none",
            scope_cidr=None,
        )
    requested = body.get("requested_contact", "none")
    if requested is None:
        requested = "none"
    req = lan_policy.LanPolicyRequest(
        consent=body.get("lan_consent", False),
        allow_active=body.get("allow_active", False),
        scope_cidr=body.get("scope_cidr"),
        requested_contact=str(requested),
    )
    try:
        decision = lan_policy.evaluate(req)
    except Exception:
        return LanWebVerdict(
            permitted=False,
            status=403,
            error="lan-consent-required",
            message="LAN scan blocked: explicit ownership or written "
            "permission is required.",
            max_contact="none",
            scope_cidr=None,
        )
    if decision.allowed:
        return LanWebVerdict(
            permitted=True,
            status=200,
            error=None,
            message=decision.message,
            max_contact=decision.max_contact,
            scope_cidr=decision.scope_cidr,
        )
    if decision.block_reason == "scope_invalid":
        return LanWebVerdict(
            permitted=False,
            status=400,
            error="lan-scope-invalid",
            message=decision.message,
            max_contact="none",
            scope_cidr=None,
        )
    if decision.block_reason == "contact_denied":
        # Degrade, never refuse: the checkbox caps the ceiling, it does
        # not gate the run. Active tools stay off, passive still runs,
        # and the UI shows the notice as a warning.
        return LanWebVerdict(
            permitted=True,
            status=200,
            error=None,
            message="Active scanning unavailable (server policy); "
            "running passive-only. Set ESTORIDES_LAN_ALLOW_ACTIVE=1 "
            "to enable active tools.",
            max_contact="none",
            scope_cidr=decision.scope_cidr,
            notice="active-unavailable",
        )
    return LanWebVerdict(
        permitted=False,
        status=403,
        error="lan-consent-required",
        message=decision.message,
        max_contact="none",
        scope_cidr=None,
    )
