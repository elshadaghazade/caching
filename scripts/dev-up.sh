#!/usr/bin/env bash
# Bring up the local dev stack: Postgres on localhost:5432, FastAPI on localhost:8000.
set -euo pipefail
cd "$(dirname "$0")/.."

COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME:-cache-dev}
COMPOSE_FILE=${COMPOSE_FILE:-infra/compose/docker-compose.dev.yml}

export COMPOSE_PROJECT_NAME

echo "==> Starting dev stack (project: $COMPOSE_PROJECT_NAME, file: $COMPOSE_FILE)"
docker compose \
  --project-name "$COMPOSE_PROJECT_NAME" \
  -f "$COMPOSE_FILE" \
  up --build -d --remove-orphans

echo
echo "==> Dev stack is up."
echo "    Postgres  -> localhost:5432  (user/pass: cache/cache)"
echo "    FastAPI   -> localhost:8000"
echo
echo "Tear down with:  ./scripts/dev-down.sh"
echo "Tail logs with:  docker compose -p $COMPOSE_PROJECT_NAME -f $COMPOSE_FILE logs -f"