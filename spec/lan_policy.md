# lan_policy — LAN scan authorization and contact ceiling

## Purpose

Single source of truth for LAN scan authorization. This module decides
whether a local network discovery run may proceed and which contact
classes it may use. It governs every LAN tool and every LAN source so
the web checkbox for active scanning and the blocking consent gate have
one enforcement point. No tool runs without passing through this policy.

## Inputs

- `LanPolicyRequest` (dict or dataclass fields):
  - `consent: bool` — operator confirmed ownership or written permission.
    Required True. Any other value blocks.
  - `allow_active: bool` — state of the web checkbox "Allow active
    scanning". Default False.
  - `scope_cidr: str | None` — target network in CIDR notation, for
    example `192.168.1.0/24`. Optional at policy level; validated when
    present.
  - `requested_contact: str` — highest contact class the caller wants:
    one of `none`, `broker`, `active`. Default `none`.
- Environment: `ESTORIDES_LAN_ALLOW_ACTIVE` (bool, default True) is
  the server-side kill-switch. The effective permission is
  `allow_active AND env_ceiling`. Authorization rests on the
  blocking consent modal plus the explicit checkbox (double opt-in);
  set the flag to 0 to force passive-only on shared servers.

Types: booleans are strict. Truthy strings such as `"true"` do not
count as True and are rejected to blocked state.

## Outputs

- `LanPolicyDecision` (frozen dataclass, JSON serializable via
  `to_dict()`):
  - `allowed: bool`
  - `max_contact: str` — one of `none`, `broker`, `active`.
  - `active_permitted: bool` — True only when consent is True and both
    checkbox and env ceiling permit active.
  - `block_reason: str | None` — machine readable code when blocked:
    `consent_required`, `scope_invalid`, `contact_denied`.
  - `message: str` — human readable explanation, English, no emojis.
  - `scope_cidr: str | None` — normalized CIDR or None.

JSON schema:

```json
{
  "allowed": "boolean",
  "max_contact": "enum[none,broker,active]",
  "active_permitted": "boolean",
  "block_reason": "string|null",
  "message": "string",
  "scope_cidr": "string|null"
}
```

## Error table

| Failure | Code | Message | Behavior |
|---|---|---|---|
| consent missing or not True | `consent_required` | `LAN scan blocked: explicit ownership or written permission is required.` | `allowed=False`, `max_contact=none` |
| scope present but not valid CIDR | `scope_invalid` | `LAN scan blocked: scope_cidr is not a valid IPv4/IPv6 CIDR.` | `allowed=False` |
| scope is public or loopback range | `scope_invalid` | `LAN scan blocked: scope must be a private local network.` | `allowed=False` |
| requested active without permission | `contact_denied` | `Active scanning is disabled: enable the checkbox and server policy.` | `allowed=False` for active-only runs; passive still allowed when consent holds |
| unknown contact string | `contact_denied` | `Unknown contact class, treated as active and denied.` | deny active, cap to `none` |

## Security guarantees

- Default deny. Consent False blocks everything, including passive.
- Active requires triple gate: consent True AND checkbox True AND env
  ceiling True. Any False denies active.
- Unknown contact strings map to `active` severity, never downgrade.
- Scope validation rejects non-CIDR, public ranges, loopback,
  multicast, and oversized scopes (prefix shorter than /8 for IPv4 or
  /32 for IPv6 is rejected to avoid Internet-wide scans).
- Pure function. No I/O, no sockets, no subprocess, no env writes.
  Only reads `ESTORIDES_LAN_ALLOW_ACTIVE` through envutil.
- No `eval`, no `exec`, no dynamic import, no shell.

## Out of scope

- Tool execution (belongs to `tool_runner` and the future
  `lan_inventory` module).
- Packet capture, ARP parsing, DHCP parsing (future `lan_inventory`).
- Graph mutation, STIX export, output directory layout (future
  `lan_bundle`).
- Web rendering (the checkbox and modal consume this module, they do
  not live here).
- LazyOwn bridge changes.

## Scenarios BDD Given-When-Then

- S1 happy passive: Given consent True, allow_active False, and
  requested_contact none, When evaluate is called, Then allowed is True
  and max_contact is none.
- S2 happy active triple gate: Given consent True, checkbox True, env
  ceiling True, and requested_contact active, When evaluate is called,
  Then allowed is True and active_permitted is True.
- S3 edge checkbox without env ceiling: Given consent True, checkbox
  True, env ceiling False, and requested active, When evaluate is
  called, Then allowed is False with code contact_denied.
- S4 edge valid private scope: Given consent True and scope
  `192.168.1.0/24`, When evaluate is called, Then allowed is True and
  scope_cidr echoes normalized.
- S5 error no consent: Given consent False, When evaluate is called,
  Then allowed is False with code consent_required even for passive.
- S6 error public scope: Given consent True and scope `8.8.8.0/24`,
  When evaluate is called, Then allowed is False with code
  scope_invalid.
- S7 security truthy string: Given consent `"yes"` as string, When
  evaluate is called, Then allowed is False with code consent_required.
- S8 security unknown contact: Given requested_contact `hyperactive`,
  When evaluate is called, Then active is denied and max_contact caps
  to none.

## Contracts

- `evaluate(request) -> LanPolicyDecision` never raises on bad input;
  bad input yields a blocked decision.
- `max_contact_for(allow_active: bool, consent: bool) -> str` returns
  `active` only on triple gate, else `none`.
- `requires_consent() -> str` returns the canonical consent notice in
  English used by the blocking modal.
