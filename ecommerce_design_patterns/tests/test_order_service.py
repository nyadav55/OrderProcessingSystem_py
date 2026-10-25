# Expected result: 4 tests passed.
# These are unit tests using a mocked repository; 
# they don't require PostgreSQL to run. Your existing database integration test can still be run separately.
# Run in root - python -m pytest tests/ -v 

# Import pytest to verify expected errors and run test cases
import pytest

# Import Mock to simulate repository behavior without a real database
from unittest.mock import Mock

# Import the service containing order business rules
from services.order_service import OrderService

# Import the repository that handles order database operations
from repositories.order_repository import OrderRepository


# Verify that valid order details are passed to the repository
def test_create_order_success():
    # Create a mock repository to isolate the service from PostgreSQL
    repository = Mock()

    # Simulate that the order number does not already exist
    repository.get_by_order_number.return_value = None

    # Simulate the order returned after successful persistence
    saved_order = Mock(id=1, order_number="ORD-1001")
    repository.create.return_value = saved_order

    # Inject the mock repository into the service
    service = OrderService(order_repository=repository)

    # Call the service with valid order details
    result = service.create_order(
        db=Mock(),
        order_number="ORD-1001",
        customer_email="customer@example.com"
    )

    # Verify that the service returns the saved order
    assert result.id == 1

    # Verify that the repository was asked to save the correct order
    repository.create.assert_called_once()


# Verify that duplicate order numbers are rejected
def test_create_order_duplicate_number():
    # Create a mock repository that finds an existing order
    repository = Mock()
    repository.get_by_order_number.return_value = Mock(
        order_number="ORD-1001"
    )

    # Inject the mock repository into the service
    service = OrderService(order_repository=repository)

    # Verify that duplicate order numbers raise a validation error
    with pytest.raises(ValueError, match="Order number already exists"):
        service.create_order(
            db=Mock(),
            order_number="ORD-1001",
            customer_email="customer@example.com"
        )

    # Ensure the service never attempts to save a duplicate
    repository.create.assert_not_called()


# Verify that an empty order number is rejected
def test_create_order_empty_number():
    # Inject a mock repository to avoid database access
    repository = Mock()
    service = OrderService(order_repository=repository)

    # Verify that invalid input raises a clear error
    with pytest.raises(ValueError, match="Order number cannot be empty"):
        service.create_order(
            db=Mock(),
            order_number="   ",
            customer_email="customer@example.com"
        )

    # Ensure validation happens before any repository query
    repository.get_by_order_number.assert_not_called()


# Verify that an empty customer email is rejected
def test_create_order_empty_email():
    # Inject a mock repository to isolate the validation test
    repository = Mock()
    service = OrderService(order_repository=repository)

    # Verify that invalid email input raises a clear error
    with pytest.raises(ValueError, match="Customer email cannot be empty"):
        service.create_order(
            db=Mock(),
            order_number="ORD-1002",
            customer_email=" "
        )

    # Ensure invalid input never reaches the repository
    repository.get_by_order_number.assert_not_called()

# Part 2
# Verify that a failed database commit triggers a rollback
def test_create_order_rolls_back_on_commit_failure():
    # Create a mock database session to simulate a transaction
    db = Mock()

    # Simulate a database failure when committing the transaction
    db.commit.side_effect = RuntimeError("Simulated database failure")

    # Create the repository responsible for saving orders
    repository = OrderRepository()

    # Verify that the original database error is re-raised
    with pytest.raises(RuntimeError, match="Simulated database failure"):
        repository.create(
            db,
            order_number="ORD-ROLLBACK-TEST",
            customer_email="test@example.com"
        )

    # Verify that the failed transaction was rolled back
    db.rollback.assert_called_once()

    # Verify that the repository attempted to commit the transaction
    db.commit.assert_called_once()

    # Verify that the order was never refreshed after the failed commit
    db.refresh.assert_not_called()
