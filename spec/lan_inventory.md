# lan_inventory — passive-first LAN device inventory

## Purpose

Turn local, already-available network state into a device inventory
without touching the wire. Parses ARP/neighbor tables and DHCP leases,
normalizes MAC and IP identities, and merges sightings into one device
per physical host. Active Kali tools (nmap, arp-scan, nbtscan,
snmpwalk, enum4linux, smbclient) enrich the same devices only when
`lan_policy` permits active contact.

## Inputs

- `parse_arp_table(text: str)`: text of `ip neigh show` or
  `/proc/net/arp`. Lines with IP plus MAC.
- `parse_dhcp_leases(text: str)`: dnsmasq lease file lines
  `expiry mac ip hostname clientid`.
- `parse_nmap_xml(text: str)`: nmap `-oX` output. Hosts with
  `status state="up"` yield sightings with ipv4/ipv6, MAC, vendor
  as hostname hint, and OS guesses ignored.
- `parse_nmap_grepable(text: str)`: nmap `-oG -` output. `Host:`
  lines with `Status: Up` yield sightings; `MAC Address:` trailing
  fields attach MAC and vendor.
- `parse_active_output(text, source)`: format dispatch. XML
  (leading `<`) wins, greppable (`Host:` lines) second, raw
  neighbor lines last. Every sighting tagged with `source`.
- `merge_devices(sightings: list[dict])`: each sighting
  `{"ip": str|None, "mac": str|None, "hostname": str|None,
  "source": str}`.
- MAC formats accepted: colon, hyphen, Cisco dot. Case insensitive.
- IP accepted: valid IPv4 or IPv6, private or link-local. Public and
  garbage dropped.

## Outputs

- `LanDevice` frozen dataclass: `device_id`, `ips: tuple`,
  `mac: str|None`, `hostnames: tuple`, `sources: tuple`.
  `device_id` is `mac:<norm>` when MAC known, else `ip:<ip>`.
  JSON serializable via `to_dict()`.
- `parse_*` return `list[dict]` sightings, never raise.
- `merge_devices` returns `list[LanDevice]` sorted by device_id.
- `device_to_entities(device) -> list[dict]`: graph-ready entities
  (`mac`, `ipv4`/`ipv6`, `hostname` as domain type) with source tags.
- `contact_for_tool(tool: str) -> str`: `none` for local readers
  (`ip-neigh`, `dhcp-leases`, `mdns-listen`, `ssdp-listen`),
  `active` for `nmap`, `arp-scan`, `nbtscan`, `netdiscover`,
  `snmpwalk`, `enum4linux`, `smbclient`, `ncat`, `socat`. Unknown
  maps to `active` (never downgrade).

## Error table

| Failure | Behavior |
|---|---|
| garbage line | skipped, no raise |
| invalid MAC | sighting kept without MAC when IP valid |
| invalid or public IP | sighting dropped |
| empty input | `[]` |
| duplicate sightings | merged, sources union, order stable |

## Security guarantees

- Pure parsing. No sockets, no subprocess, no file reads inside
  parsers. Readers live outside this module.
- XML parsing goes through `defusedxml` (declared dependency),
  plus a 2 MB input cap, outright DOCTYPE/ENTITY rejection, and
  fail-soft error handling. Billion-laughs style entity expansion
  cannot exhaust memory.
- MAC normalization validates octets; no regex backtracking risk
  (bounded patterns only).
- Public IPs never become devices; scope filtering stays in
  `lan_policy`/`lan_scope`.
- No `eval`/`exec`, no shell, no dynamic import.

## Out of scope

- Authorization (`lan_policy`), scope detection (`lan_scope`).
- Tool execution, packet capture, graph writes, exports, web UI.
- Vendor OUI database (hostname only; OUI is a future module).

## Scenarios BDD Given-When-Then

- S1 happy arp: Given `ip neigh` lines with reachable entries, When
  parsed, Then sightings carry normalized MAC and IP.
- S2 happy dhcp: Given dnsmasq lease lines, When parsed, Then hostname
  attaches to the same MAC.
- S3 edge merge: Given ARP sighting plus DHCP sighting with same MAC
  and different IPs, When merged, Then one device with both IPs and
  union sources.
- S4 edge no-mac: Given two sightings with same IP and no MAC, When
  merged, Then one `ip:` device.
- S10 cross-source fold: Given an `ip:` sighting from nmap and a
  `mac:` sighting from passive sharing the same IP, When merged,
  Then one `mac:` device with union IPs, hostnames, and sources.
- S5 error garbage: Given random text, When parsed, Then empty.
- S6 error public: Given public IP with valid MAC, When parsed, Then
  dropped.
- S7 security mac formats: Given hyphen and Cisco dot MACs, When
  normalized, Then identical colon lowercase.
- S8 contact map: Given `nmap`, When mapped, Then `active`; Given
  `ip-neigh`, When mapped, Then `none`; Given unknown, Then `active`.
- S10 nmap XML: Given `-oX` with two hosts up (one with MAC and
  vendor), When parsed, Then two sightings with normalized MAC.
- S11 nmap greppable: Given `-oG` with `Status: Up` hosts, When
  parsed, Then hosts down are skipped and MACs attach.
- S12 dispatch: Given XML text, When dispatched with source `nmap`,
  Then XML sightings tagged `nmap`; given greppable, Then greppable
  sightings; given neighbor lines, Then arp sightings.
- S13 hostile XML: Given 3 MB of entity expansion noise, When parsed,
  Then empty, no exception, bounded time.
