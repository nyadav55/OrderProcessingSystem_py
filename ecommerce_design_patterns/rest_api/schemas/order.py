
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict, EmailStr


# Request schema for an individual order item.
class OrderItemCreate(BaseModel):
    # Product being purchased.
    product_id: int = Field(gt=0)

    # Customer must order at least one unit.
    quantity: int = Field(gt=0)


# Request schema for creating an order.
class OrderCreate(BaseModel):
    # Email address of the customer placing the order.
    customer_email: EmailStr

    # An order must contain at least one item.
    items: list[OrderItemCreate] = Field(min_length=1)


# Response schema for an order item.
class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int

    # Price captured when the order was placed.
    unit_price: Decimal

    # Convert SQLAlchemy model objects into Pydantic responses.
    model_config = ConfigDict(from_attributes=True)


# Response schema for an order.
class OrderResponse(BaseModel):
    id: int
    order_number: str
    customer_email: EmailStr
    status: str

    # Order items will be populated by the service/repository layer.
    items: list[OrderItemResponse]

    # Read attributes from SQLAlchemy model objects.
    model_config = ConfigDict(from_attributes=True)