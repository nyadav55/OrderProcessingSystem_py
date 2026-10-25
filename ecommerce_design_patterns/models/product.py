#  Run the automated service unit tests
# (.venv) PS E:\git_ny_project\OrderProcessingSystem_py\ecommerce_design_patterns> python -m pytest tests/ -v

# Import Decimal to perform accurate monetary calculations
from decimal import Decimal


class Product:
    """Represent a product available in the online store."""

    def __init__(self, product_id: int, name: str, price: Decimal):
        # Reject invalid product identifiers
        if product_id <= 0:
            raise ValueError("Product ID must be greater than zero")

        # Reject empty or whitespace-only product names
        if not name or not name.strip():
            raise ValueError("Product name cannot be empty")

        # Ensure price uses Decimal for accurate money handling
        if not isinstance(price, Decimal):
            raise TypeError("Product price must be a Decimal value")

        # Reject negative prices
        if price < Decimal("0.00"):
            raise ValueError("Product price cannot be negative")

        # Store validated product details
        self.product_id = product_id
        self.name = name.strip()
        self.price = price

    def __str__(self) -> str:
        # Format the price consistently with two decimal places
        return f"{self.name} - ${self.price:.2f}"
