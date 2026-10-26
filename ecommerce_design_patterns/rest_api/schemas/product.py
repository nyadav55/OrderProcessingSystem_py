# Pydantic validates incoming API data before it reaches your business logic.
# Request → Pydantic → Controller → Service → Repository → Database

from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


# Validates incoming product data from API requests.
class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    quantity: int = Field(ge=0)  # Quantity cannot be negative.
    price: Decimal = Field(
        gt=0, max_digits=10, decimal_places=2
    )  # New products must have a positive price.


# Defines the product data returned by the API.
class ProductResponse(BaseModel):
    id: int
    name: str
    quantity: int
    price: Decimal | None = None  # Allows legacy database rows with NULL prices.

    # Allows Pydantic to read values from SQLAlchemy model objects.
    model_config = ConfigDict(from_attributes=True)