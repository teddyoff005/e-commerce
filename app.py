from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

# Sample data
products = [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Smartphone", "price": 20000},
    {"id": 3, "name": "Headphones", "price": 1500}
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
    product = next((p for p in products if p['id'] == pid), None)
    if product:
        cart.append(product)
        session['cart'] = cart
        flash(f"Added {product['name']} to cart.")
    return redirect(url_for('home'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

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
    return redirect(url_for('my_orders'))

@app.route('/my_orders')
def my_orders():
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    user_orders = [o for o in orders if o['user'] == session['user']]
    return render_template('orders.html', orders=user_orders)

if __name__ == '__main__':
    app.run(debug=True)