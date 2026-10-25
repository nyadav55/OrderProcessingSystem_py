
# Import the database session factory to handle connections and transactions
from db.database import SessionLocal
# Import the repository layer responsible for encapsulating Order database operations
from repositories.order_repository import OrderRepository

# Initialize the order repository instance to access data manipulation methods
repository = OrderRepository()

# Use a context manager to open a secure database session
# This automatically closes the session when the block finishes execution
with SessionLocal() as db:
    
    # Create and persist a new order record in the database
    order = repository.create(
        db,
        order_number="ORD-1001",
        customer_email="customer@example.com"
    )

    # Output the newly generated database primary key ID
    print("Order ID:", order.id)
    
    # Output the unique business identifier assigned to the order
    print("Order Number:", order.order_number)
    
    # Output the email address associated with the purchasing customer
    print("Customer:", order.customer_email)

    # Fetch all orders currently stored in the database and display the total count
    print("Total Orders:", len(repository.get_all(db)))
