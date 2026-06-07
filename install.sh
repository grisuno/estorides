#!/bin/bash
# Bootstrap a venv and install the runtime + optional test dependencies.
# Idempotent: re-running on an existing venv is a no-op for the venv step.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d env ]; then
    python3 -m venv env
fi
# shellcheck disable=SC1091
source env/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo
echo "Estorides venv ready. Try:"
echo "  source env/bin/activate"
echo "  python3 estorides_cli.py status"
echo "  python3 _validate.py   # full self-test (~10s)"
