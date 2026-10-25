# Builder Pattern
# Goal: Build complex objects step by step instead of passing many parameters to one constructor.

# E-commerce example: Create an order with customer details, products, shipping address, and discount.
# Interview answer: The Builder pattern constructs complex objects incrementally, 
# improves readability, and validates required data before returning the finished object.
# The builder should store order details until .build() is called, then create the validated Order.

# Import the Order model that will be created after all required details are set
from models.order import Order

# Import Product for type hints and product validation
from models.product import Product


class OrderBuilder:
    """Build an order step by step before creating the final Order object."""

    def __init__(self, order_id: str):
        # Store the order ID without creating an incomplete Order object
        self.order_id = order_id

        # Keep customer details until the build step
        self.customer_email = ""

        # Store products added during the building process
        self.products: list[Product] = []

        # Store the shipping address separately
        self.shipping_address = ""

    def set_customer(self, customer_email: str):
        # Save the customer email for validation when build() is called
        self.customer_email = customer_email
        return self

    def add_product(self, product: Product):
        # Reject anything that is not a Product instance
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added")

        # Add the product to the order being assembled
        self.products.append(product)
        return self

    def set_shipping_address(self, address: str):
        # Save the shipping address for the completed order
        self.shipping_address = address
        return self

    def build(self) -> Order:
        # Validate required information before creating the Order
        if not self.customer_email or not self.customer_email.strip():
            raise ValueError("Customer email cannot be empty")

        # Create the Order only after required details are provided
        order = Order(self.order_id, self.customer_email)

        # Transfer all selected products into the final order
        for product in self.products:
            order.add_product(product)

        # Attach the shipping address to the completed order
        order.shipping_address = self.shipping_address

        # Return the fully constructed order
        return order
