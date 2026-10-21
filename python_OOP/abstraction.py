# By inheriting from Python's built-in ABC (Abstract Base Class), you can force child classes to implement specific methods. 
# You cannot create an instance of an abstract class directly.
# Abstraction means hiding implementation details and exposing only the essential functionality.

# Real-world example: 
# When you pay online, you click “Pay.” You don't need to know how the payment gateway processes the transaction internally.

from abc import ABC, abstractmethod

# Abstract class defines the payment contract.
class Payment(ABC):
    """
    By inheriting from ABC, this class becomes an Abstract Class.
    You CANNOT instantiate this directly (e.g., shipper = OrderShipper() will crash).
    """

    @abstractmethod
    def pay(self, amount):
        """
        The @abstractmethod decorator acts as a strict rule.
        Any child class MUST implement this method with their own custom logic.
        """
        pass


# Concrete class implements card payment.
class CardPayment(Payment):

    def pay(self, amount):
        # Validate the payment amount.
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        print(f"Processing card payment: ${amount:.2f}")
        print("Payment successful!")


# Create payment object.
payment = CardPayment()

try:
    # Attempt to process the payment.
    payment.pay(11002)

except ValueError as error:
    # Handle invalid payment amounts.
    print(f"Payment error: {error}")

except Exception as error:
    # Handle unexpected errors.
    print(f"Unexpected error: {error}")

else:
    # Runs only if no exception occurs.
    print("Order can proceed to confirmation.")

finally:
    # Runs whether payment succeeds or fails.
    print("Payment operation completed.")