# Phase 5 — Database and Business Logic
Step	Task	Technology
5.1	Add automated unit tests	pytest
5.2	Define database models	SQLAlchemy
5.3	Connect to database	PostgreSQL
5.4	Add schema migrations	Alembic
5.5	Implement repositories and services	Repository + Service layers
5.6	Add inventory and order validation	Business rules
5.7	Add transactions and rollback	Database integrity

Step 5.1 — Add unit tests

tests/
├── __init__.py
├── test_product.py
├── test_order.py
├── test_factory_method.py
├── test_decorator.py
└── test_strategy.py

# Create the files in their respective folders
New-Item -ItemType Directory tests
@('__init__.py', 'test_product.py', 'test_order.py', 'test_factory_method.py', 'test_decorator.py', 'test_strategy.py') | 
    ForEach-Object { New-Item -ItemType File "tests/$_" }


install pytest
python -m pip install pytest
python -m pytest -v

Phase 5.2 — Define Database Models using SQLAlchemy
python -m pip install sqlalchemy psycopg[binary]

ecommerce_design_patterns/
└── db/
    ├── __init__.py
    ├── base.py
    └── models/
        ├── __init__.py
        ├── product.py
        ├── order.py
        └── order_item.py
# Create the nested folders first
New-Item -ItemType Directory -Path "db/models" -Force

# Create the files in their respective folders
New-Item -ItemType File "db/__init__.py"
New-Item -ItemType File "db/base.py"
New-Item -ItemType File "db/models/__init__.py"
New-Item -ItemType File "db/models/product.py"
New-Item -ItemType File "db/models/order.py"
New-Item -ItemType File "db/models/order_item.py"

New-Item -ItemType File -Force repositories\order_repository.py
db/ — database connection and models.
repositories/ — database operations for products and orders.

# Step 5.6 - Install Alembic for managing database schema versions
python -m pip install alembic

# Save the installed dependency list
python -m pip freeze > requirements.txt

# Create the Alembic configuration and migration directory
python -m alembic init migrations
This creates alembic.ini and the migrations/ folder.