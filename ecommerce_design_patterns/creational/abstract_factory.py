# Abstract Factory Pattern
# Goal: Create families of related objects without specifying their concrete classes.

# E-commerce example: Support different payment and shipping providers.

from abc import ABC, abstractmethod
from decimal import Decimal


# Product interfaces
class Payment(ABC):
    @abstractmethod
    def pay(self, amount: Decimal) -> str:
        pass


class Shipping(ABC):
    @abstractmethod
    def ship(self, order_id: str) -> str:
        pass


# PayPal family
class PayPalPayment(Payment):
    def pay(self, amount: Decimal) -> str:
        return f"Paid ${amount:.2f} using PayPal"


class PayPalShipping(Shipping):
    def ship(self, order_id: str) -> str:
        return f"Shipping order {order_id} via PayPal partner"


# Credit Card family
class CardPayment(Payment):
    def pay(self, amount: Decimal) -> str:
        return f"Paid ${amount:.2f} using Credit Card"


class ExpressShipping(Shipping):
    def ship(self, order_id: str) -> str:
        return f"Shipping order {order_id} via Express Shipping"


# Abstract factory
class CheckoutFactory(ABC):
    @abstractmethod
    def create_payment(self) -> Payment:
        pass

    @abstractmethod
    def create_shipping(self) -> Shipping:
        pass


# Concrete factory 1
class PayPalCheckoutFactory(CheckoutFactory):
    def create_payment(self) -> Payment:
        return PayPalPayment()

    def create_shipping(self) -> Shipping:
        return PayPalShipping()


# Concrete factory 2
class CardCheckoutFactory(CheckoutFactory):
    def create_payment(self) -> Payment:
        return CardPayment()

    def create_shipping(self) -> Shipping:
        return ExpressShipping()


# Factory Method creates a particular product; Abstract Factory creates a compatible family of products.
# Interview answer: Abstract Factory creates families of related objects through a common interface, 
# keeping checkout logic independent of specific payment and shipping implementations.