from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import db, User, Product, Order
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:C-sharp909!@localhost:8800/Ernur_1'
app.config['SECRET_KEY'] = 's00987sss78900s'
db.init_app(app)

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return redirect(url_for('catalog'))

@app.route('/catalog')
def catalog():
    products = Product.query.all()
    return render_template('catalog.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Пользователь уже существует!')
            return redirect(url_for('register'))
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна! Теперь войдите.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash('Вход выполнен успешно!')
            return redirect(url_for('catalog'))
        flash('Неверный логин или пароль!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из аккаунта.')
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        flash('Нет прав администратора!')
        return redirect(url_for('catalog'))
    products = Product.query.all()
    users = User.query.all()
    orders = Order.query.all()
    return render_template('admin.html', products=products, users=users, orders=orders)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if not session.get('is_admin'):
        flash('Нет прав администратора!')
        return redirect(url_for('catalog'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image_url = request.form['image_url']
        product = Product(name=name, description=description, price=price, image_url=image_url)
        db.session.add(product)
        db.session.commit()
        flash('Товар добавлен!')
        return redirect(url_for('catalog'))
    return render_template('add_product.html')

@app.route('/order/<int:product_id>', methods=['POST'])
def order(product_id):
    if 'user_id' not in session:
        flash('Сначала войдите в аккаунт!')
        return redirect(url_for('login'))
    quantity = int(request.form.get('quantity', 1))
    order = Order(user_id=session['user_id'], product_id=product_id, quantity=quantity)
    db.session.add(order)
    db.session.commit()
    flash('Заказ оформлен!')
    return redirect(url_for('orders'))

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        flash('Сначала войдите в аккаунт!')
        return redirect(url_for('login'))
    orders = Order.query.filter_by(user_id=session['user_id']).all()
    return render_template('orders.html', orders=orders)

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            cart_items.append({'product': product, 'quantity': quantity})
            total += product.price * quantity
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    session['cart'] = cart
    flash('Товар добавлен в корзину!')
    return redirect(url_for('catalog'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    flash('Товар удалён из корзины!')
    return redirect(url_for('cart'))

@app.route('/make_order', methods=['POST'])
def make_order():
    if 'user_id' not in session:
        flash('Сначала войдите в аккаунт!')
        return redirect(url_for('login'))
    cart = session.get('cart', {})
    if not cart:
        flash('Корзина пуста!')
        return redirect(url_for('cart'))
    for product_id, quantity in cart.items():
        order = Order(user_id=session['user_id'], product_id=int(product_id), quantity=quantity)
        db.session.add(order)
    db.session.commit()
    session['cart'] = {}
    flash('Заказ оформлен!')
    return redirect(url_for('orders'))


if __name__ == '__main__':
    create_tables()  
    app.run(debug=True)