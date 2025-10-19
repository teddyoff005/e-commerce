# cart.py
# Handles cart operations for the current user

cart = []

def add_to_cart(product):
    # Check if product is already in cart
    for item in cart:
        if item['product']['id'] == product['id']:
            item['quantity'] += 1
            print(f"Increased quantity of {product['name']} to {item['quantity']}.")
            return
    # If not in cart, add it with quantity 1
    cart.append({'product': product, 'quantity': 1})
    print(f"Added {product['name']} to cart.")

def view_cart():
    if not cart:
        print("Cart is empty.")
        return
    print("\nYour Cart:")
    total = 0
    for idx, item in enumerate(cart, 1):
        product = item['product']
        quantity = item['quantity']
        print(f"{idx}. {product['name']} - Rs.{product['price']} x {quantity}")
        total += product['price'] * quantity
    print(f"Total: Rs.{total}")

def clear_cart():
    cart.clear()