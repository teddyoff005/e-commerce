# products.py
# Handles product listing and management

products = [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Smartphone", "price": 20000},
    {"id": 3, "name": "Headphones", "price": 1500},
    {"id": 4, "name": "Book", "price": 500},
]

def list_products():
    print("\nAvailable Products:")
    for product in products:
        print(f"{product['id']}. {product['name']} - Rs.{product['price']}")

def get_product_by_id(pid):
    for product in products:
        if product["id"] == pid:
            return product
    return None
