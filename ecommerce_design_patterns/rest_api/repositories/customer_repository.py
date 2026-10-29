from sqlalchemy.orm import Session

# Import your SQLAlchemy Customer model.
from db.models.customer import CustomerModel


# Create a new customer.
def create_customer(db: Session, customer_data: dict) -> CustomerModel:
    # Convert dictionary data into a CustomerModel object.
    customer = CustomerModel(**customer_data)

    # Stage the new customer for insertion.
    db.add(customer)

    try:
        # Save the record to PostgreSQL.
        db.commit()

        # Load database-generated fields such as ID.
        db.refresh(customer)

        # Return the saved customer to the service layer.
        return customer

    except Exception:
        # Roll back the transaction if insertion fails.
        db.rollback()
        raise


# Retrieve all customers.
def list_customers(db: Session) -> list[CustomerModel]:
    # Return customers sorted by ID.
    return db.query(CustomerModel).order_by(CustomerModel.id).all()


# Find a customer by ID.
def get_customer_by_id(
    db: Session,
    customer_id: int,
) -> CustomerModel | None:
    # Return None when no customer matches.
    return db.query(CustomerModel).filter(
        CustomerModel.id == customer_id
    ).first()


# Find a customer by email.
def get_customer_by_email(
    db: Session,
    email: str,
) -> CustomerModel | None:
    # Used to prevent duplicate customer registrations.
    return db.query(CustomerModel).filter(
        CustomerModel.email == email
    ).first()

def update_customer(
    db: Session,
    customer_id: int,
    customer_data: dict,
) -> CustomerModel | None:

    # Find the customer by ID.
    customer = db.query(CustomerModel).filter(
        CustomerModel.id == customer_id
    ).first()

    # Return None if the customer doesn't exist.
    if customer is None:
        return None

    # Update only the allowed customer fields.
    customer.name = customer_data["name"]
    customer.email = customer_data["email"]

    try:
        # Save changes to PostgreSQL.
        db.commit()

        # Refresh the customer with updated database values.
        db.refresh(customer)

        # Return the updated customer.
        return customer

    except Exception:
        # Undo the transaction if an error occurs.
        db.rollback()
        raise

# Customer Delete API
def delete_customer(db: Session, customer_id: int) -> bool:
    # Find the customer in PostgreSQL.
    customer = db.query(CustomerModel).filter(
        CustomerModel.id == customer_id
    ).first()

    # Return False if the customer does not exist.
    if customer is None:
        return False

    try:
        # Mark the customer for deletion.
        db.delete(customer)

        # Permanently save the deletion.
        db.commit()

        # Confirm successful deletion.
        return True

    except Exception:
        # Roll back the transaction if deletion fails.
        db.rollback()
        raise    