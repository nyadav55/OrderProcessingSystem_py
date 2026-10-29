# uuid4()	Generate an order number with a very low collision probability
# set()	Detect duplicate product IDs
# sorted()	Acquire database locks consistently
# with_for_update()	Prevent concurrent transactions from modifying the same stock simultaneously
# db.commit()	Save all related changes together
# db.rollback()	Prevent partial orders and incorrect stock deductions

# Important: This assumes the orders, order_items, products, and customers tables exist with the expected columns. 
# Your pending Alembic migration still needs to be reconciled before production use.

from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Import the existing customer repository function.
from rest_api.repositories.customer_repository import get_customer_by_email

# Import order repository functions.
from rest_api.repositories.order_repository import (
    get_product_for_update,
    create_order,
    create_order_item,
    get_order_by_id,
    get_order_items,
    list_orders,
)

# Import the Pydantic request schema.
from rest_api.schemas.order import OrderCreate

from rest_api.schemas.order_status import OrderStatus, OrderStatusUpdate
from rest_api.repositories.product_repository import get_product_by_id

from db.models.order import OrderModel
from db.models.product import ProductModel


# Convert database order records into API response dictionaries.
def build_order_response(db: Session, order):
    # Fetch items associated with this order.
    items = get_order_items(db, order.id)

    # Return a structure matching OrderResponse.
    return {
        "id": order.id,
        "order_number": order.order_number,
        "customer_email": order.customer_email,
        "status": order.status,
        "items": items,
    }


# Create an order and deduct inventory atomically.
def create_order_service(db: Session, data: OrderCreate):
    # Reject repeated product IDs in the same request.
    product_ids = [item.product_id for item in data.items]

    if len(product_ids) != len(set(product_ids)):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, # # New constant supported by current Starlette versions.
            detail="Duplicate product IDs are not allowed",
        )

    try:
        # Verify that the customer exists.
        customer = get_customer_by_email(db, str(data.customer_email))

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

        # Lock product rows in a consistent order to reduce deadlock risk.
        products = {}

        for product_id in sorted(product_ids):
            product = get_product_for_update(db, product_id)

            if product is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {product_id} not found",
                )

            products[product_id] = product

        # Validate all products before changing inventory.
        for item in data.items:
            product = products[item.product_id]

            # Reject legacy products without a price.
            if product.price is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, # # New constant supported by current Starlette versions.
                    detail=f"Product {item.product_id} has no price",
                )

            # Ensure sufficient stock is available.
            if product.quantity < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Insufficient stock for product {item.product_id}",
                )

        # Generate a unique order number.
        order_number = f"ORD-{uuid4().hex[:12].upper()}"

        # Insert the order without committing.
        order = create_order(
            db=db,
            order_number=order_number,
            customer_email=str(data.customer_email),
        )

        # Create order items and deduct stock.
        for item in data.items:
            product = products[item.product_id]

            # Preserve the product price at purchase time.
            create_order_item(
                db=db,
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=product.price,
            )

            # SQLAlchemy tracks this inventory change.
            product.quantity -= item.quantity

        # Save order, order items, and stock changes together.
        db.commit()

        # Reload the saved order after committing.
        db.refresh(order)

        # Return the complete order response.
        return build_order_response(db, order)

    except HTTPException:
        # Undo any uncommitted changes after business validation fails.
        db.rollback()
        raise

    except IntegrityError:
        # Roll back database constraint failures.
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Order could not be created due to a database conflict",
        )

    except Exception:
        # Roll back unexpected failures.
        db.rollback()
        raise


# Retrieve one order with its items.
def get_order_service(db: Session, order_id: int):
    # Find the requested order.
    order = get_order_by_id(db, order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    # Return the order and associated items.
    return build_order_response(db, order)


# Retrieve all orders with their items.
def list_orders_service(db: Session):
    # Load all order records.
    orders = list_orders(db)

    # Build a response for each order.
    return [build_order_response(db, order) for order in orders]


# Phase 6 — Step 4.6: Order Status Lifecycle
# Allowed state transitions.
ALLOWED_TRANSITIONS = {
    OrderStatus.CREATED: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED},
    OrderStatus.CONFIRMED: {OrderStatus.SHIPPED, OrderStatus.CANCELLED},
    OrderStatus.SHIPPED: {OrderStatus.DELIVERED},
    OrderStatus.DELIVERED: set(),
    OrderStatus.CANCELLED: set(),
}

def update_order_status_service(
    db: Session,
    order_id: int,
    data: OrderStatusUpdate,
):
    try:
        # Lock the order to prevent simultaneous status changes.
        order = (
            db.query(OrderModel)
            .filter(OrderModel.id == order_id)
            .with_for_update()
            .first()
        )

        # Return 404 if the order does not exist.
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        # Convert stored status to the supported enum.
        try:
            current_status = OrderStatus(order.status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Unknown current order status",
            )

        # Reject invalid transitions.
        if data.status not in ALLOWED_TRANSITIONS[current_status]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cannot change {current_status.value} to {data.status.value}",
            )

        # Restore stock if the order is cancelled.
        if data.status == OrderStatus.CANCELLED:
            items = get_order_items(db, order_id)

            # Aggregate quantities by product ID.
            quantities = {}
            for item in items:
                quantities[item.product_id] = (
                    quantities.get(item.product_id, 0) + item.quantity
                )

            # Lock products consistently before modifying inventory.
            for product_id in sorted(quantities):
                product = (
                    db.query(ProductModel)
                    .filter(ProductModel.id == product_id)
                    .with_for_update()
                    .first()
                )

                if product is None:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Product {product_id} no longer exists",
                    )

                # Return reserved stock to inventory.
                product.quantity += quantities[product_id]

        # Update order status.
        order.status = data.status.value

        # Save status and stock restoration atomically.
        db.commit()
        db.refresh(order)

        # Return order with its items.
        return build_order_response(db, order)

    except Exception:
        # Roll back on any validation or database failure.
        db.rollback()
        raise