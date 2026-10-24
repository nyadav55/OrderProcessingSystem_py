# Adapter pattern allows incompatible interfaces to work together without changing the existing application or third-party code.
# Goal: Make an external payment gateway work with your existing payment interface.

from decimal import Decimal
from abc import ABC, abstractmethod


# Our application's expected interface
class PaymentProcessor(ABC):

    @abstractmethod
    def pay(self, amount: Decimal) -> str:
        pass


# External gateway with a different method name
class ExternalPaymentGateway:

    def make_payment(self, amount: Decimal) -> str:
        return f"External gateway processed ${amount:.2f}"


# Adapter translates our interface to the gateway's interface
class PaymentAdapter(PaymentProcessor):

    def __init__(self, gateway: ExternalPaymentGateway):
        self.gateway = gateway

    def pay(self, amount: Decimal) -> str:
        return self.gateway.make_payment(amount)