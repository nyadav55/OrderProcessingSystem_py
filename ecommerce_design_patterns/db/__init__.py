
from db.database import engine
from db.base import Base
import db.models


def create_tables():
    """Create database tables that do not already exist."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()
