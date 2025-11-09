#!/bin/bash
set -e

echo "Running migrations..."
uv run python main.py migrate --noinput

echo "Starting server..."
exec "$@"

