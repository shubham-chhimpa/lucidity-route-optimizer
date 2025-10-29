#!/usr/bin/env bash
set -euo pipefail

# Docker-friendly test runner for BestRoute
# Usage examples (from host):
#   docker run --rm -v "$(pwd)":/code -w /code python:3.10-slim bash scripts/test.sh
#   docker compose run --rm api bash scripts/test.sh
# Environment overrides:
#   TEST_PATH            - path to tests (default: tests/unit)
#   PYTEST_ADDOPTS       - extra pytest flags (default: '')
#   MARKEXPR             - pytest -m expression to select markers (default: '')

ROOT_DIR="/code"
cd "$ROOT_DIR"

TEST_PATH=${TEST_PATH:-tests/unit}
PYTEST_ADDOPTS=${PYTEST_ADDOPTS:-}
MARKEXPR=${MARKEXPR:-}

# Ensure pip is up to date and deps are installed (idempotent)
python -m pip install --upgrade pip >/dev/null 2>&1 || true
if [[ -f requirements.txt ]]; then
  pip install --no-cache-dir -r requirements.txt
fi

# Build pytest command (unit tests only, no coverage)
CMD=("python" "-m" "pytest" "$TEST_PATH")

# Apply marker filter if provided
if [[ -n "$MARKEXPR" ]]; then
  CMD+=("-m" "$MARKEXPR")
fi

# Append any extra options
if [[ -n "$PYTEST_ADDOPTS" ]]; then
  # shellcheck disable=SC2206
  EXTRA_OPTS=( $PYTEST_ADDOPTS )
  CMD+=("${EXTRA_OPTS[@]}")
fi

echo "Running: ${CMD[*]}"
exec "${CMD[@]}"
