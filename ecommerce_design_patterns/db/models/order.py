
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    customer_email: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(30), default="created", nullable=False
    )