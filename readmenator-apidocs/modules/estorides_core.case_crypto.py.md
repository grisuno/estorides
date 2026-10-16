# `estorides_core.case_crypto`

> Source: [estorides_core/case_crypto.py:1](../../estorides_core/case_crypto.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

estorides_core.case_crypto ========================== Opt in field encryption for case notes and analysis at rest.

I read a Fernet key from ESTORIDES_CASE_KEY only. Absent, malformed
or missing backend means disabled and plaintext. I never raise on
crypto failure and I never log the key.

## Contents

- **Functions:** [`crypto_status`](#crypto_status), [`encrypt_text`](#encrypt_text), [`decrypt_text`](#decrypt_text)

## Functions

<a id="crypto_status"></a>

### `crypto_status`

`function` | [estorides_core/case_crypto.py:36](../../estorides_core/case_crypto.py#L36)

```python
def crypto_status() -> dict[str, Any]
```

Report whether field encryption is active and why.

**Returns:** `dict[str, Any]`

---

<a id="encrypt_text"></a>

### `encrypt_text`

`function` | [estorides_core/case_crypto.py:50](../../estorides_core/case_crypto.py#L50)

```python
def encrypt_text(plain: str) -> str
```

Encrypt plain text when enabled else return it unchanged.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `plain` | `str` |  |  |

**Returns:** `str`

*Called by:* [`CaseStore.create_case`](estorides_core.cases.py.md#casestore-create_case), [`CaseStore.finalise`](estorides_core.cases.py.md#casestore-finalise), [`CaseStore.set_notes`](estorides_core.cases.py.md#casestore-set_notes)

---

<a id="decrypt_text"></a>

### `decrypt_text`

`function` | [estorides_core/case_crypto.py:65](../../estorides_core/case_crypto.py#L65)

```python
def decrypt_text(token: str) -> str
```

Decrypt a token, passing through plaintext and errors safely.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `token` | `str` |  |  |

**Returns:** `str`

---
