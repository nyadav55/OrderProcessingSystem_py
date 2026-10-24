# Strategy pattern encapsulates interchangeable algorithms behind a common interface and allows the application to select one at runtime.
# Goal: Switch between different algorithms at runtime without changing the checkout code.

# Real-world example: Customers choose Standard Shipping or Express Shipping.


from abc import ABC, abstractmethod
from decimal import Decimal


# Common interface for all shipping strategies.
class ShippingStrategy(ABC):

    @abstractmethod
    def calculate_cost(self, order_total: Decimal) -> Decimal:
        pass


# Standard shipping: fixed cost of $5.
class StandardShipping(ShippingStrategy):

    def calculate_cost(self, order_total: Decimal) -> Decimal:
        return Decimal("5.00")


# Express shipping: fixed cost of $15.
class ExpressShipping(ShippingStrategy):

    def calculate_cost(self, order_total: Decimal) -> Decimal:
        return Decimal("15.00")


# Uses the selected strategy to calculate shipping.
class ShippingCostCalculator:

    def __init__(self, strategy: ShippingStrategy):
        self.strategy = strategy

    def calculate(self, order_total: Decimal) -> Decimal:
        return self.strategy.calculate_cost(order_total)

    # Change shipping strategy at runtime.
    def set_strategy(self, strategy: ShippingStrategy) -> None:
        self.strategy = strategy
