#!/usr/bin/env bash
# Bootstrap a venv and install the runtime + optional test dependencies.
#
# Idempotent: re-running on an existing venv is a no-op for the venv step.
# Tries the full install first (kuzu + aiohttp_socks + gunicorn), then
# degrades gracefully if a native dep fails to build (e.g. ARM Kali).
#
# Usage:
#   ./install.sh           install everything
#   ./install.sh --minimal install only the minimum required deps
#   ./install.sh --dev     also install test/lint extras
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

MODE="full"
EXTRAS=()
for arg in "$@"; do
    case "$arg" in
        --minimal) MODE="minimal" ;;
        --dev)     EXTRAS+=(dev) ;;
        -h|--help)
            sed -n '2,12p' "$0"
            exit 0
            ;;
    esac
done

PYTHON_BIN="${PYTHON:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "error: $PYTHON_BIN not found. Set PYTHON=/path/to/python and retry." >&2
    exit 1
fi

# 1) Create venv on first run.
if [ ! -d env ]; then
    echo "[install] creating venv at ./env (this is one-time)"
    "$PYTHON_BIN" -m venv env
fi
# shellcheck disable=SC1091
source env/bin/activate

# 2) Pin pip so the resolver behaves the same on every machine.
python3 -m pip install --upgrade pip wheel setuptools

# 3) Two install passes: full first, minimal fallback.
#    We don't want a single Cython build error to leave the user with a
#    half-installed project — better to fall back to a working baseline
#    and tell them what didn't make it.
install_full() {
    python3 -m pip install -e ".[${EXTRAS[*]:+$(IFS=,; echo "${EXTRAS[*]}")}]"
}

install_minimal() {
    # Minimal is enough to run the CLI + web. kuzu is the only one that
    # routinely fails to build on aarch64 / musl — the rest is pure Python.
    python3 -m pip install flask networkx requests pyyaml aiohttp
}

if [ "$MODE" = "minimal" ]; then
    echo "[install] --minimal: installing core only"
    install_minimal
else
    echo "[install] full install (kuzu + aiohttp_socks + gunicorn + console script)"
    if ! install_full 2>install.log; then
        echo "[install] full install failed; falling back to --minimal"
        tail -20 install.log || true
        install_minimal
        echo
        echo "[install] WARNING: kuzu and/or aiohttp_socks are not installed."
        echo "  The engine falls back to in-memory NetworkX without kuzu."
        echo "  Re-run with ./install.sh once the build toolchain is fixed."
    else
        rm -f install.log
    fi
fi

# 4) Sanity check: can we import the core + can the console script be found?
echo
echo "[install] self-check..."
python3 -c "import estorides_core.orchestrator; print('  import: ok')" || {
    echo "  import failed — re-run with --minimal to recover." >&2
    exit 1
}
if command -v estorides >/dev/null 2>&1; then
    echo "  console script: $(command -v estorides)"
else
    echo "  console script: not on PATH (you can still use ./estorides or python3 estorides_cli.py)"
fi

echo
echo "Estorides venv ready. Try:"
echo "  source env/bin/activate"
echo "  estorides status"
echo "  estorides run example.com --only-sources crt_sh_certificates,ipapi_free"
echo "  estorides serve --port 5050          # dev server (loopback)"
echo "  gunicorn -w 4 -b 127.0.0.1:5050 wsgi:app   # production"
echo
echo "Optional: cp .env.example .env and add API keys to enable paid sources."
