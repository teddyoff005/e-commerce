# cart.py
# Handles cart operations for the current user

cart = []

def add_to_cart(product):
    cart.append(product)
    print(f"Added {product['name']} to cart.")

def view_cart():
    if not cart:
        print("Cart is empty.")
        return
    print("\nYour Cart:")
    total = 0
    for idx, item in enumerate(cart, 1):
        print(f"{idx}. {item['name']} - Rs.{item['price']}")
        total += item['price']
    print(f"Total: Rs.{total}")

def clear_cart():
    cart.clear()
