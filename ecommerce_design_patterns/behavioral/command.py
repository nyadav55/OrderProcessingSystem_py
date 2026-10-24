# Commands separate the request from the code that executes it. 
# This makes actions easier to log, queue, test, and extend.
# Goal: Encapsulate an action as an object so it can be executed, logged, queued, or potentially undone.

# E-commerce example: Place an order or cancel an order using separate command objects.


from abc import ABC, abstractmethod

# Common interface for all commands.
class Command(ABC):

    @abstractmethod
    def execute(self) -> str:
        pass

# Business object that performs the actual operations.
class OrderService:

    def place_order(self, order_id: str) -> str:
        return f"Order {order_id} placed successfully"

    def cancel_order(self, order_id: str) -> str:
        return f"Order {order_id} cancelled successfully"

# Command for placing an order.
class PlaceOrderCommand(Command):

    def __init__(self, service: OrderService, order_id: str):
        self.service = service
        self.order_id = order_id

    def execute(self) -> str:
        return self.service.place_order(self.order_id)

# Command for cancelling an order.
class CancelOrderCommand(Command):

    def __init__(self, service: OrderService, order_id: str):
        self.service = service
        self.order_id = order_id

    def execute(self) -> str:
        return self.service.cancel_order(self.order_id)

# Invoker executes commands without knowing their details.
class OrderController:

    def execute_command(self, command: Command) -> None:
        print(command.execute())
