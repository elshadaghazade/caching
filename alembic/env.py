"""Alembic environment wired to src.db.DATABASE_URL."""
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine.url import make_url

from alembic import context

from src.db import DATABASE_URL, Base
from src import models  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _sync_database_url() -> str:
    """Drop the `_async` suffix from the async URL so Alembic can connect."""
    url = make_url(DATABASE_URL)
    if url.drivername.endswith("_async"):
        url = url.set(drivername=url.drivername.removesuffix("_async"))
    return url.render_as_string(hide_password=False)


def run_migrations_offline() -> None:
    """Emit SQL to stdout without a DB connection."""
    context.configure(
        url=_sync_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against a live DB connection."""
    section = config.get_section(config.config_ini_section, {})
    section["sqlalchemy.url"] = _sync_database_url()
    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()