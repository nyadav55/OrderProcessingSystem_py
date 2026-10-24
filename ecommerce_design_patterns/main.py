from decimal import Decimal
from models.product import Product
from models.order import Order
from creational.factory_method import PaymentFactory
from creational.abstract_factory import PayPalCheckoutFactory
from creational.builder import OrderBuilder
from structural.adapter import ExternalPaymentGateway, PaymentAdapter
from structural.decorator import (
    BasePrice,
    DiscountDecorator,
    TaxDecorator,
    ShippingDecorator,
)
from structural.facade import CheckoutFacade
from behavioral.strategy import (
    ShippingCostCalculator,
    StandardShipping,
    ExpressShipping,
)
from behavioral.observer import OrderSubject, CustomerNotifier
from behavioral.command import (
    OrderService,
    PlaceOrderCommand,
    CancelOrderCommand,
    OrderController,
)



def main():
    # Create Products.
    laptop = Product(1, "Laptop", Decimal("800.00"))
    mouse = Product(2, "Mouse", Decimal("25.00"))

    # Create an order for a customer.
    order = Order("ORD-1001", "customer@example.com")

    # Add products to the order.
    order.add_product(laptop)
    order.add_product(mouse) 

    # Display order details.
    print(f"Order ID: {order.order_id}")
    print(f"Customer: {order.customer_email}")
    print(f"Status: {order.status}")

    print("\nProducts:")
    for product in order.items:
        print(f" - {product}")
    
    print(f"\nOrder Total: ${order.total:.2f}")

    #Creational- Factory Pattern Create a payment method based on customer selection.
    payment = PaymentFactory.create_payment("credit_card")
    # Process the order payment.
    print(payment.pay(float(order.total)))

    #Creational-Abstract Factory Pattern Create a compatible payment and shipping service.
    factory = PayPalCheckoutFactory()

    payment = factory.create_payment()
    shipping = factory.create_shipping()

    print(payment.pay(order.total))
    print(shipping.ship(order.order_id))

    # Creational-Builder Pattern Build an order step by step.
    built_order = (
        OrderBuilder("ORD-1002")
        .set_customer("customer@example.com")
        .add_product(laptop)
        .add_product(mouse)
        .set_shipping_address("Bhopal, India")
        .build()
    )

    print(f"Order ID: {built_order.order_id}")
    print(f"Customer: {built_order.customer_email}")
    print(f"Shipping: {built_order.shipping_address}")
    print(f"Total: ${built_order.total:.2f}")

    # Structural-Adapter Pattern
    gateway = ExternalPaymentGateway()
    adapter = PaymentAdapter(gateway)
    print(adapter.pay(order.total))

    # Structural-Decorator Pattern
    # Apply discount, then tax, then shipping.
    price = BasePrice(order.total)
    price = DiscountDecorator(price)
    price = TaxDecorator(price)
    price = ShippingDecorator(price, Decimal("50.00"))

    print(f"Final Price: ${price.calculate():.2f}")

    # Structural-Facade Pattern
    # One call coordinates all checkout services.
    checkout = CheckoutFacade()

    for result in checkout.checkout(order.order_id, order.total):
        print(result)

    # Behavioral-Strategy Pattern
    # Start with standard shipping.
    calculator = ShippingCostCalculator(StandardShipping())
    print(f"Standard: ${calculator.calculate(order.total):.2f}")

    # Switch to express shipping without changing the calculator.
    calculator.set_strategy(ExpressShipping())
    print(f"Express: ${calculator.calculate(order.total):.2f}")

    # Behavioral-Observer Pattern
    # Create an order status subject.
    subject = OrderSubject("ORD-1001")

    # Subscribe the customer to order updates.
    customer = CustomerNotifier()
    subject.subscribe(customer)

    # Status changes trigger notifications.
    subject.set_status("shipped")
    subject.set_status("delivered")

    # Behavioral-Command Pattern
    # Create the service and controller.
    service = OrderService()
    controller = OrderController()

    # Execute the place-order command.
    place_command = PlaceOrderCommand(service, "ORD-1001")
    controller.execute_command(place_command)

    # Execute the cancel-order command.
    cancel_command = CancelOrderCommand(service, "ORD-1001")
    controller.execute_command(cancel_command)

if __name__ == "__main__":
    main()        

