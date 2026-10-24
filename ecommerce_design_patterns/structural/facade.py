# Facade pattern provides a simplified interface to multiple subsystems, 
# reducing coupling between client code and internal complexity.
# Goal: Simplify a complex checkout process behind one method.

# Real-world example: Instead of calling inventory, payment, and shipping services separately, the application calls checkout().


from decimal import Decimal

class InventoryService:
    """Checks whether products are available."""

    def check_stock(self, order_id: str) -> str:
        return f"Stock checked for {order_id}"

class PaymentService:
    """Processes order payments."""

    def process_payment(self, amount: Decimal) -> str:
        return f"Payment processed: ${amount:.2f}"

class ShippingService:
    """Arranges shipment after payment."""

    def arrange_shipping(self, order_id: str) -> str:
        return f"Shipping arranged for {order_id}"

class CheckoutFacade:
    """Provides one simple interface to the checkout process."""

    def __init__(self):
        # The facade coordinates the underlying services.
        self.inventory = InventoryService()
        self.payment = PaymentService()
        self.shipping = ShippingService()

    def checkout(self, order_id: str, amount: Decimal) -> list[str]:
        # Execute checkout steps in the correct order.
        results = [
            self.inventory.check_stock(order_id),
            self.payment.process_payment(amount),
            self.shipping.arrange_shipping(order_id),
        ]
        return results
