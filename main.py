# main.py
# Entry point and menu-driven interface

import products
import users
import cart
import orders

def main_menu():
    while True:
        print("\n--- E-Commerce Store ---")
        print("1. Register")
        print("2. Login")
        print("3. List Products")
        print("4. Add Product to Cart")
        print("5. View Cart")
        print("6. Place Order")
        print("7. View My Orders")
        print("8. Logout")
        print("9. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            users.register()
        elif choice == '2':
            users.login()
        elif choice == '3':
            products.list_products()
        elif choice == '4':
            if not users.get_current_user():
                print("Please login first.")
                continue
            products.list_products()
            try:
                pid = int(input("Enter product ID to add to cart: "))
                product = products.get_product_by_id(pid)
                if product:
                    cart.add_to_cart(product)
                else:
                    print("Invalid product ID.")
            except ValueError:
                print("Invalid input.")
        elif choice == '5':
            cart.view_cart()
        elif choice == '6':
            user = users.get_current_user()
            if not user:
                print("Please login first.")
                continue
            orders.place_order(user, cart.cart)
            cart.clear_cart()
        elif choice == '7':
            user = users.get_current_user()
            if not user:
                print("Please login first.")
                continue
            orders.view_orders(user)
        elif choice == '8':
            users.logout()
        elif choice == '9':
            print("Thank you for visiting!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
