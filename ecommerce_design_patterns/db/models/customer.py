# SQLAlchemy maps this Python class to the PostgreSQL customers table.
# Create the Customer database model

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

# from db.database import Base
from db.base import Base  # Correct: imports the shared SQLAlchemy Base

class CustomerModel(Base):
    # Database table for customer records.
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )