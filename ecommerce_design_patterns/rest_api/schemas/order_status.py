

from enum import Enum
from pydantic import BaseModel


# Restrict status values to supported order states.
class OrderStatus(str, Enum):
    CREATED = "created"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# Validate the incoming status update request.
class OrderStatusUpdate(BaseModel):
    status: OrderStatus