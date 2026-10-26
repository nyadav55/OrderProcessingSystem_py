# Business rules belong here, not in the controller or repository.

from sqlalchemy.orm import Session
from rest_api.repositories.product_repository import (
    create_product,
    list_products,
)
from rest_api.schemas.product import ProductCreate

# Import the repository function.
from rest_api.repositories.product_repository import get_product_by_id
from rest_api.repositories.product_repository import update_product
from rest_api.repositories.product_repository import delete_product


# Insert Product
def create_product_service(db: Session, data: ProductCreate):
    # Convert the validated Pydantic object into a dictionary.
    product_data = data.model_dump()

    # Call the repository and return the saved product to the API.
    return create_product(db, product_data)

# Get all product
def list_products_service(db: Session):
    # Delegate database retrieval to the repository.
    return list_products(db)

# get product by ID
def get_product_service(db: Session, product_id: int):
    # Delegate database lookup to the repository.
    return get_product_by_id(db, product_id)

# Update product - put
def update_product_service(
    db: Session,
    product_id: int,
    data: ProductCreate,
):
    # Convert validated request data into a dictionary.
    product_data = data.model_dump()

    # Delegate the update to the repository.
    return update_product(db, product_id, product_data)    

# delete by product_id
def delete_product_service(db: Session, product_id: int) -> bool:
    # Delegate deletion to the repository.
    return delete_product(db, product_id)    