#!/usr/bin/env bash
# Tear down the dev stack; named Postgres volume is kept.
set -euo pipefail
cd "$(dirname "$0")/.."

COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME:-cache-dev}
COMPOSE_FILE=${COMPOSE_FILE:-infra/compose/docker-compose.dev.yml}

echo "==> Stopping dev stack (project: $COMPOSE_PROJECT_NAME)"
docker compose \
  --project-name "$COMPOSE_PROJECT_NAME" \
  -f "$COMPOSE_FILE" \
  down --remove-orphans

echo "==> Dev stack stopped."
echo "Drop the Postgres volume with:  docker volume rm cache-dev-postgres-data"