# This layer handles database operations, keeping SQLAlchemy queries out of the API and business logic.

from sqlalchemy.orm import Session
from db.models.product import ProductModel


def create_product(db: Session, product_data: dict) -> ProductModel:
    # Create a database model using validated product data.
    product = ProductModel(**product_data)

    # Add the product to the current database transaction.
    db.add(product)

    try:
        # Save the product in PostgreSQL.
        db.commit()

        # Refresh the object to retrieve database-generated values, such as ID.
        db.refresh(product)

        # Return the saved product; otherwise, the API may return None.
        return product

    except Exception:
        # Roll back changes if saving fails.
        db.rollback()

        # Re-raise the error so it can be diagnosed.
        raise


def list_products(db: Session) -> list[ProductModel]:
    # Fetch all products ordered by ID.
    return db.query(ProductModel).order_by(ProductModel.id).all()

def get_product_by_id(db: Session, product_id: int) -> ProductModel | None:
    # Search for a product using its primary key.
    # Return None when the product does not exist.
    return db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()


# Step 2: Update Product API (PUT)
def update_product(
    db: Session,
    product_id: int,
    product_data: dict,
) -> ProductModel | None:
    # Find the product to update.
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()

    # Return None if the product does not exist.
    if product is None:
        return None

    # Apply the validated fields to the existing product.
    for field, value in product_data.items():
        setattr(product, field, value)

    try:
        # Persist changes to PostgreSQL.
        db.commit()

        # Refresh the object with the saved database values.
        db.refresh(product)
        return product

    except Exception:
        # Undo the transaction if the update fails.
        db.rollback()
        raise

# Step 3: Delete Product API
def delete_product(db: Session, product_id: int) -> bool:
    # Find the product by its database ID.
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()

    # Return False if the product does not exist.
    if product is None:
        return False

    try:
        # Mark the product for deletion.
        db.delete(product)

        # Persist the deletion in PostgreSQL.
        db.commit()
        return True

    except Exception:
        # Undo the transaction if deletion fails.
        db.rollback()
        raise