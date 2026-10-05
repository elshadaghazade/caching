# Caching Service

A small FastAPI service that takes a list of input strings, "transforms" each one
through a (simulated) external call, and caches the result so repeated requests
hit the cache instead of the slow path. The transform itself is a stand-in
(`asyncio.sleep` + `str.upper()`); the point of the service is the cache layer.

## Endpoints

- `POST /payload` — body is `{"key": ["str1", "str2", ...], ...}` (one or more
  lists). Each string is transformed; duplicates inside the request are
  deduped. The response is `{"id": <int>}`.
- `GET /{id}` — returns the deduplicated, transformed strings for a previous
  POST, joined with `, `.

Example:

```bash
# POST a payload, get an id back
curl -s -X POST http://localhost:8000/payload \
  -H 'content-type: application/json' \
  -d '{"a": ["foo", "bar"], "b": ["foo", "qux"]}'
# → {"id": 1, "message": "payload created"}

# Read it later by id
curl -s http://localhost:8000/payload/1
# → {"output": "FOO, BAR, QUX"}
```

## Run with Docker (dev stack)

```bash
./scripts/dev-up.sh        # postgres on :5432, cache-api on :8000
./scripts/dev-down.sh      # stop; the named volume is kept
```

Both scripts accept `COMPOSE_PROJECT_NAME` / `COMPOSE_FILE` overrides. Logs:

```bash
docker compose -p cache-dev -f infra/compose/docker-compose.dev.yml logs -f
```

## Run without Docker

```bash
uv sync                                    # install deps into .venv
DATABASE_URL=postgresql+psycopg_async://cache:cache@localhost:5432/cache \
  uv run alembic upgrade head
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Tests assume a Postgres reachable via the URL the app uses, with the migrations
applied.

## CLI

`cache-cli` posts a payload N times and reports per-call elapsed time.

```bash
uv run cache-cli --host http://localhost:8000 --repeat 5 --json '{"a":["x","y"]}'
# → {"id": 7, "elapsed": 0.512}

uv run cache-cli --host http://localhost:8000 --repeat 3 \
  --input path/to/body.json --output results.json
```

- `--input` / `--output` default to `-` (stdin / stdout).
- `--json <string>` sends the body inline (overrides `--input`).
- `--repeat N` runs the request N times; output is a list of `{id, elapsed}`
  dicts when N > 1.

## How the cache works

Three tables back the service:

| Table | Shape | Purpose |
|---|---|---|
| `string_cache` | `string_hash PK → transformed_string` | One row per distinct input string. Hides the slow transform on second-and-hits. |
| `list_cache` | `list_hash PK → transformed[]` | One row per distinct input list. Saves both the per-string lookups and the assembly. |
| `transforms` | `id PK → transformed[]` | One row per cached POST request. The id is what the API returns; the GET endpoint reads this row. |

Hashes:

- `string_hash(s)` — `blake2b(s, digest_size=16)` packed into a UUID.
- `list_hash(items)` — length-prefix blake2b so `["ab","c"]` and `["a","bc"]`
  hash differently. Order matters: `["a","b"]` ≠ `["b","a"]`.

The first POST for a string pays the transform latency (0.5 s in the dev
service, 1 ms in tests). Every later POST that includes the same string or
same list pays a Postgres lookup instead. The simulated transform is configured
in `src/transformer.py`; swap it for the real call when integrating.

## Tests

```bash
uv run pytest -q
```

`tests/test_keys.py` and `tests/test_transformer.py` are pure-Python unit
tests. `tests/test_endpoints.py`, `tests/test_get_payload.py`, and
`tests/test_retrieve.py` cover the FastAPI surface; they mock the DB session
for unit-style checks and rely on the configured test database for the
integration paths.

## Project layout

```
src/
  main.py            FastAPI app + lifespan + endpoints
  services.py        cache_payload / get_payload — the two cache ways
  schemas.py         request/response models
  models.py          string_cache, list_cache, transforms (ORM)
  transformer.py     simulated external service
  keys.py            blake2b helpers
  db.py              async engine + session factory

alembic/             migrations; sync URL resolved from DATABASE_URL
cli/                 cache-cli entry point (typer)
infra/compose/       docker-compose for the dev stack
scripts/             dev-up.sh / dev-down.sh
Dockerfile           multistage build (deps → runtime)
```