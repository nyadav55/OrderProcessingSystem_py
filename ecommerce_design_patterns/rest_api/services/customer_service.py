# The duplicate-email check improves the API response, but PostgreSQL's unique constraint 
# remains the final protection against concurrent duplicate inserts.

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

# Import your repository functions.
from rest_api.repositories.customer_repository import (
    create_customer,
    list_customers,
    get_customer_by_id,
    get_customer_by_email,
    update_customer,
    delete_customer
)

# Import the Pydantic request schema.
from rest_api.schemas.customer import CustomerCreate

# create_customer
def create_customer_service(db: Session, data: CustomerCreate):
    # Check whether the email is already registered.
    existing_customer = get_customer_by_email(db, str(data.email))

    if existing_customer:
        # Reject duplicate email addresses.
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer email already exists",
        )

    # Convert validated Pydantic data to a dictionary.
    customer_data = data.model_dump()

    # Save the new customer through the repository.
    return create_customer(db, customer_data)

# get_customer
def list_customers_service(db: Session):
    # Return all customers from the repository.
    return list_customers(db)

# get_customer_by_id
def get_customer_service(db: Session, customer_id: int):
    # Search for the customer using the provided ID.
    customer = get_customer_by_id(db, customer_id)

    if customer is None:
        # Return HTTP 404 if the customer does not exist.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    # Return the customer if found.
    return customer

# update_customer_service
def update_customer_service(
    db: Session,
    customer_id: int,
    data: CustomerCreate,
):
    # Find the customer before updating.
    customer = get_customer_by_id(db, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    # Check whether another customer already uses the email.
    existing = get_customer_by_email(db, str(data.email))

    if existing is not None and existing.id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer email already exists",
        )

    try:
        # Update the customer through the repository.
        return update_customer(db, customer_id, data.model_dump())

    except IntegrityError:
        # Handles a concurrent duplicate-email insertion/update.
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer email already exists",
        )

# delete_customer_id
def delete_customer_service(db: Session, customer_id: int) -> bool:
    # Call the repository to delete the customer.
    return delete_customer(db, customer_id)