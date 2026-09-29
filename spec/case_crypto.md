# case_crypto — Spec

## Purpose
I protect operator notes and analysis at rest when the operator opts in. Single user local threat model: stolen laptop or disk image. No Vault, no KMS, no multi user. Plaintext stays default so existing installs keep working.

## Inputs
- `ESTORIDES_CASE_KEY` env: Fernet urlsafe base64 key (`Fernet.generate_key()`). Absent or empty means disabled.
- `get_cipher()` returns a Fernet-like object or None when disabled or when `cryptography` is absent.
- `encrypt_text(plain)` and `decrypt_text(token)` operate on str and return str.

## Outputs
- `CaseStore` writes `notes` and `analysis_json` encrypted with `gAAAA...` prefix when enabled, plaintext otherwise.
- `get_case` and `search_cases` transparently decrypt on read. A row written plaintext still reads after enabling.
- `crypto_status()` reports `{"enabled": bool, "backend": "fernet"|"missing"|"disabled"}`.

## Error table
| Condition | Behaviour |
|---|---|
| key malformed | disabled + warning log, writes stay plaintext, never raise |
| `cryptography` missing | disabled + warning, plaintext, never raise |
| token corrupt on read | return placeholder `"[decrypt-error]"`, log warning, never raise |
| empty string | stored as empty, no encrypt call |

## Security guarantees
- Key never logged, never stored in DB, read only from env at call time so rotation needs only process restart.
- No eval, no shell, parameterized SQL unchanged. Ciphertext goes through the same `?` placeholders.
- Plaintext query column stays searchable by design; documented as not encrypted.

## Out of scope
- Vault, KMS, per case keys, password KDF, encrypting query or indexed columns, key rotation history.

## BDD scenarios
- Given no env key, when creating a case with notes, then DB stores plaintext and `crypto_status().enabled` is False.
- Given a valid key, when writing notes and analysis, then DB holds `gAAAA` tokens and `get_case` returns originals.
- Given a bad key, when writing, then it falls back to plaintext and never raises.
- Given mixed rows, when reading after enabling, then plaintext rows still read and encrypted rows decrypt.
- Given tampered token, when reading, then it returns `[decrypt-error]` without raising.
