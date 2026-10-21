# Inheritance allows a new class (child) to adopt the code of an existing class (parent). 
# This eliminates copy-pasting. 
# The child class automatically gets all methods from the parent 
# but can also add its own special features

# Remember:
# - Class: blueprint.
# - Object: instance of a class.
# - __init__: initializes an object.
# - self: refers to the current instance.

from decimal import Decimal
from typing import Optional

class BaseProduct:
    def __init__(self, brand: str, name, price):
        self.name = name
        self.price = price
        self.brand = brand


# Child Class inherits from BaseProduct + add unique weight trait
class PhysicalProduct(BaseProduct):
    def __init__(self, brand: str, name: str, price: Optional[Decimal] = None, weight: float = 0.0):
        # super() calls the Parent __init__ to handle brand, name, and price of the BaseProduct
        super().__init__(brand, name, price)
        # Child adds its own unique property i.e. weight
        # if else add for Safeguard
        self.weight = weight if weight is not None else 0.0
        self.price = price if price is not None else Decimal("0.00")
        self.brand = brand if brand else "Unknown"


# Display Method
    def get_details(self):
        print (f"Brand: {self.brand} | Item: {self.name} | Price: ${self.price:.2f} | Weight: {self.weight}kg")
    
# --- TESTING DATA HANDLERS ---
# code handles data sanitization effectively inside the child class.
# in PowerShell, nothing will print to the console.
# This is because your get_details() method uses a return statement instead of a print() statement. 
# Scenario A: Passing explicit 'None' (null) values

laptop_nulls = PhysicalProduct(brand=None, name="Laptop", weight=2.5, price=None)
laptop_nulls.get_details() 
# Output: Brand: Unknown | Item: Laptop | Price: $0.00 | Weight: 2.5kg

# Scenario B: Omitting values entirely (skipping fields using keyword arguments)
mouse_omitted = PhysicalProduct(brand="Logitech", name="Gaming Mouse")
mouse_omitted.get_details()
# Output: Brand: Logitech | Item: Gaming Mouse | Price: $0.00 | Weight: 0.0kg