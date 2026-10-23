# Builder Pattern
# Goal: Build complex objects step by step instead of passing many parameters to one constructor.

# E-commerce example: Create an order with customer details, products, shipping address, and discount.
# Interview answer: The Builder pattern constructs complex objects incrementally, 
# improves readability, and validates required data before returning the finished object.


from decimal import Decimal
from models.order import Order
from models.product import Product


class OrderBuilder:
    """Build an order step by step."""

    def __init__(self, order_id: str):
        self.order = Order(order_id, "")

    def set_customer(self, email: str):
        self.order.customer_email = email
        return self  # Allows method chaining

    def add_product(self, product: Product):
        self.order.add_product(product)
        return self

    def set_shipping_address(self, address: str):
        self.order.shipping_address = address
        return self

    def build(self) -> Order:
        # Validate required information before returning.
        if not self.order.customer_email:
            raise ValueError("Customer email is required")

        if not self.order.items:
            raise ValueError("Order must contain at least one product")

        if not hasattr(self.order, "shipping_address"):
            raise ValueError("Shipping address is required")

        return self.order