# users.py
# Handles user registration and login (simulated, no real authentication)

users = {}

current_user = None

def register():
    global users
    username = input("Enter new username: ")
    if username in users:
        print("Username already exists!")
        return False
    password = input("Enter password: ")
    users[username] = password
    print("Registration successful!")
    return True

def login():
    global current_user
    username = input("Enter username: ")
    password = input("Enter password: ")
    if users.get(username) == password:
        current_user = username
        print(f"Welcome, {username}!")
        return True
    else:
        print("Invalid credentials!")
        return False

def get_current_user():
    return current_user

def logout():
    global current_user
    current_user = None
    print("Logged out.")
