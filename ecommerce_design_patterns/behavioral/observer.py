# Observer pattern establishes a one-to-many relationship so that subscribers are automatically notified when an object's state changes.
# Goal: Automatically notify subscribers when an order's status changes.

# Real-world example: When an order is shipped, the customer receives a notification.


from abc import ABC, abstractmethod


# Defines the interface for anyone receiving order updates.
class OrderObserver(ABC):

    @abstractmethod
    def update(self, order_id: str, status: str) -> None:
        pass


# Customer notification subscriber.
class CustomerNotifier(OrderObserver):

    def update(self, order_id: str, status: str) -> None:
        print(f"Notification: Order {order_id} is {status}")


# Order manages subscribers and sends notifications.
class OrderSubject:

    def __init__(self, order_id: str):
        self.order_id = order_id
        self.status = "created"
        self.observers: list[OrderObserver] = []

    def subscribe(self, observer: OrderObserver) -> None:
        # Register a subscriber.
        self.observers.append(observer)

    def unsubscribe(self, observer: OrderObserver) -> None:
        # Remove a subscriber.
        if observer in self.observers:
            self.observers.remove(observer)

    def set_status(self, status: str) -> None:
        # Update status, then notify every subscriber.
        self.status = status

        for observer in self.observers:
            observer.update(self.order_id, self.status)
