# It connects Alembic to your existing SQLAlchemy models.
# Compare SQLAlchemy models with the current PostgreSQL schema
# Run - python -m alembic revision --autogenerate -m "initial schema"

# Import Alembic's configuration and migration context
from alembic import context

# Import the application's database engine and connection settings
from db.database import DATABASE_URL

# Import Base so Alembic can inspect all registered table definitions
from db.base import Base

# Import models so their tables are registered in Base.metadata
import db.models

# Load settings from alembic.ini
config = context.config

# Supply the application's database URL to Alembic
config.set_main_option("sqlalchemy.url", DATABASE_URL.replace("%", "%%"))

# Tell Alembic which SQLAlchemy metadata to compare against PostgreSQL
target_metadata = Base.metadata


def run_migrations_offline():
    # Generate SQL without opening a live database connection
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # Run the migration in offline mode
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    # Use the application's existing engine and connection
    from db.database import engine

    # Open a database connection for schema comparison and migration
    with engine.connect() as connection:
        # Configure Alembic to use the active connection and model metadata
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        # Execute migration operations within a transaction
        with context.begin_transaction():
            context.run_migrations()


# Select offline or online execution based on Alembic's configuration
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()