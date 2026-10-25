
# Import the SQLAlchemy session type for database operations
from sqlalchemy.orm import Session

# Import the repository responsible for order data access
from repositories.order_repository import OrderRepository


class OrderService:

    # Accept a repository dependency, or create the default repository
    def __init__(self, order_repository=None):
        self.order_repository = order_repository or OrderRepository()

    # Validate order details before asking the repository to save them
    def create_order(
        self,
        db: Session,
        order_number: str,
        customer_email: str
    ):
        # Reject order numbers containing only whitespace
        if not order_number or not order_number.strip():
            raise ValueError("Order number cannot be empty")

        # Reject customer emails containing only whitespace
        if not customer_email or not customer_email.strip():
            raise ValueError("Customer email cannot be empty")

        # Remove accidental spaces around the supplied values
        order_number = order_number.strip()
        customer_email = customer_email.strip()

        # Check whether this order number is already in use
        existing_order = self.order_repository.get_by_order_number(
            db, order_number
        )

        # Reject duplicate order numbers before attempting to save
        if existing_order is not None:
            raise ValueError("Order number already exists")

        # Delegate persistence to the repository after validation
        return self.order_repository.create(
            db,
            order_number,
            customer_email
        )

        # Define which status changes are allowed by the business
    ALLOWED_TRANSITIONS = {
        "created": {"paid", "cancelled"},
        "paid": {"shipped", "refunded"},
        "shipped": {"delivered"},
        "delivered": set(),
        "cancelled": set(),
        "refunded": set(),
    }

    # Validate a requested transition and persist it through the repository
    def update_order_status(
        self,
        db: Session,
        order_number: str,
        new_status: str,
    ):
        # Normalize the incoming values before validation
        order_number = order_number.strip() if order_number else ""
        new_status = new_status.strip().lower() if new_status else ""

        # Reject missing order numbers
        if not order_number:
            raise ValueError("Order number cannot be empty")

        # Reject statuses not supported by the lifecycle
        if new_status not in self.ALLOWED_TRANSITIONS:
            raise ValueError("Invalid order status")

        # Find the existing order in the database
        order = self.order_repository.get_by_order_number(
            db, order_number
        )

        # Fail clearly when the order does not exist
        if order is None:
            raise ValueError("Order not found")

        # Read the valid next statuses for the current state
        allowed = self.ALLOWED_TRANSITIONS.get(order.status, set())

        # Prevent invalid transitions, such as delivered to cancelled
        if new_status not in allowed:
            raise ValueError(
                f"Cannot change order status from "
                f"{order.status} to {new_status}"
            )

        # Persist the validated status change
        return self.order_repository.update_status(
            db, order, new_status
        )