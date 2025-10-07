from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

# Sample data
products = [
    {
        "name": "Laptop",
        "varieties": [
            {"id": 1, "name": "Dell Inspiron 15", "price": 50000},
            {"id": 2, "name": "HP Pavilion x360", "price": 62000},
            {"id": 3, "name": "Apple MacBook Air", "price": 95000}
        ]
    },
    {
        "name": "Smartphone",
        "varieties": [
            {"id": 4, "name": "Samsung Galaxy S23", "price": 70000},
            {"id": 5, "name": "iPhone 14", "price": 80000},
            {"id": 6, "name": "OnePlus 11", "price": 60000}
        ]
    },
    {
        "name": "Headphones",
        "varieties": [
            {"id": 7, "name": "Sony WH-1000XM4", "price": 25000},
            {"id": 8, "name": "Boat Rockerz 450", "price": 1500},
            {"id": 9, "name": "JBL Tune 510BT", "price": 3500}
        ]
    },
    {
        "name": "Book",
        "varieties": [
            {"id": 10, "name": "Atomic Habits", "price": 500},
            {"id": 11, "name": "The Alchemist", "price": 400},
            {"id": 12, "name": "Rich Dad Poor Dad", "price": 450}
        ]
    },
    {
        "name": "Smartwatch",
        "varieties": [
            {"id": 13, "name": "Apple Watch SE", "price": 32000},
            {"id": 14, "name": "Samsung Galaxy Watch 5", "price": 28000},
            {"id": 15, "name": "Noise ColorFit Pro", "price": 3500}
        ]
    },
    {
        "name": "Bluetooth Speaker",
        "varieties": [
            {"id": 16, "name": "JBL Flip 5", "price": 8000},
            {"id": 17, "name": "Boat Stone 650", "price": 1800},
            {"id": 18, "name": "Sony SRS-XB13", "price": 3500}
        ]
    },
    {
        "name": "Backpack",
        "varieties": [
            {"id": 19, "name": "Wildcraft 35L", "price": 1200},
            {"id": 20, "name": "Skybags Brat", "price": 1400},
            {"id": 21, "name": "American Tourister", "price": 1800}
        ]
    },
    {
        "name": "Desk Lamp",
        "varieties": [
            {"id": 22, "name": "Philips LED Desk Lamp", "price": 900},
            {"id": 23, "name": "Wipro Garnet", "price": 1100},
            {"id": 24, "name": "Syska Table Lamp", "price": 850}
        ]
    },
    {
        "name": "Wireless Mouse",
        "varieties": [
            {"id": 25, "name": "Logitech M235", "price": 700},
            {"id": 26, "name": "HP X200", "price": 650},
            {"id": 27, "name": "Dell WM126", "price": 800}
        ]
    },
    {
        "name": "Water Bottle",
        "varieties": [
            {"id": 28, "name": "Milton Thermosteel", "price": 900},
            {"id": 29, "name": "Cello Puro", "price": 400},
            {"id": 30, "name": "Borosil Hydra", "price": 650}
        ]
    }
]
users = {}
orders = []

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
def home():
    return render_template('home.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists.')
        else:
            users[username] = password
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['user'] = username
            flash('Login successful.')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out.')
    return redirect(url_for('home'))

@app.route('/add_to_cart/<int:pid>')
def add_to_cart(pid):
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    cart = session.get('cart', [])
    cart.append(pid)
    session['cart'] = cart
    flash('Added to cart.')
    return redirect(url_for('home'))

def get_variety_by_id(pid):
    for p in products:
        for v in p['varieties']:
            if v['id'] == pid:
                return {"product": p["name"], **v}
    return None

@app.route('/cart')
def view_cart():
    cart_ids = session.get('cart', [])
    cart_items = []
    total = 0
    for pid in cart_ids:
        item = get_variety_by_id(pid)
        if item:
            cart_items.append(item)
            total += item['price']
    return render_template('cart.html', cart=cart_items, total=total)

@app.route('/place_order')
def place_order():
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    cart = session.get('cart', [])
    if not cart:
        flash('Cart is empty.')
        return redirect(url_for('home'))
    orders.append({'user': session['user'], 'items': cart.copy()})
    session['cart'] = []
    flash('Order placed successfully!')
    return redirect(url_for('view_cart'))

@app.route('/my_orders')
def my_orders():
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    user_orders = [o for o in orders if o['user'] == session['user']]
    return render_template('orders.html', orders=user_orders)

if __name__ == '__main__':
    app.run(debug=True)