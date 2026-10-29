# Create Customer API endpoints (POST, GET all, GET by ID) and register the router.

# Import FastAPI routing, dependency injection, and HTTP status codes.
from fastapi import APIRouter, Depends, status, HTTPException

# SQLAlchemy database session.
from sqlalchemy.orm import Session

# Existing database dependency.
from db.database import get_db

# Pydantic request and response schemas.
from rest_api.schemas.customer import CustomerCreate, CustomerResponse

# Import customer business logic from the service layer.
from rest_api.services.customer_service import (
    create_customer_service,
    list_customers_service,
    get_customer_service,
    update_customer_service,
    delete_customer_service,
)

# Group all customer endpoints under /customers.
router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


# 1. POST /customers/ - Create a new customer.
@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer_endpoint(
    data: CustomerCreate,
    db: Session = Depends(get_db),
):
    # FastAPI validates incoming JSON using CustomerCreate.
    # Depends(get_db) provides the database session.
    return create_customer_service(db, data)


# 2. GET /customers/ - Retrieve all customers.
@router.get("/", response_model=list[CustomerResponse])
def list_customers_endpoint(
    db: Session = Depends(get_db),
):
    # Return customer records through the service layer.
    return list_customers_service(db)


# 3. GET /customers/{customer_id} - Retrieve a customer by ID.
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
):
    # The service returns 404 if the customer doesn't exist.
    return get_customer_service(db, customer_id)

# 4. Put /customers/{customer_id} - Update a customer by ID.
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer_endpoint(
    customer_id: int,
    data: CustomerCreate,
    db: Session = Depends(get_db),
):
    # Delegate validation and updating to the service layer.
    return update_customer_service(db, customer_id, data)

# 5. Delete /customers/{customer_id} - delete a customer by ID.
@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
):
    # Request deletion through the service layer.
    deleted = delete_customer_service(db, customer_id)

    # Return HTTP 404 if the customer does not exist.
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    # HTTP 204 returns no response body.
    return None
