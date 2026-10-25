#  Run the automated service unit tests
# (.venv) PS E:\git_ny_project\OrderProcessingSystem_py\ecommerce_design_patterns> python -m pytest tests/ -v


# Import Decimal to calculate order totals without floating-point errors
from decimal import Decimal

# Import Product to type-check products added to an order
from models.product import Product


class Order:
    """Represent a customer's shopping order."""

    def __init__(self, order_id: str, customer_email: str):
        # Reject missing order identifiers
        if not order_id or not order_id.strip():
            raise ValueError("Order ID cannot be empty")

        # Reject missing customer email addresses
        if not customer_email or not customer_email.strip():
            raise ValueError("Customer email cannot be empty")

        # Basic email format check for this learning project
        if "@" not in customer_email or "." not in customer_email.split("@")[-1]:
            raise ValueError("Invalid customer email address")

        # Store validated order details
        self.order_id = order_id.strip()
        self.customer_email = customer_email.strip()

        # Initialize an empty list of products belonging to this order
        self.items: list[Product] = []

        # Set the initial order lifecycle status
        self.status = "created"

    def add_product(self, product: Product) -> None:
        """Add a valid product to the order."""

        # Prevent unrelated objects from being added to the order
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added to an order")

        # Add the validated product to the order
        self.items.append(product)

    @property
    def total(self) -> Decimal:
        """Calculate the current order total."""

        # Add every product price, starting with Decimal zero
        return sum(
            (product.price for product in self.items),
            start=Decimal("0.00")
        )
