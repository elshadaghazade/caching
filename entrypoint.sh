#!/usr/bin/env bash

set -euo pipefail
alembic upgrade head

uvicorn src.main:app --host 0.0.0.0 --port 8000