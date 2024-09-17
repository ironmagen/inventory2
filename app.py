import psycopg2
import atexit
from psycopg2 import pool
from inventory_items_table import InventoryItems
from inventory_input import InventoryInput
from inventory_utilities import InventoryUtilities
from sales_items_table import SalesItems
from orders import Orders
from deliveries import Deliveries
from flask import Flask, render_template, request, jsonify, redirect, url_for


app = Flask(__name__)

# Database connection pooling configuration
DB_HOST = 'localhost'
DB_NAME = 'inventory'
DB_USER = 'your_database_user'
DB_PASSWORD = 'your_database_password'
DB_PORT = 5432
MIN_CONNS = 1
MAX_CONNS = 10

# Create a database connection pool
db_pool = pool.ThreadedConnectionPool(
    MIN_CONNS, MAX_CONNS,
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
)


# Initialize classes with database connection pool
inventory_items_table = InventoryItems(db_pool)
inventory_input = InventoryInput(db_pool)
inventory_utilities = InventoryUtilities(db_pool)
sales_items = SalesItems(db_pool)
orders = Orders(db_pool)
deliveries = Deliveries(db_pool)


# Inventory Routes
@app.route('/inventory', methods=['GET'])
def get_inventory():
    try:
        inventory_data = inventory_items_table.get_inventory()
        return render_template('inventory.html', inventory=inventory_data)
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/add_item', methods=['POST'])
def add_item():
    try:
        item_data = request.form
        required_fields = ['item_name', 'vendor', 'quantity', 'value']
        
        # Validate data
        for field in required_fields:
            if not item_data.get(field):
                return f"Error: Please fill out all fields. ({field} is missing)"
        
        inventory_items_table.add_item(item_data)
        return redirect(url_for('get_inventory'))
    except Exception as e:
        return f"Error: {str(e)}"


# Input Routes
@app.route('/input', methods=['GET'])
def get_input():
    try:
        input_data = inventory_input.get_input()
        return render_template('input.html', input=input_data)
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/submit_input', methods=['POST'])
def submit_input():
    try:
        input_data = request.form
        required_fields = ['input_type', 'quantity', 'date']
        
        # Validate data
        for field in required_fields:
            if not input_data.get(field):
                return f"Error: Please fill out all fields. ({field} is missing)"
        
        inventory_input.submit_input(input_data)
        return redirect(url_for('get_input'))
    except Exception as e:
        return f"Error: {str(e)}"


# Utilities Routes
@app.route('/utilities', methods=['GET'])
def get_utilities():
    try:
        utilities_data = inventory_utilities.get_utilities()
        return render_template('utilities.html', utilities=utilities_data)
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/run_utility', methods=['POST'])
def run_utility():
    try:
        utility_data = request.form
        required_fields = ['utility_name', 'parameters']
        
        # Validate data
        for field in required_fields:
            if not utility_data.get(field):
                return f"Error: Please fill out all fields. ({field} is missing)"
        
        inventory_utilities.run_utility(utility_data)
        return redirect(url_for('get_utilities'))
    except Exception as e:
        return f"Error: {str(e)}"


# Sales Routes
@app.route('/sales', methods=['GET'])
def get_sales():
    try:
        sales_data = sales_items.get_sales()
        return render_template('sales.html', sales=sales_data)
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/add_sale', methods=['POST'])
def add_sale():
    try:
        sale_data = request.form
        required_fields = ['sale_date', 'item_name', 'quantity', 'price']
        
        # Validate data
        for field in required_fields:
            if not sale_data.get(field):
                return f"Error: Please fill out all fields. ({field} is missing)"
        
        sales_items.add_sale(sale_data)
        return redirect(url_for('get_sales'))
    except Exception as e:
        return f"Error: {str(e)}"


# Orders Routes
@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        orders_data = orders.get_orders()
        return render_template('orders.html', orders=orders_data)
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        order_data = request.form
        required_fields = ['order_date', 'customer_name', 'item_name', 'quantity']
        
        # Validate data
        for field in required_fields:
            if not order_data.get(field):
                return f"Error: Please fill out all fields. ({field} is missing)"
        
        orders.place_order(order_data)
        return redirect(url_for('get_orders'))
    except Exception as e:
        return f"Error: {str(e)}"


# Deliveries Routes
@app.route('/deliveries', methods=['GET'])
def get_deliveries():
    try:
        deliveries_data = deliveries.get_deliveries()
        return render_template('deliveries.html', deliveries=deliveries_data)
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/record_delivery', methods=['POST'])
def record_delivery():
    try:
        delivery_data = request.form
        required_fields = ['order_id', 'date', 'status']
        
        # Validate data
        for field in required_fields:
            if not delivery_data.get(field):
                return f"Error: Please fill out all fields. ({field} is missing)"
        
        deliveries.add_delivery(delivery_data['order_id'], delivery_data['date'], delivery_data['status'])
        return redirect(url_for('get_deliveries'))
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)

# When shutting down the application, close all database connections
atexit.register(db_pool.closeall)
