# Class and object
# Real-world example: An online store sells products. 
# A Product class defines what every product contains, while each product object represents an actual item.

# Remember:
# - Class: blueprint.
# - Object: instance of a class.
# - __init__: initializes an object.
# - self: refers to the current instance.

from decimal import Decimal

# Class: blueprint for creating products
# Double underscores on both sides, spelled i-n-i-t
class Product:
    def __init__(self, name:str, price:Decimal):
        self.name = name
        self.price = price

    def display(self):
        # Display product information
        print(f"{self.name}: ${self.price:.2f}")  

# Objects: individual products
laptop = Product("Laptop", Decimal("800.00"))  
mouse = Product("Mouse", Decimal("25.00"))  

laptop.display()
mouse.display()
