# The controller defines the HTTP endpoint and validates input/output through Pydantic schemas.
# Keep your existing POST endpoint and add this GET endpoint.

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.database import get_db
from rest_api.schemas.product import ProductCreate, ProductResponse

from rest_api.services.product_service import (
    create_product_service,
    list_products_service,
    get_product_service,  
    update_product_service,
    delete_product_service,
)

# HTTPException lets us return HTTP errors such as 404.
from fastapi import APIRouter, Depends, HTTPException, status

# Groups product-related API endpoints under /products.
router = APIRouter(prefix="/products", tags=["Products"])

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product_endpoint(
    data: ProductCreate,
    db: Session = Depends(get_db),
):
    # Validate input through Pydantic and return the saved product.
    return create_product_service(db, data)


@router.get("/", response_model=list[ProductResponse])
def get_products_endpoint(db: Session = Depends(get_db)):
    # Return the list of products; the response schema permits NULL prices.
    return list_products_service(db)


# Add HTTPException to your FastAPI imports, import get_product_service, and add this endpoint:
@router.get("/{product_id}", response_model=ProductResponse)
def get_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
):
    # Fetch the requested product through the service layer.
    product = get_product_service(db, product_id)

    # Return HTTP 404 instead of a misleading response when absent.
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    # FastAPI converts the SQLAlchemy object using ProductResponse.
    return product    


# Update product - put
@router.put("/{product_id}", response_model=ProductResponse)
def update_product_endpoint(
    product_id: int,
    data: ProductCreate,
    db: Session = Depends(get_db),
):
    # Ask the service to update the requested product.
    product = update_product_service(db, product_id, data)

    # Return 404 when no matching product exists.
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    # Return the updated product.
    return product

# delete by product_id
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
):
    # Ask the service to delete the product.
    deleted = delete_product_service(db, product_id)

    # Return 404 if the product was not found.
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    # HTTP 204 means deletion succeeded with no response body.
    return None    
