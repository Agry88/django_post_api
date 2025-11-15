#!/bin/bash
set -e

echo "Running migrations..."
uv run python main.py migrate --noinput

echo "Creating superuser if not exists..."
uv run python main.py createsuperuser_if_not_exists

echo "Starting server..."
exec "$@"

