# syntax=docker/dockerfile:1.7

# ---- deps -----------------------------------------------------------------
# Resolves and installs Python dependencies into a virtualenv. Re-runs only
# when pyproject.toml or uv.lock change.
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS deps

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project


# ---- runtime -------------------------------------------------------------
# Carries the prebuilt .venv into a slim final image and adds only the
# application sources on top, so editing a .py file re-busts only the COPY
# layer that pulls in src/, not the deps layer.
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:${PATH}"

WORKDIR /app

COPY --from=deps /app/.venv /app/.venv

COPY alembic.ini ./
COPY alembic ./alembic
COPY src ./src
COPY entrypoint.sh ./

EXPOSE 8000
ENTRYPOINT [ "/app/entrypoint.sh" ]