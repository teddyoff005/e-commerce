# orders.py
# Handles order placement

orders = []

def place_order(user, cart):
    if not cart:
        print("Cart is empty. Cannot place order.")
        return
    order = {
        "user": user,
        "items": cart.copy()
    }
    orders.append(order)
    print(f"Order placed successfully for {user}!")

def view_orders(user):
    print(f"\nOrders for {user}:")
    found = False
    for order in orders:
        if order["user"] == user:
            found = True
            print("Order:")
            for item in order["items"]:
                product = item['product']
                quantity = item['quantity']
                print(f"- {product['name']} - Rs.{product['price']} x {quantity}")
    if not found:
        print("No orders found.")
