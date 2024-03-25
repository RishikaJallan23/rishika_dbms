from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Define database models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.String(20), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

# Create tables
with app.app_context():
    db.create_all()
    # Sample data
    sample_data = {
        'Customer': [
            {'name': 'John Doe', 'email': 'john@example.com', 'address': '123 Main St, Anytown'},
            {'name': 'Jane Smith', 'email': 'jane@example.com', 'address': '456 Elm St, Othertown'}
        ],
        'Employee': [
            {'name': 'Alice Johnson', 'position': 'Manager', 'department': 'Sales'},
            {'name': 'Bob Williams', 'position': 'Clerk', 'department': 'Inventory'}
        ],
        'Stock': [
            {'product_id': 1, 'quantity': 100},
            {'product_id': 2, 'quantity': 50}
        ],
        'Supplier': [
            {'name': 'ABC Supplies', 'email': 'info@abc.com', 'address': '789 Oak St, Yetanothertown'},
            {'name': 'XYZ Distributors', 'email': 'info@xyz.com', 'address': '321 Maple St, Somewhere'}
        ],
        'Order': [
            {'customer_id': 1, 'product_id': 1, 'quantity': 5, 'order_date': '2024-03-22'},
            {'customer_id': 2, 'product_id': 2, 'quantity': 10, 'order_date': '2024-03-22'}
        ],
        'Product': [
            {'name': 'Widget', 'description': 'A simple widget', 'price': 10.99},
            {'name': 'Gadget', 'description': 'An advanced gadget', 'price': 24.99}
        ]
    }
    # Insert sample data into tables
    for table_name, data in sample_data.items():
        model_class = globals()[table_name]
        if not db.session.query(model_class).count():
            for entry in data:
                db.session.add(model_class(**entry))
            db.session.commit()

# Routes
@app.route('/')
def index():
    return render_template('index.html',
                           customers=Customer.query.all(),
                           employees=Employee.query.all(),
                           stocks=Stock.query.all(),
                           suppliers=Supplier.query.all(),
                           orders=Order.query.all(),
                           products=Product.query.all())

@app.route('/customers')
def customers():
    return render_template('customers.html', customers=Customer.query.all())

@app.route('/add_customer', methods=['POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        new_customer = Customer(name=name, email=email, address=address)
        db.session.add(new_customer)
        db.session.commit()
    return redirect(url_for('customers'))

@app.route('/delete_customer/<int:id>', methods=['POST'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('customers'))

@app.route('/modify_customer/<int:id>', methods=['POST'])
def modify_customer(id):
    customer = Customer.query.get_or_404(id)
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.email = request.form['email']
        customer.address = request.form['address']
        db.session.commit()
    return redirect(url_for('customers'))
@app.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

# Route to add a new product
@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        new_product = Product(name=name, price=price, description=description)
        db.session.add(new_product)
        db.session.commit()
    return redirect(url_for('products'))

# Route to delete a product
@app.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products'))

# Route to modify a product
@app.route('/modify_product/<int:id>', methods=['POST'])
def modify_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.description = request.form['description']
        db.session.commit()
    return redirect(url_for('products'))

# Routes for Order
@app.route('/orders')
def orders():
    all_orders = Order.query.all()
    return render_template('orders.html', orders=all_orders)

@app.route('/add_order', methods=['POST'])
def add_order():
    if request.method == 'POST':
        customer_id = int(request.form['customer_id'])
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        order_date = datetime.utcnow()
        
        new_order = Order(customer_id=customer_id, product_id=product_id, quantity=quantity, order_date=order_date)
        db.session.add(new_order)
        db.session.commit()
    return redirect(url_for('orders'))

# Route to delete an order
@app.route('/delete_order/<int:id>', methods=['POST'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('orders'))

# Route to modify an order
@app.route('/modify_order/<int:id>', methods=['POST'])
def modify_order(id):
    order = Order.query.get_or_404(id)
    if request.method == 'POST':
        order.customer_id = int(request.form['customer_id'])
        order.product_id = int(request.form['product_id'])
        order.quantity = int(request.form['quantity'])
        order.order_date = datetime.utcnow()
        db.session.commit()
    return redirect(url_for('orders'))

@app.route('/employees')
def employees():
    all_employees = Employee.query.all()
    return render_template('employees.html', employees=all_employees)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        new_employee = Employee(name=name, position=position)
        db.session.add(new_employee)
        db.session.commit()
    return redirect(url_for('employees'))

@app.route('/delete_employee/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('employees'))

@app.route('/modify_employee/<int:id>', methods=['POST'])
def modify_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.position = request.form['position']
        db.session.commit()
    return redirect(url_for('employees'))

# Routes for Stock
@app.route('/stocks')
def stocks():
    all_stocks = Stock.query.all()
    return render_template('stocks.html', stocks=all_stocks)

@app.route('/add_stock', methods=['POST'])
def add_stock():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        new_stock = Stock(name=name, quantity=quantity)
        db.session.add(new_stock)
        db.session.commit()
    return redirect(url_for('stocks'))

@app.route('/delete_stock/<int:id>', methods=['POST'])
def delete_stock(id):
    stock = Stock.query.get_or_404(id)
    db.session.delete(stock)
    db.session.commit()
    return redirect(url_for('stocks'))

@app.route('/modify_stock/<int:id>', methods=['POST'])
def modify_stock(id):
    stock = Stock.query.get_or_404(id)
    if request.method == 'POST':
        stock.name = request.form['name']
        stock.quantity = int(request.form['quantity'])
        db.session.commit()
    return redirect(url_for('stocks'))

# Routes for Supplier
@app.route('/suppliers')
def suppliers():
    all_suppliers = Supplier.query.all()
    return render_template('suppliers.html', suppliers=all_suppliers)

@app.route('/add_supplier', methods=['POST'])
def add_supplier():
    if request.method == 'POST':
        name = request.form['name']
        product = request.form['product']
        new_supplier = Supplier(name=name, product=product)
        db.session.add(new_supplier)
        db.session.commit()
    return redirect(url_for('suppliers'))

@app.route('/delete_supplier/<int:id>', methods=['POST'])
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    return redirect(url_for('suppliers'))

@app.route('/modify_supplier/<int:id>', methods=['POST'])
def modify_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    if request.method == 'POST':
        supplier.name = request.form['name']
        supplier.product = request.form['product']
        db.session.commit()
    return redirect(url_for('suppliers'))

if __name__ == '__main__':
    app.run(debug=True)

