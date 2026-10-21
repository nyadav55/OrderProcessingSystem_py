# OrderProcessingSystem_py
Category,Pattern,Real-world use
1-- Creational
    Singleton-One shared database connection,
    Factory Method-Create Electronics vs Clothing products,
    Abstract Factory-Stripe / PayPal payment families,
    Builder-Step-by-step Order construction
2-- Structural
    Adapter-Wrap legacy payment system,
    Decorator-Gift wrap + Express + Insurance,
    Facade-One simple place_order() method
3-- Behavioral
    Strategy-Swap shipping & discount algorithms,
    Observer-"Notify customer, warehouse, analytics",
    Command-Place/Cancel orders with Undo

# Strucutre & CMD (powershell)
ecommerce_design_patterns/
├── README.md
├── requirements.txt
├── main.py                    ← run this
├── creational/
│   ├── singleton.py
│   ├── factory_method.py
│   ├── abstract_factory.py
│   └── builder.py
├── structural/
│   ├── adapter.py
│   ├── decorator.py
│   └── facade.py
├── behavioral/
│   ├── strategy.py
│   ├── observer.py
│   └── command.py
└── models/
    ├── product.py
    └── order.py  folow this structure and give cmd to create it

# 1. Create project root
mkdir ecommerce_design_patterns
cd ecommerce_design_patterns

# 2. Create pattern and model directories
mkdir creational, structural, behavioral, models

# 3. Create root files
New-Item README.md -ItemType File
New-Item requirements.txt -ItemType File
New-Item main.py -ItemType File

# 4. Creational patterns
New-Item creational/singleton.py -ItemType File
New-Item creational/factory_method.py -ItemType File
New-Item creational/abstract_factory.py -ItemType File
New-Item creational/builder.py -ItemType File

# 5. Structural patterns
New-Item structural/adapter.py -ItemType File
New-Item structural/decorator.py -ItemType File
New-Item structural/facade.py -ItemType File

# 6. Behavioral patterns
New-Item behavioral/strategy.py -ItemType File
New-Item behavioral/observer.py -ItemType File
New-Item behavioral/command.py -ItemType File

# 7. Models
New-Item models/product.py -ItemType File
New-Item models/order.py -ItemType File

# 8. Create package initialization files
New-Item creational/__init__.py -ItemType File
New-Item structural/__init__.py -ItemType File
New-Item behavioral/__init__.py -ItemType File
New-Item models/__init__.py -ItemType File
