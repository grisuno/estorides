# lan_scope — private local scope auto-detection

## Purpose

Derive a safe default LAN scope when the operator leaves scope empty.
Reads local interface addresses and keeps only private local networks.
Public, loopback, multicast, and oversized ranges never become scope.
Pure parsing plus one thin OS reader, kept separate for testability.

## Inputs

- `InterfaceAddr` dict: `{"address": "192.168.1.10", "prefix": 24}`
  or `{"address": "192.168.1.10/24"}`. IPv4 and IPv6 accepted.
- `interfaces: list[InterfaceAddr]` from the OS reader or tests.
- OS reader output: text of `ip -o -f inet addr show` and
  `ip -o -f inet6 addr show`, parsed without sockets or probes.

Ranges: prefix must satisfy IPv4 >= 8, IPv6 >= 32. Anything wider is
dropped to avoid Internet-wide scope.

## Outputs

- `select_private_cidrs(interfaces) -> list[str]`: sorted, deduped
  CIDR strings, private only.
- `default_scope(interfaces) -> str | None`: first CIDR or None when
  no private network exists.
- `parse_interface_addr(raw: dict) -> str | None`: normalized CIDR or
  None when unparsable or not private.

## Error table

| Failure | Code path | Behavior |
|---|---|---|
| unparsable address | `parse_interface_addr` | return None, no raise |
| public address | filter | dropped |
| loopback / multicast / reserved | filter | dropped |
| prefix too wide (< 8 v4, < 32 v6) | filter | dropped |
| empty input | `select/default` | `[]` / None |
| OS reader binary missing | `read_local_interfaces` | return `[]`, no raise |

## Security guarantees

- Default deny: unknown or non-private never enters scope.
- No sockets, no probes, no broadcast. Reader only inspects local
  interface configuration via `ip` binary with argument list, no shell.
- Pure functions never raise on hostile strings; they return None or
  empty.
- IPv6 link-local (`fe80::/10`) and ULA (`fc00::/7`) accepted; global
  unicast dropped.

## Out of scope

- Authorization (belongs to `lan_policy`).
- Device discovery, ARP/DHCP parsing (belongs to `lan_inventory`).
- Graph mutation, exports, web UI.

## Scenarios BDD Given-When-Then

- S1 happy v4: Given `192.168.1.10/24`, When parsed and selected,
  Then scope contains `192.168.1.0/24`.
- S2 happy v6 ULA: Given `fd00::5/64`, When selected, Then scope
  contains the normalized ULA CIDR.
- S3 edge mixed: Given private plus public plus loopback, When
  selected, Then only the private CIDR remains.
- S4 error garbage: Given `not-an-ip`, When parsed, Then None.
- S5 error public: Given `8.8.8.8/24`, When parsed, Then None.
- S6 security wide scope: Given `10.0.0.1/4`, When parsed, Then None.
- S7 empty: Given empty list, When default requested, Then None.
- S8 reader fail-soft: Given missing `ip` binary, When reader runs,
  Then empty list, no exception.
