# Build the Product API
# We’ll implement POST /products using Pydantic, Controller, Service, Repository, and your existing PostgreSQL database.

# What each layer does
# Component	Purpose	Example
# Pydantic	Validates request/response data	Reject negative quantity
# Controller / API	Handles HTTP requests and responses	POST /products
# Service	Implements business rules	Check product availability
# Repository	Handles database queries	Insert or retrieve product
# SQLAlchemy model	Maps Python objects to database tables	ProductModel
# PostgreSQL	Permanently stores data	products table

# Request → Pydantic → Controller → Service → Repository → Database

from fastapi import FastAPI
# Import API routers from your project.
from rest_api.api.products import router as products_router
from rest_api.api.customers import router as customers_router
from rest_api.api.orders import router as orders_router


app = FastAPI(title="E-Commerce Order Processing API")

# Register product endpoints with the main application.
app.include_router(products_router)

# Register customer endpoints.
app.include_router(customers_router)

# Register Order APIs.
app.include_router(orders_router)


# Health check endpoint.
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}