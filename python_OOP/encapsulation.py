# Real-world problem: Customers should not be able to purchase products at negative prices.
# Key concepts to remember
# - @property — lets you access a method like an attribute: product.price.
# - @price.setter — intercepts assignments to product.price.
# - self._price — stores the actual value internally.
# - ValueError — reports that the supplied value is invalid.
# - Encapsulation — keeps validation logic in one place, so it runs during both object creation and later price updates.

# Remember:
# - Class: blueprint.
# - Object: instance of a class.
# - __init__: initializes an object.
# - self: refers to the current instance.

# Decimal handles decimal numbers more reliably than float
from decimal import Decimal

class Product:
# Runs automatically when we create a Product object.
    def __init__(self, name:str, price:Decimal):
        self.name = name
        # Private attribute: Hidden from direct access outside the class 
        self.price = price  # Uses the property setter below

# Getter: Safely read-only access to private data
    @property
    def price(self):
        # Return the internally stored price.
        return self._price

# Setter: runs whenever we assign product.price = value.
    @price.setter 
    def price(self,value):   
         # Reject negative prices.
         if value < Decimal("0.00"):
             raise ValueError("Price cannot be negative")
         # Store the validated price.
         # Underscore indicates an internal-use attribute.
         self._price = value

# Create a product; the setter validates the initial price.
product = Product("Keyboard", Decimal("50.00"))

# Update the price; the setter validates this value too.
product.price = Decimal("25.00")

# Read the price; the getter returns the stored/updated value.
print(product.price)

# Uncomment to test validation:
#product.price = Decimal("-10.00")
# Raises ValueError: Price cannot be negative


