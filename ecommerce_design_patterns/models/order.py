from decimal import Decimal
from unicodedata import decimal
from models.product import Product

class Order:
    """Represents a customer's shopping order."""

    def __init__(self, order_id:str, customer_email:str):
        self.order_id = order_id
        self.customer_email = customer_email

        # An order contains multiple products (composition).
        self.items: list[Product] = []
        self.status = "created"

    def add_product(self, product: Product) -> None:
        """Add a product to the order."""
        self.items.append(product)

    @property
    def total(self) -> Decimal:
        """Calculate the order total."""
        return sum(
            (product.price for product in self.items),
            start=Decimal("0")
        )        

# - @property — decorator in Python is an excellent example of encapsulation.lets you access total like a variable.
# - self.items — contains the order's products.
# - product.price for product in self.items — retrieves each product's price.
# - sum(...) — adds all prices.
# - Decimal("0") — starts with a decimal zero, including when the order is empty.
# - -> Decimal — indicates the expected return type.
# Example: Laptop = 800, Mouse = 25 → order.total returns Decimal("825").

# Interview answer: "@property lets me expose a calculated value as an attribute. 
# Here, the order total is calculated dynamically from the current product list."