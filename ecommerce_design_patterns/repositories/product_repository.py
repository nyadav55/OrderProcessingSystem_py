


from sqlalchemy.orm import Session
from db.models import ProductModel


class ProductRepository:
    # Save a new product in PostgreSQL
    def create(self, db: Session, name: str, price):
        product = ProductModel(name=name, price=price)

        try:
            db.add(product)       # Prepare product for saving
            db.commit()           # Save changes to database
            db.refresh(product)   # Fetch generated ID

        except Exception:
            db.rollback()         # Undo failed transaction
            raise                 # Re-raise the original error

        return product            # Return after successful save

    # Find a product using its ID
    def get_by_id(self, db: Session, product_id: int):
        return db.get(ProductModel, product_id)

    # Get all products
    def get_all(self, db: Session):
        return db.query(ProductModel).all()
