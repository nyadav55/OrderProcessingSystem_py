from decimal import Decimal

class Product:
    """Represents a product available in the online store."""
    def __init__(self, product_id:int, name: str, price:Decimal):
        # validate the product price.
        if price < Decimal("0.00"):
            raise ValueError("Product price cannot be negative")

        # store product details
        self.product_id = product_id
        self.name = name
        self.price = price

    def __str__(self) -> str:
        # Return a readable product description.
        return f"{self.name} - ${self.price:2f}"    
