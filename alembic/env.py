from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from todolist.app.db.session import engine
from todolist.app.models.models import Base

# Interpret the config file for Python logging.
fileConfig(context.config.config_file_name)

# Set the metadata object for Alembic's autogenerate feature
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = str(engine.url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
