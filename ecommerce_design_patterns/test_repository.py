
from decimal import Decimal

# Opens a database session to communicate with PostgreSQL.
from db.database import SessionLocal

# Imports the repository that handles product database operations.
from repositories.product_repository import ProductRepository


# Creates an object to access product operations.
repository = ProductRepository()


# Opens a database session and automatically closes it afterward.
with SessionLocal() as db:

    # Creates a new product and saves it in PostgreSQL.
    product = repository.create(
        db,
        "Wireless Mouse",
        Decimal("25.00")  # Decimal avoids floating-point money errors.
    )

    # Prints the details of the product saved in the database.
    print("Product ID:", product.id)
    print("Product Name:", product.name)
    print("Product Price:", product.price)

    # Retrieves all products stored in PostgreSQL.
    products = repository.get_all(db)

    # Displays how many products are currently stored.
    print("Total Products:", len(products))
