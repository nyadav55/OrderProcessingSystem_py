# Step 5.5 acceptance criteria
# - Valid transitions are accepted.
# - Invalid transitions and unknown statuses are rejected.
# - Missing orders return a clear error.
# - Status updates commit to PostgreSQL; database failures roll back.
# Run - python -m pytest tests/ -v
# o/p - 9 passed

# Import pytest to verify expected validation errors
import pytest

# Import Mock to isolate service tests from PostgreSQL
from unittest.mock import Mock

# Import SimpleNamespace to create a lightweight order object
from types import SimpleNamespace

# Import the service that enforces order lifecycle rules
from services.order_service import OrderService


# Verify that a valid status transition is persisted
def test_created_order_can_be_paid():
    # Create a fake order in its initial state
    order = SimpleNamespace(order_number="ORD-1001", status="created")

    # Mock repository calls so no real database is needed
    repository = Mock()
    repository.get_by_order_number.return_value = order
    repository.update_status.return_value = order

    # Create the service with the mocked repository
    service = OrderService(order_repository=repository)

    # Request a valid status transition
    result = service.update_order_status(
        Mock(), "ORD-1001", "paid"
    )

    # Verify that the repository received the validated update
    repository.update_status.assert_called_once_with(
        repository.get_by_order_number.call_args.args[0],
        order,
        "paid",
    )
    assert result.status == "created"  # Mock repository does not change the object


# Verify that an invalid transition is rejected
def test_delivered_order_cannot_be_cancelled():
    # Create an order that has already been delivered
    order = SimpleNamespace(order_number="ORD-1002", status="delivered")

    # Configure the repository to return the existing order
    repository = Mock()
    repository.get_by_order_number.return_value = order

    # Create the service with the mocked repository
    service = OrderService(order_repository=repository)

    # Confirm that the invalid transition raises an error
    with pytest.raises(ValueError, match="Cannot change order status"):
        service.update_order_status(Mock(), "ORD-1002", "cancelled")

    # Ensure the invalid update was never persisted
    repository.update_status.assert_not_called()


# Verify that unsupported status names are rejected
def test_unknown_status_is_rejected():
    # Create the service without needing a real repository
    repository = Mock()
    service = OrderService(order_repository=repository)

    # Confirm that an unsupported status fails validation
    with pytest.raises(ValueError, match="Invalid order status"):
        service.update_order_status(Mock(), "ORD-1003", "processing")

    # Ensure invalid input does not trigger a database lookup
    repository.get_by_order_number.assert_not_called()


# Verify that a missing order is reported clearly
def test_missing_order_is_rejected():
    # Simulate an order number that does not exist
    repository = Mock()
    repository.get_by_order_number.return_value = None

    # Create the service with the mocked repository
    service = OrderService(order_repository=repository)

    # Confirm that the service reports the missing order
    with pytest.raises(ValueError, match="Order not found"):
        service.update_order_status(Mock(), "ORD-MISSING", "paid")

    # Ensure no status update was attempted
    repository.update_status.assert_not_called()