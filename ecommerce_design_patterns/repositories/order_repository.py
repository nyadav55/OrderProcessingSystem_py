
# Import the SQLAlchemy session type used to execute database operations
from sqlalchemy.orm import Session

# Import the SQLAlchemy model representing an order record
from db.models import OrderModel


class OrderRepository:

    # Find an existing order using its unique business identifier
    def get_by_order_number(self, db: Session, order_number: str):
        # Return the matching order, or None if it does not exist
        return (
            db.query(OrderModel)
            .filter(OrderModel.order_number == order_number)
            .first()
        )

    # Save a new order in PostgreSQL
    def create(
        self,
        db: Session,
        order_number: str,
        customer_email: str
    ):
        # Create an order object using the supplied customer details
        order = OrderModel(
            order_number=order_number,
            customer_email=customer_email
        )

        try:
            # Add the new order to the current database session
            db.add(order)

            # Commit the transaction to persist the order
            db.commit()

            # Refresh the object to retrieve database-generated values
            db.refresh(order)

        except Exception:
            # Roll back the transaction if any database operation fails
            db.rollback()

            # Re-raise the original error for the caller to handle
            raise

        # Return the persisted order after a successful commit
        return order

    # Retrieve an order by its primary key
    def get_by_id(self, db: Session, order_id: int):
        return db.get(OrderModel, order_id)

    # Retrieve every order stored in the database
    def get_all(self, db: Session):
        return db.query(OrderModel).all()

        # Update and persist an order's status in PostgreSQL
    def update_status(self, db: Session, order, new_status: str):
        # Assign the new status to the order record
        order.status = new_status

        try:
            # Save the status change in the current transaction
            db.commit()

            # Refresh the object with the latest database values
            db.refresh(order)
        except Exception:
            # Undo the transaction if saving the status fails
            db.rollback()

            # Preserve the original database error
            raise

        # Return the updated order after a successful commit
        return order