# Create request and response schemas

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerCreate(BaseModel):
    # Validate customer details received from the API.
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr


class CustomerResponse(BaseModel):
    # Define the fields returned to API clients.
    id: int
    name: str
    email: EmailStr

    # Read values directly from SQLAlchemy model objects.
    model_config = ConfigDict(from_attributes=True)