# `install.sh`

> Source: [install.sh:1](../../install.sh#L1) | language `sh` | coverage 66.7% | [API index](../index.md)

Bootstrap a venv and install the runtime + optional test dependencies.

Idempotent: re-running on an existing venv is a no-op for the venv step. Tries the full install first (kuzu + aiohttp_socks + gunicorn), then degrades gracefully if a native dep fails to build (e.g. ARM Kali).  Usage: ./install.sh           install everything ./install.sh --minimal install only the minimum required deps ./install.sh --dev     also install test/lint extras

## Contents

- **Functions:** [`install_full`](#install_full), [`install_minimal`](#install_minimal)

## Functions

<a id="install_full"></a>

### `install_full`

`function` | [install.sh:51](../../install.sh#L51)

```bash
install_full()
```

3) Two install passes: full first, minimal fallback.

We don't want a single Cython build error to leave the user with a half-installed project — better to fall back to a working baseline and tell them what didn't make it.

---

<a id="install_minimal"></a>

### `install_minimal`

`function` | [install.sh:55](../../install.sh#L55)

```bash
install_minimal()
```

---
