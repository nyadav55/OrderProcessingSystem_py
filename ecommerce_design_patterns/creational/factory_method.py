# Factory Method Pattern
# Goal: Create different payment methods without directly creating their objects inside the order-processing code.

# Real-world example: An e-commerce customer can pay using a credit card or PayPal.

from abc import ABC, abstractmethod
from decimal import Decimal

# Step 1: Define the common payment interface.
class Payment(ABC):

    @abstractmethod
    def pay(self, amount: Decimal) -> str: 
        pass

class CreditCardPayment(Payment):
    def pay(self, amount: Decimal) -> str:
        return f"Paid ${amount:.2f} using Credit Card"

# Step 3: Implement PayPal payment.
class PayPalPayment(Payment):

    def pay(self, amount: Decimal) -> str:
        return f"Paid ${amount:.2f} using PayPal"

# Step 4: Define the factory.
class PaymentFactory:
    @staticmethod
    def create_payment(payment_type: str) -> Payment:
        if payment_type == "credit_card":
            return CreditCardPayment()
        elif payment_type == "paypal":
            return PayPalPayment()
        else:
            raise ValueError("Unsupported payment method")

# Interview answer: The Factory Method pattern separates object creation from business logic, 
# making it easier to introduce new payment methods without changing the checkout flow.            

