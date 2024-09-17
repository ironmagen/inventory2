from inventory_items_table import InventoryItemsTable
from inventory_input import InventoryInput
from inventory_utilities import InventoryUtilities
from sales_items import SalesItems
from orders import Orders
from deliveries import Deliveries
from flask import Flask, render_template, request


inventory_items_table = InventoryItemsTable()
inventory_input = InventoryInput()
inventory_utilities = InventoryUtilities()
sales_items = SalesItems()
orders = Orders()
deliveries = Deliveries()

app = Flask(__name__)


@app.route('/inventory', methods=['GET'])
def get_inventory():
    inventory_data = inventory_items_table.get_inventory()
    return render_template('inventory.html', inventory=inventory_data)

@app.route('/add_item', methods=['POST'])
def add_item():
    item_data = request.form
    inventory_items_table.add_item(item_data)
    return redirect(url_for('get_inventory'))

@app.route('/input', methods=['GET'])
def get_input():
    input_data = inventory_input.get_input()
    return render_template('input.html', input=input_data)

@app.route('/submit_input', methods=['POST'])
def submit_input():
    input_data = request.form
    inventory_input.submit_input(input_data)
    return redirect(url_for('get_input'))

@app.route('/utilities', methods=['GET'])
def get_utilities():
    utilities_data = inventory_utilities.get_utilities()
    return render_template('utilities.html', utilities=utilities_data)

@app.route('/run_utility', methods=['POST'])
def run_utility():
    utility_data = request.form
    inventory_utilities.run_utility(utility_data)
    return redirect(url_for('get_utilities'))

@app.route('/sales', methods=['GET'])
def get_sales():
    sales_data = sales_items.get_sales()
    return render_template('sales.html', sales=sales_data)

@app.route('/add_sale', methods=['POST'])
def add_sale():
    sale_data = request.form
    sales_items.add_sale(sale_data)
    return redirect(url_for('get_sales'))

@app.route('/orders', methods=['GET'])
def get_orders():
    orders_data = orders.get_orders()
    return render_template('orders.html', orders=orders_data)

@app.route('/place_order', methods=['POST'])
def place_order():
    order_data = request.form
    orders.place_order(order_data)
    return redirect(url_for('get_orders'))

@app.route('/deliveries', methods=['GET'])
def get_deliveries():
    deliveries_data = deliveries.get_deliveries()
    return render_template('deliveries.html', deliveries=deliveries_data)

@app.route('/record_delivery', methods=['POST'])
def record_delivery():
    order_id = request.form['order_id']
    date = request.form['date']
    status = request.form['status']

    # Validate data
    if not order_id or not date or not status:
        return 'Error: Please fill out all fields.'

    # Store data in database
    deliveries.add_delivery(order_id, date, status)

    # Return success message
    return redirect(url_for('get_deliveries'))

if __name__ == '__main__':
    app.run(debug=True)
