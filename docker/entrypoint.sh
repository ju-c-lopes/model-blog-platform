#!/bin/bash
set -euo pipefail

export HOME="${HOME:-/app}"
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-/app/.config}"
export POETRY_CACHE_DIR="${POETRY_CACHE_DIR:-/app/.cache/poetry}"
mkdir -p "${XDG_CONFIG_HOME}" "${POETRY_CACHE_DIR}"

cd /app

poetry config virtualenvs.in-project true

if [ "${SKIP_POETRY_INSTALL:-0}" != "1" ]; then
    if [ -f pyproject.toml ]; then
        echo "Installing Poetry dependencies into /app/.venv (bind-mounted project)..."
        poetry install --no-interaction --no-ansi
    else
        echo "Warning: pyproject.toml not found; skipping poetry install."
    fi
fi

export PATH="/app/.venv/bin:${PATH}"

exec "$@"
