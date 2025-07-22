#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Run the Dash test‑suite inside the project venv.
# Exits 0 if all tests pass, 1 (or Pytest’s own non‑zero code) otherwise.
# ---------------------------------------------------------------------------

set -e # stop on first error
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Locate & activate the virtual environment
VENV_DIR="$PROJECT_ROOT/venv"

if [[ ! -d "$VENV_DIR" ]]; then
  echo "Virtual environment not found at $VENV_DIR" >&2
  exit 1
fi

# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

# Run the test‑suite
echo "▶️  Running Pytest…"
pytest -q
STATUS=$?

# Tear down & propagate status
deactivate
exit "$STATUS"
