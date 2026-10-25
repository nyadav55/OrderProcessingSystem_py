
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Read the connection string from an environment variable.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://inventory:devpass@localhost:5432/inventory_db"
)

# Engine manages connections to PostgreSQL.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Check connections before reusing them.
)

# Each request or operation should use its own session.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)

# Add safe session handling
def get_db():
    """Provide a database session and always close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()