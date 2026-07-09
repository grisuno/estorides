# `target_management` -- Spec (Modulo 2i)

Purpose
-------

Estorides currently only accepts targets through `/api/run` (full OSINT
query) or `/api/discover/start` (background subdomain extraction). There is
no lightweight way to register a target in the fusion store, tag it, append
it to an existing case, or batch-import multiple targets from a CSV/text
block without triggering a full recon run.

This module fills that gap. It provides a pure, stateless service that:

1. Validates a target's type and value against the entity ontology.
2. Registers the target in the fusion store (cross-run fact base) with
   no run required -- the target is "watched" from the moment it is
   added.
3. Appends the target to an existing case or creates a new case for it.
4. Supports batch import from CSV or plain-text (one per line).
5. Exposes a REST surface through `estorides_web.py` so the UI can
   render a "Targets" management panel.

Inputs
------

### `TargetEntry`

| Field | Type | Range | Notes |
|-------|------|-------|-------|
| `type` | `str` | one of `domain, ipv4, ipv6, email, username, cve, btc_address, eth_address, asn, md5, sha1, sha256, url, phone` | Entity type |
| `value` | `str` | 1-2048 chars | The indicator value |
| `label` | `str` | 0-256 chars | Optional human-readable label |
| `case_id` | `str` or null | valid case id or null | If set, append to this case |

### `BatchInput`

A text block where each line is one of:
- `<type>:<value>` (e.g. `domain:evilcorp.com`)
- `<value>` (type is auto-detected)
- CSV with columns `type,value,label`

### Type validation rules

| Entity type | Validation |
|-------------|------------|
| `domain` | matches `^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$` |
| `ipv4` | matches `^\d{1,3}(\.\d{1,3}){3}$` |
| `ipv6` | matches `^([0-9a-fA-F]{1,4}:){2,7}[0-9a-fA-F]{1,4}$` |
| `email` | matches `^[^\s@]+@[^\s@]+\.[^\s@]+$` |
| `cve` | matches `^CVE-\d{4}-\d{4,}$` |
| `btc_address` | matches `^(1\|3\|bc1)[a-km-zA-HJ-NP-Z1-9]{25,71}$` |
| `eth_address` | matches `^0x[a-fA-F0-9]{40}$` |
| `phone` | matches `^\+[1-9]\d{6,14}$` |
| `asn` | matches `^AS\d{1,10}$` |
| `url` | starts with `http://` or `https://` |
| `username` | 1-128 chars, no spaces |
| `person` | 1-256 chars |
| `company` | 1-256 chars |

### Config

All from the centralized `config.py` -- no hardcoded values.

Outputs
-------

### `TargetResult`

```json
{
  "id": "sha1(type:value)[:16]",
  "type": "domain",
  "value": "evilcorp.com",
  "label": "Primary target",
  "valid": true,
  "validation_errors": [],
  "case_id": "abc123...",
  "created_at": 1700100000.0
}
```

### Batch result

```json
{
  "total": 10,
  "valid": 8,
  "invalid": 2,
  "errors": [{"line": 3, "reason": "invalid type"}],
  "targets": [TargetResult, ...]
}
```

Error table
-----------

| Condition | HTTP | Body |
|-----------|------|------|
| Empty value | 400 | `{"error": "value is required"}` |
| Invalid type | 400 | `{"error": "invalid-type", "valid_types": [...]}` |
| Value fails type validation | 400 | `{"error": "validation-failed", "reason": "..."}` |
| Unknown case_id | 404 | `{"error": "case-not-found"}` |
| Case store unavailable | 503 | `{"error": "case store unavailable"}` |
| Fusion store unavailable | 503 | `{"error": "fusion store unavailable"}` |
| Batch line unparseable | included in response errors | skipped, not rejected |

Security guarantees
-------------------

1. No I/O except through the injected store adapters.
2. Pure validation -- no eval/exec/os.system. Regex-based.
3. Input length bounded (2048 chars per value, 200 items per batch).
4. No logging of sensitive target values at INFO level or above.
5. CSP-safe: API responses are JSON, never HTML.

Out of scope
------------

- Running OSINT queries for the target (that is the orchestrator's job).
- Persistence of target watchlists beyond the fusion store.
- Storing target metadata (tags, notes, status) beyond label.
- Email/push notifications on target changes.

--- BDD scenarios (Given-When-Then) ---

### S1 -- Happy path: single target created

**Given** a valid target type and value
**When** `target_management.add_target("domain", "evilcorp.com")`
**Then** a TargetResult is returned with `valid=True`
**And** `id` is a 16-char hex string
**And** `case_id` is a non-empty string
**And** the fusion store contains an observation for this target

### S2 -- Edge: type auto-detected from value

**Given** a value `"8.8.8.8"` without an explicit type
**When** `target_management.add_target("auto", "8.8.8.8")`
**Then** `type == "ipv4"`
**And** `valid == True`

### S3 -- Edge: invalid value by type

**Given** type `"email"` and value `"not-an-email"`
**When** `target_management.validate_target("email", "not-an-email")`
**Then** `valid == False`
**And** `validation_errors` is non-empty

### S4 -- Edge: unknown type

**Given** type `"alien_artifact"`
**When** `target_management.validate_target("alien_artifact", "x")`
**Then** `valid == False`
**And** `validation_errors` lists valid types

### S5 -- Error: empty value

**Given** an empty value
**When** `target_management.add_target("domain", "")`
**Then** raises `ValueError("value must be non-empty")`

### S6 -- Error: case store unavailable

**Given** case store is None
**When** `target_management.add_target("domain", "test.com", case_store=None)`
**Then** `case_id` is None (ephemeral mode)

### S7 -- Batch: 3 valid + 1 invalid

**Given** a batch text:
```
domain:evilcorp.com
ipv4:8.8.8.8
email:user@example.com
email:not-an-email
```
**When** `target_management.batch_import(text)`
**Then** `result.total == 4`
**And** `result.valid == 3`
**And** `result.invalid == 1`

### S8 -- Security: max batch size enforced

**Given** a batch with 201 lines
**When** `target_management.batch_import(text)`
**Then** raises `ValueError("batch exceeds max size")`

### S9 -- Security: XSS attempt in value is rejected

**Given** type `"domain"` and value `"<script>alert(1)</script>"`
**When** `target_management.validate_target("domain", value)`
**Then** `valid == False`
**And** `validation_errors` contains "invalid domain"

### S10 -- Determinism: same input same output

**Given** two identical calls to `add_target`
**When** both complete
**Then** both return the same `id` and `case_id` (idempotent)

Module close criteria
---------------------

- `pytest tests/test_target_management.py -v` -- green (S1-S10).
- `pytest tests/properties/test_target_management_properties.py -v` -- green.
- `ruff check estorides_core/target_management.py tests/test_target_management.py`
- `mypy --strict estorides_core/target_management.py`
- `bandit -r estorides_core/target_management.py`
- Full suite -- no regressions.
