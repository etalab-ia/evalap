#!/bin/bash
set -e

# Run database migrations
echo "Running database migrations..."
alembic -c evalap/api/alembic.ini upgrade head

# Seed the database with initial datasets
echo "Seeding database with initial datasets..."
python -m evalap.scripts.run_seed_data || true

# Start uvicorn server
echo "Starting uvicorn server..."
uvicorn evalap.api.main:app --host 0.0.0.0 --port 8000 --workers 4
