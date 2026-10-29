# Create three Order APIs using FastAPI and connect them to your existing Order Service.

# Import FastAPI router, dependency injection and HTTP status codes.
from fastapi import APIRouter, Depends, status

# Import SQLAlchemy database session.
from sqlalchemy.orm import Session

# Import your existing database session dependency.
from db.database import get_db

# Import request and response validation schemas.
from rest_api.schemas.order import OrderCreate, OrderResponse

# Import business logic from your Order Service.
from rest_api.services.order_service import (
    create_order_service,
    get_order_service,
    list_orders_service,
    update_order_status_service,
)

# Import status update request schema.
from rest_api.schemas.order_status import OrderStatusUpdate


# Group all order endpoints under /orders.
router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


# 1. POST /orders/ - Create a new order.
@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order_endpoint(
    data: OrderCreate,
    db: Session = Depends(get_db),
):
    # Pydantic validates the incoming request.
    # FastAPI injects the database session using Depends().
    # Service handles stock validation, order creation and transaction.
    return create_order_service(db, data)


# 2. GET /orders/ - Retrieve all orders.
@router.get(
    "/",
    response_model=list[OrderResponse],
)
def list_orders_endpoint(
    db: Session = Depends(get_db),
):
    # Retrieve all orders with their order items.
    return list_orders_service(db)


# 3. GET /orders/{order_id} - Retrieve one order.
@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
):
    # Return the requested order or HTTP 404 if not found.
    return get_order_service(db, order_id)

@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
)
def update_order_status_endpoint(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
):
    # Delegate lifecycle validation and persistence to service.
    return update_order_status_service(db, order_id, data)    