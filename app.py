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
    },
    {
        "name": "Dress (Men)",
        "varieties": [
            {"id": 31, "name": "Formal Shirt", "price": 1200},
            {"id": 32, "name": "Casual T-Shirt", "price": 600},
            {"id": 33, "name": "Jeans", "price": 1500},
            {"id": 34, "name": "Kurta", "price": 900}
        ]
    },
    {
        "name": "Dress (Women)",
        "varieties": [
            {"id": 35, "name": "Saree", "price": 2000},
            {"id": 36, "name": "Kurti", "price": 800},
            {"id": 37, "name": "Western Dress", "price": 1800},
            {"id": 38, "name": "Leggings", "price": 400}
        ]
    },
    {
        "name": "Dress (Kids)",
        "varieties": [
            {"id": 39, "name": "Frock", "price": 700},
            {"id": 40, "name": "Dungaree", "price": 900},
            {"id": 41, "name": "Kids T-Shirt", "price": 350},
            {"id": 42, "name": "Shorts", "price": 400}
        ]
    },
    {
        "name": "Dress (Unisex)",
        "varieties": [
            {"id": 43, "name": "Hoodie", "price": 1200},
            {"id": 44, "name": "Track Pants", "price": 900},
            {"id": 45, "name": "Raincoat", "price": 1100}
        ]
    },
    {
        "name": "Shoes",
        "varieties": [
            {"id": 46, "name": "Nike Running Shoes", "price": 3500},
            {"id": 47, "name": "Adidas Sneakers", "price": 4000},
            {"id": 48, "name": "Bata Formal Shoes", "price": 1800}
        ]
    },
    {
        "name": "Sunglasses",
        "varieties": [
            {"id": 49, "name": "Ray-Ban Aviator", "price": 6500},
            {"id": 50, "name": "Fastrack Wayfarer", "price": 1200},
            {"id": 51, "name": "Vincent Chase Round", "price": 900}
        ]
    },
    {
        "name": "Cycle",
        "varieties": [
            {"id": 52, "name": "Hero Sprint Next 26T", "price": 8500},
            {"id": 53, "name": "Firefox Bad Attitude 8", "price": 12000},
            {"id": 54, "name": "Btwin Rockrider ST 100", "price": 15000}
        ]
    },
    {
        "name": "Bike",
        "varieties": [
            {"id": 55, "name": "Royal Enfield Classic 350", "price": 210000},
            {"id": 56, "name": "Bajaj Pulsar 150", "price": 120000},
            {"id": 57, "name": "Yamaha FZ-S V3", "price": 130000}
        ]
    },
    {
        "name": "Car",
        "varieties": [
            {"id": 58, "name": "Maruti Suzuki Swift", "price": 600000},
            {"id": 59, "name": "Hyundai Creta", "price": 1100000},
            {"id": 60, "name": "Tata Nexon", "price": 900000}
        ]
    },
    {
        "name": "Tablet",
        "varieties": [
            {"id": 61, "name": "Apple iPad 9th Gen", "price": 32000},
            {"id": 62, "name": "Samsung Galaxy Tab A8", "price": 18000},
            {"id": 63, "name": "Lenovo Tab M10", "price": 15000}
        ]
    },
    {
        "name": "Camera",
        "varieties": [
            {"id": 64, "name": "Canon EOS 1500D", "price": 35000},
            {"id": 65, "name": "Nikon D3500", "price": 40000},
            {"id": 66, "name": "Sony Alpha ILCE-6100", "price": 65000}
        ]
    },
    {
        "name": "Gaming Console",
        "varieties": [
            {"id": 67, "name": "Sony PlayStation 5", "price": 49990},
            {"id": 68, "name": "Microsoft Xbox Series S", "price": 34990},
            {"id": 69, "name": "Nintendo Switch", "price": 29990}
        ]
    },
    {
        "name": "Television",
        "varieties": [
            {"id": 70, "name": "Samsung 43\" 4K UHD", "price": 35000},
            {"id": 71, "name": "Sony Bravia 50\" 4K", "price": 55000},
            {"id": 72, "name": "Mi 40\" Full HD", "price": 25000}
        ]
    },
    {
        "name": "Refrigerator",
        "varieties": [
            {"id": 73, "name": "LG 260L Double Door", "price": 27000},
            {"id": 74, "name": "Samsung 253L 3 Star", "price": 24000},
            {"id": 75, "name": "Whirlpool 190L Single Door", "price": 16000}
        ]
    },
    {
        "name": "Washing Machine",
        "varieties": [
            {"id": 76, "name": "Bosch 7kg Front Load", "price": 32000},
            {"id": 77, "name": "LG 6.5kg Top Load", "price": 21000},
            {"id": 78, "name": "Samsung 7kg Top Load", "price": 22000}
        ]
    },
    {
        "name": "Microwave Oven",
        "varieties": [
            {"id": 79, "name": "IFB 20L Convection", "price": 9500},
            {"id": 80, "name": "Samsung 23L Solo", "price": 8000},
            {"id": 81, "name": "LG 28L Convection", "price": 14000}
        ]
    }
    # ...add more as needed...
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
    user_orders = []
    for o in orders:
        if o['user'] == session['user']:
            items = [get_variety_by_id(pid) for pid in o['items']]
            user_orders.append({'items': items})
    return render_template('orders.html', user_orders=user_orders)

@app.route('/checkout')
def checkout():
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    cart_ids = session.get('cart', [])
    cart_items = []
    total = 0
    for pid in cart_ids:
        item = get_variety_by_id(pid)
        if item:
            cart_items.append(item)
            total += item['price']
    return render_template('checkout.html', cart=cart_items, total=total)

if __name__ == '__main__':
    app.run(debug=True)