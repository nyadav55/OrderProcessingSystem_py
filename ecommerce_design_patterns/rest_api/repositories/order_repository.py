# db.add()	Stage an object for database insertion
# db.flush()	Send SQL to PostgreSQL without committing
# db.commit()	Permanently save the transaction
# db.rollback()	Undo uncommitted changes
# .with_for_update()	Lock selected rows until transaction completion
# .first()	Retrieve one matching record or None

# Important: The repository intentionally does not call db.commit(). 
# The Order Service will control one transaction covering order creation, order items, and inventory deduction.

from sqlalchemy.orm import Session

# Import existing SQLAlchemy database models.
from db.models.order import OrderModel
from db.models.order_item import OrderItemModel
from db.models.product import ProductModel


# 1. Find a product by ID and lock its row during order processing.
def get_product_for_update(db: Session, product_id: int):
    # Row locking helps prevent concurrent orders from overselling stock.
    return (
        db.query(ProductModel)
        .filter(ProductModel.id == product_id)
        .with_for_update()
        .first()
    )


# 2. Create an order record without committing yet.
def create_order(
    db: Session,
    order_number: str,
    customer_email: str,
) -> OrderModel:

    # Create an order with its initial status.
    order = OrderModel(
        order_number=order_number,
        customer_email=customer_email,
        status="created",
    )

    # Stage the order for insertion.
    db.add(order)

    # Send INSERT to PostgreSQL to generate the order ID.
    # Do not commit yet; the service will manage the transaction.
    db.flush()

    return order


# 3. Add a product to an existing order.
def create_order_item(
    db: Session,
    order_id: int,
    product_id: int,
    quantity: int,
    unit_price,
) -> OrderItemModel:

    # Create an order item using the product's purchase-time price.
    item = OrderItemModel(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price,
    )

    # Stage the order item for insertion.
    db.add(item)

    # Generate the order-item ID without committing.
    db.flush()

    return item


# 4. Retrieve an order by ID.
def get_order_by_id(db: Session, order_id: int) -> OrderModel | None:

    # Return the matching order, or None if not found.
    return db.query(OrderModel).filter(
        OrderModel.id == order_id
    ).first()


# 5. Retrieve all items belonging to an order.
def get_order_items(db: Session, order_id: int) -> list[OrderItemModel]:

    # Query order items using the order's ID.
    return db.query(OrderItemModel).filter(
        OrderItemModel.order_id == order_id
    ).order_by(OrderItemModel.id).all()


# 6. Retrieve all orders.
def list_orders(db: Session) -> list[OrderModel]:

    # Return all orders sorted by ID.
    return db.query(OrderModel).order_by(OrderModel.id).all()