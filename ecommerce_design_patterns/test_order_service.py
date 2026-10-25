


# Import the database session factory
from db.database import SessionLocal

# Import the service that handles order business logic
from services.order_service import OrderService


# Create the service instance
service = OrderService()

# Open a database session and close it automatically afterward
with SessionLocal() as db:
    # Create an order through the service layer
    order = service.create_order(
        db,
        order_number="ORD-1002",
        customer_email="customer2@example.com"
    )

    # Display the newly created order details
    print("Order ID:", order.id)
    print("Order Number:", order.order_number)
    print("Customer:", order.customer_email)
