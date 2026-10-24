# Decorator Pattern
# Goal: Add discounts, tax, or shipping charges to an order dynamically without modifying the Order class.

from abc import ABC, abstractmethod
from decimal import Decimal

# Common pricing interface
class PriceCalculator(ABC):
    @abstractmethod
    def calculate(self) -> Decimal:
        pass

# Base order price
class BasePrice(PriceCalculator):
    def __init__(self, amount: Decimal):
        self.amount = amount

    def calculate(self) -> Decimal:
        return self.amount   

# Base decorator
class PriceDecorator(PriceCalculator):
    def __init__(self, calculator: PriceCalculator):
        self.calculator = calculator

# Add a 10% discount
class DiscountDecorator(PriceDecorator):
    def calculate(self) -> Decimal:
        price = self.calculator.calculate()
        return price * Decimal("0.90")  

# Add 18% tax
class TaxDecorator(PriceDecorator):

    def calculate(self) -> Decimal:
        price = self.calculator.calculate()
        return price * Decimal("1.18")


# Add shipping charge
class ShippingDecorator(PriceDecorator):

    def __init__(
        self,
        calculator: PriceCalculator,
        shipping_fee: Decimal
    ):
        super().__init__(calculator)
        self.shipping_fee = shipping_fee

    def calculate(self) -> Decimal:
        # Add shipping to the calculated price.
        return self.calculator.calculate() + self.shipping_fee