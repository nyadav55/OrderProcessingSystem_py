from schemas.product import ProductCreate

# Test valid product input.
product = ProductCreate(
    name="Wireless Mouse",
    quantity=10,
    price="25.00",
)

print(product.model_dump())

# Test invalid input.
try:
    ProductCreate(name="M", quantity=-1, price="-5")
except Exception as error:
    print("Validation correctly rejected invalid data.")
    