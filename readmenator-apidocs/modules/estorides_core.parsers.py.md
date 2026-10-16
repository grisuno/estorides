# `estorides_core.parsers`

> Source: [estorides_core/parsers.py:1](../../estorides_core/parsers.py#L1) | language `py` | coverage 37.3% | [API index](../index.md)

estorides_core.parsers ====================== A small library of structured parsers.

Each parser knows how to take a raw response from a specific OSINT source and pull out the things the rest of the pipeline cares about: domain, IP, geolocation, etc.

The [`parser`](estorides_core.observation_models.py.md#observation-parser) field of each YAML source selects one of these functions
via the [`PARSERS`](#parsers) registry. New parsers are added with
`@register_parser("name")` or by appending to [`PARSERS`](#parsers) directly.

## Contents

- **Functions:** [`parse_dns_json`](#parse_dns_json), [`parse_crtsh_json`](#parse_crtsh_json), [`parse_rdap`](#parse_rdap), [`parse_ipapi`](#parse_ipapi), [`parse_ipinfo`](#parse_ipinfo), [`parse_ipapi_co`](#parse_ipapi_co), [`parse_shodan_internetdb`](#parse_shodan_internetdb), [`parse_greynoise`](#parse_greynoise), [`parse_ipwhois`](#parse_ipwhois), [`parse_abuseipdb`](#parse_abuseipdb), [`parse_vt_ip`](#parse_vt_ip), [`parse_vt_domain`](#parse_vt_domain), [`parse_vt_file`](#parse_vt_file), [`parse_bgpview`](#parse_bgpview), [`parse_cisa_kev`](#parse_cisa_kev), [`parse_ripe_stat`](#parse_ripe_stat), [`parse_nominatim`](#parse_nominatim), [`parse_urlscan`](#parse_urlscan), [`parse_wayback_cdx`](#parse_wayback_cdx), [`parse_wayback_avail`](#parse_wayback_avail), [`parse_threatfox`](#parse_threatfox), [`parse_urlhaus`](#parse_urlhaus), [`parse_urlhaus_payloads`](#parse_urlhaus_payloads), [`parse_malwarebazaar`](#parse_malwarebazaar), [`parse_otx`](#parse_otx), [`parse_hibp_breach`](#parse_hibp_breach), [`parse_hibp_paste`](#parse_hibp_paste), [`parse_phonebook`](#parse_phonebook), [`parse_wikipedia`](#parse_wikipedia), [`parse_wikidata`](#parse_wikidata), [`parse_openalex`](#parse_openalex), [`parse_crossref`](#parse_crossref), [`parse_arxiv`](#parse_arxiv), [`parse_nvd_cve`](#parse_nvd_cve), [`parse_github_advisories`](#parse_github_advisories), [`parse_blockchain_btc`](#parse_blockchain_btc), [`parse_blockstream`](#parse_blockstream), [`parse_ethplorer`](#parse_ethplorer), [`parse_microlink`](#parse_microlink), [`parse_github_user`](#parse_github_user), [`parse_github_search`](#parse_github_search), [`parse_reddit`](#parse_reddit), [`parse_mastodon`](#parse_mastodon), [`parse_keybase`](#parse_keybase), [`parse_hackernews`](#parse_hackernews), [`parse_reddit_search`](#parse_reddit_search), [`parse_dev_to`](#parse_dev_to), [`parse_text_lines`](#parse_text_lines), [`parse_raw_text`](#parse_raw_text), [`parse_http_headers`](#parse_http_headers), [`parse_whois_text`](#parse_whois_text), [`parse_twitter_user`](#parse_twitter_user), [`parse_youtube_user`](#parse_youtube_user), [`parse_twitch_user`](#parse_twitch_user), [`parse_discord_discovery`](#parse_discord_discovery), [`get_parser`](#get_parser), [`register_parser`](#register_parser), [`list_parsers`](#list_parsers)
- **Constants:** [`PARSERS`](#parsers)

## Functions

<a id="parse_dns_json"></a>

### `parse_dns_json`

`function` | [estorides_core/parsers.py:62](../../estorides_core/parsers.py#L62)

```python
def parse_dns_json(payload: Any) -> dict[str, Any]
```

Google/Cloudflare DNS-over-HTTPS response.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_crtsh_json"></a>

### `parse_crtsh_json`

`function` | [estorides_core/parsers.py:78](../../estorides_core/parsers.py#L78)

```python
def parse_crtsh_json(payload: Any) -> dict[str, Any]
```

crt.sh CT log response.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_rdap"></a>

### `parse_rdap`

`function` | [estorides_core/parsers.py:96](../../estorides_core/parsers.py#L96)

```python
def parse_rdap(payload: Any) -> dict[str, Any]
```

RDAP (RFC 7483) domain object.

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

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_ipapi"></a>

### `parse_ipapi`

`function` | [estorides_core/parsers.py:176](../../estorides_core/parsers.py#L176)

```python
def parse_ipapi(payload: Any) -> dict[str, Any]
```

ip-api.com response.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_ipinfo"></a>

### `parse_ipinfo`

`function` | [estorides_core/parsers.py:202](../../estorides_core/parsers.py#L202)

```python
def parse_ipinfo(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_ipapi_co"></a>

### `parse_ipapi_co`

`function` | [estorides_core/parsers.py:217](../../estorides_core/parsers.py#L217)

```python
def parse_ipapi_co(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_shodan_internetdb"></a>

### `parse_shodan_internetdb`

`function` | [estorides_core/parsers.py:227](../../estorides_core/parsers.py#L227)

```python
def parse_shodan_internetdb(payload: Any) -> dict[str, Any]
```

internetdb.shodan.io — IP service summary.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_greynoise"></a>

### `parse_greynoise`

`function` | [estorides_core/parsers.py:241](../../estorides_core/parsers.py#L241)

```python
def parse_greynoise(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_ipwhois"></a>

### `parse_ipwhois`

`function` | [estorides_core/parsers.py:256](../../estorides_core/parsers.py#L256)

```python
def parse_ipwhois(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_abuseipdb"></a>

### `parse_abuseipdb`

`function` | [estorides_core/parsers.py:274](../../estorides_core/parsers.py#L274)

```python
def parse_abuseipdb(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_vt_ip"></a>

### `parse_vt_ip`

`function` | [estorides_core/parsers.py:304](../../estorides_core/parsers.py#L304)

```python
def parse_vt_ip(payload: Any) -> dict[str, Any]
```

VirusTotal v3 — IP address object.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_vt_domain"></a>

### `parse_vt_domain`

`function` | [estorides_core/parsers.py:325](../../estorides_core/parsers.py#L325)

```python
def parse_vt_domain(payload: Any) -> dict[str, Any]
```

VirusTotal v3 — domain object.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_vt_file"></a>

### `parse_vt_file`

`function` | [estorides_core/parsers.py:352](../../estorides_core/parsers.py#L352)

```python
def parse_vt_file(payload: Any) -> dict[str, Any]
```

VirusTotal v3 — file object.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_bgpview"></a>

### `parse_bgpview`

`function` | [estorides_core/parsers.py:376](../../estorides_core/parsers.py#L376)

```python
def parse_bgpview(payload: Any) -> dict[str, Any]
```

BGPView IP/ASN response (keyless).

Total: never raises.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_cisa_kev"></a>

### `parse_cisa_kev`

`function` | [estorides_core/parsers.py:408](../../estorides_core/parsers.py#L408)

```python
def parse_cisa_kev(payload: Any) -> dict[str, Any]
```

CISA KEV catalog (keyless).

Capped at 20 items. Total: never raises.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_ripe_stat"></a>

### `parse_ripe_stat`

`function` | [estorides_core/parsers.py:427](../../estorides_core/parsers.py#L427)

```python
def parse_ripe_stat(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_nominatim"></a>

### `parse_nominatim`

`function` | [estorides_core/parsers.py:438](../../estorides_core/parsers.py#L438)

```python
def parse_nominatim(payload: Any) -> list[dict[str, Any]]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `list[dict[str, Any]]`

---

<a id="parse_urlscan"></a>

### `parse_urlscan`

`function` | [estorides_core/parsers.py:456](../../estorides_core/parsers.py#L456)

```python
def parse_urlscan(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_wayback_cdx"></a>

### `parse_wayback_cdx`

`function` | [estorides_core/parsers.py:478](../../estorides_core/parsers.py#L478)

```python
def parse_wayback_cdx(payload: Any) -> list[dict[str, Any]]
```

CDX returns a list where the first row is the header.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `list[dict[str, Any]]`

---

<a id="parse_wayback_avail"></a>

### `parse_wayback_avail`

`function` | [estorides_core/parsers.py:493](../../estorides_core/parsers.py#L493)

```python
def parse_wayback_avail(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_threatfox"></a>

### `parse_threatfox`

`function` | [estorides_core/parsers.py:503](../../estorides_core/parsers.py#L503)

```python
def parse_threatfox(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_urlhaus"></a>

### `parse_urlhaus`

`function` | [estorides_core/parsers.py:512](../../estorides_core/parsers.py#L512)

```python
def parse_urlhaus(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_urlhaus_payloads"></a>

### `parse_urlhaus_payloads`

`function` | [estorides_core/parsers.py:521](../../estorides_core/parsers.py#L521)

```python
def parse_urlhaus_payloads(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_malwarebazaar"></a>

### `parse_malwarebazaar`

`function` | [estorides_core/parsers.py:530](../../estorides_core/parsers.py#L530)

```python
def parse_malwarebazaar(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_otx"></a>

### `parse_otx`

`function` | [estorides_core/parsers.py:539](../../estorides_core/parsers.py#L539)

```python
def parse_otx(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_hibp_breach"></a>

### `parse_hibp_breach`

`function` | [estorides_core/parsers.py:564](../../estorides_core/parsers.py#L564)

```python
def parse_hibp_breach(payload: Any) -> list[dict[str, Any]]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `list[dict[str, Any]]`

---

<a id="parse_hibp_paste"></a>

### `parse_hibp_paste`

`function` | [estorides_core/parsers.py:582](../../estorides_core/parsers.py#L582)

```python
def parse_hibp_paste(payload: Any) -> list[dict[str, Any]]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `list[dict[str, Any]]`

---

<a id="parse_phonebook"></a>

### `parse_phonebook`

`function` | [estorides_core/parsers.py:598](../../estorides_core/parsers.py#L598)

```python
def parse_phonebook(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_wikipedia"></a>

### `parse_wikipedia`

`function` | [estorides_core/parsers.py:619](../../estorides_core/parsers.py#L619)

```python
def parse_wikipedia(payload: Any) -> list[dict[str, Any]]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `list[dict[str, Any]]`

---

<a id="parse_wikidata"></a>

### `parse_wikidata`

`function` | [estorides_core/parsers.py:628](../../estorides_core/parsers.py#L628)

```python
def parse_wikidata(payload: Any) -> list[dict[str, Any]]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `list[dict[str, Any]]`

---

<a id="parse_openalex"></a>

### `parse_openalex`

`function` | [estorides_core/parsers.py:640](../../estorides_core/parsers.py#L640)

```python
def parse_openalex(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_crossref"></a>

### `parse_crossref`

`function` | [estorides_core/parsers.py:665](../../estorides_core/parsers.py#L665)

```python
def parse_crossref(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_arxiv"></a>

### `parse_arxiv`

`function` | [estorides_core/parsers.py:685](../../estorides_core/parsers.py#L685)

```python
def parse_arxiv(payload: Any) -> list[dict[str, Any]]
```

arXiv returns Atom XML; we expect callers to have converted to a dict.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `list[dict[str, Any]]`

---

<a id="parse_nvd_cve"></a>

### `parse_nvd_cve`

`function` | [estorides_core/parsers.py:706](../../estorides_core/parsers.py#L706)

```python
def parse_nvd_cve(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_github_advisories"></a>

### `parse_github_advisories`

`function` | [estorides_core/parsers.py:727](../../estorides_core/parsers.py#L727)

```python
def parse_github_advisories(payload: Any) -> list[dict[str, Any]]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `list[dict[str, Any]]`

---

<a id="parse_blockchain_btc"></a>

### `parse_blockchain_btc`

`function` | [estorides_core/parsers.py:752](../../estorides_core/parsers.py#L752)

```python
def parse_blockchain_btc(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_blockstream"></a>

### `parse_blockstream`

`function` | [estorides_core/parsers.py:769](../../estorides_core/parsers.py#L769)

```python
def parse_blockstream(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_ethplorer"></a>

### `parse_ethplorer`

`function` | [estorides_core/parsers.py:785](../../estorides_core/parsers.py#L785)

```python
def parse_ethplorer(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_microlink"></a>

### `parse_microlink`

`function` | [estorides_core/parsers.py:802](../../estorides_core/parsers.py#L802)

```python
def parse_microlink(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_github_user"></a>

### `parse_github_user`

`function` | [estorides_core/parsers.py:822](../../estorides_core/parsers.py#L822)

```python
def parse_github_user(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_github_search"></a>

### `parse_github_search`

`function` | [estorides_core/parsers.py:842](../../estorides_core/parsers.py#L842)

```python
def parse_github_search(payload: Any) -> list[dict[str, Any]]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `list[dict[str, Any]]`

---

<a id="parse_reddit"></a>

### `parse_reddit`

`function` | [estorides_core/parsers.py:857](../../estorides_core/parsers.py#L857)

```python
def parse_reddit(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_mastodon"></a>

### `parse_mastodon`

`function` | [estorides_core/parsers.py:887](../../estorides_core/parsers.py#L887)

```python
def parse_mastodon(payload: Any) -> list[dict[str, Any]]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `list[dict[str, Any]]`

---

<a id="parse_keybase"></a>

### `parse_keybase`

`function` | [estorides_core/parsers.py:903](../../estorides_core/parsers.py#L903)

```python
def parse_keybase(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_hackernews"></a>

### `parse_hackernews`

`function` | [estorides_core/parsers.py:932](../../estorides_core/parsers.py#L932)

```python
def parse_hackernews(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_reddit_search"></a>

### `parse_reddit_search`

`function` | [estorides_core/parsers.py:944](../../estorides_core/parsers.py#L944)

```python
def parse_reddit_search(payload: Any) -> list[dict[str, Any]]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `list[dict[str, Any]]`

---

<a id="parse_dev_to"></a>

### `parse_dev_to`

`function` | [estorides_core/parsers.py:958](../../estorides_core/parsers.py#L958)

```python
def parse_dev_to(payload: Any) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_text_lines"></a>

### `parse_text_lines`

`function` | [estorides_core/parsers.py:973](../../estorides_core/parsers.py#L973)

```python
def parse_text_lines(payload: Any) -> list[str]
```

Generic: split raw_text by newlines, drop empties.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `list[str]`

---

<a id="parse_raw_text"></a>

### `parse_raw_text`

`function` | [estorides_core/parsers.py:984](../../estorides_core/parsers.py#L984)

```python
def parse_raw_text(payload: Any) -> str
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `str`

---

<a id="parse_http_headers"></a>

### `parse_http_headers`

`function` | [estorides_core/parsers.py:992](../../estorides_core/parsers.py#L992)

```python
def parse_http_headers(payload: Any) -> dict[str, str]
```

hackertarget returns text; expect a one-line-per-header response.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, str]`

---

<a id="parse_whois_text"></a>

### `parse_whois_text`

`function` | [estorides_core/parsers.py:1008](../../estorides_core/parsers.py#L1008)

```python
def parse_whois_text(payload: Any) -> dict[str, str]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, str]`

---

<a id="parse_twitter_user"></a>

### `parse_twitter_user`

`function` | [estorides_core/parsers.py:1026](../../estorides_core/parsers.py#L1026)

```python
def parse_twitter_user(payload: Any) -> dict[str, Any]
```

Twitter/X API v2 user by username.

Expects the v2 JSON shape: {"data": {"id": ..., "name": ..., "username": ..., ...}}
Returns flat dict with the core profile fields.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_youtube_user"></a>

### `parse_youtube_user`

`function` | [estorides_core/parsers.py:1062](../../estorides_core/parsers.py#L1062)

```python
def parse_youtube_user(payload: Any) -> dict[str, Any]
```

YouTube Data API v3 channel by handle.

Expects: {"items": [{"id": ..., "snippet": {...}, "statistics": {...}}]}
Returns a flat profile dict with channel metadata.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_twitch_user"></a>

### `parse_twitch_user`

`function` | [estorides_core/parsers.py:1099](../../estorides_core/parsers.py#L1099)

```python
def parse_twitch_user(payload: Any) -> dict[str, Any]
```

Twitch Helix API user by login.

Expects: {"data": [{"id": ..., "login": ..., "display_name": ..., ...}]}
Returns a flat profile dict with core Twitch metadata.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="parse_discord_discovery"></a>

### `parse_discord_discovery`

`function` | [estorides_core/parsers.py:1132](../../estorides_core/parsers.py#L1132)

```python
def parse_discord_discovery(payload: Any) -> dict[str, Any]
```

Discord server discovery via discords.com API.

Expected shape: a list of server dicts with name, description,
member_count, etc. Or a dict with a 'results' or 'servers' key.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `Any` |  |  |

**Returns:** `dict[str, Any]`

---

<a id="get_parser"></a>

### `get_parser`

`function` | [estorides_core/parsers.py:1251](../../estorides_core/parsers.py#L1251)

```python
def get_parser(name: str) -> ParserFunc
```

Return the parser function for `name`, or a passthrough lambda.

Unknown parser names deliberately fall through to [`parse_raw_text`](#parse_raw_text)
so a source YAML with a typo in the [`parser`](estorides_core.observation_models.py.md#observation-parser) field never crashes
the run — it just produces a less-structured observation.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |

**Returns:** `ParserFunc`

*Called by:* [`parse_tool_output`](estorides_core.system_app_sources.py.md#parse_tool_output)

---

<a id="register_parser"></a>

### `register_parser`

`function` | [estorides_core/parsers.py:1264](../../estorides_core/parsers.py#L1264)

```python
def register_parser(name: str, description: str = '') -> ParserFunc
```

Decorator: register `func` as a parser under `name`.

Used by addon authors and tests to extend the catalog without
touching the central [`PARSERS`](#parsers) dict. Idempotent: re-registering
the same name overwrites the previous entry, with a debug log so
a typo doesn't silently drop a parser.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` |  |  |
| `description` | `str` | `''` |  |

**Returns:** `ParserFunc`

---

<a id="list_parsers"></a>

### `list_parsers`

`function` | [estorides_core/parsers.py:1280](../../estorides_core/parsers.py#L1280)

```python
def list_parsers() -> list[tuple[str, str]]
```

Return (name, description) tuples for every registered parser.

Used by the CLI `status` endpoint to advertise the available
parser names, and by tests to assert that a custom parser made it
into the registry.

**Returns:** `list[tuple[str, str]]`

---

## Constants

<a id="parsers"></a>

### `PARSERS`

`constant` | [estorides_core/parsers.py:1168](../../estorides_core/parsers.py#L1168)

```python
PARSERS
```

---
