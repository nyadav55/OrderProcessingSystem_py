# Polymorphism means "many forms." 
# It allows different classes to have methods with the exact same name but completely different inner behaviors. 
# Python dynamically resolves which method to run based on the object type.

# Remember:
# - Class: blueprint.
# - Object: instance of a class.
# - __init__: initializes an object.
# - self: refers to the current instance.

from decimal import Decimal
from typing import Optional

class CardPayment:
    def pay(self, amount: Optional[Decimal] = None):
# 1. Null-Value Handling
        sanitized_amount = amount if amount is not None else Decimal("0.00")
        
# 2. Exception Handling Check (Business Logic Validation)
        if sanitized_amount <= 0:
            raise ValueError("Credit Card transactions must be greater than $0.00.")
            
        print(f"Paid ${sanitized_amount:.2f} using card")


class WalletPayment:
    def pay(self, amount):
# 1. Null-Value Handling
        sanitized_amount = amount if amount is not None else Decimal("0.00")
        
# 2. Exception Handling Check (Simulating a transaction limit issue)
        if sanitized_amount > 2000:
            raise OverflowError("UPI transactions are limited to a maximum of $2,000.00 per day.")
        if sanitized_amount <= 0:
            raise ValueError("UPI transfer amount must be greater than $0.00.")        
        print(f"📱 [UPI Gateway] Paid ${amount:.2f} using wallet")


def checkout(payment_method, amount):
    # Same method call, different implementation
    payment_method.pay(amount)


checkout(CardPayment(), 10.00)
checkout(WalletPayment(), 75)