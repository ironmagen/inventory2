import psycopg2
from datetime import datetime

def create_order(conn, cursor, vendor_filter=None, type_filter=None):
    """
    Filters items based on vendor or type, allows user input for quantity and expected delivery date,
    and creates orders for items with the same vendor based on their par levels.

    Args:
        conn (psycopg2.connect): Connection to the inventory database.
        cursor (psycopg2.cursor): Database cursor for executing queries.
        vendor_filter (str, optional): Vendor name to filter by. Defaults to None.
        type_filter (str, optional): Item type to filter by. Defaults to None.
    """

    # Filter query based on user input
    filter_clause = ""
    if vendor_filter:
        filter_clause = f" WHERE vendor = '{vendor_filter}'"
    elif type_filter:
        filter_clause = f" WHERE type = '{type_filter}'"

    # Get items from inventory_items table
    query = f"""
    SELECT item_id, item_name, vendor, quantity_on_hand, par, value_on_hand
    FROM inventory_items
    {filter_clause}
    """
    cursor.execute(query)
    items = cursor.fetchall()

    if not items:
        print("No items found based on your filters.")
        return

    orders = []
    for item_id, item_name, vendor, quantity_on_hand, par, value_on_hand in items:
        # Calculate order quantity based on par level
        order_quantity = max(0, par - quantity_on_hand)  # Ensure non-negative quantity

        # Get user confirmation if order quantity is greater than 0
        if order_quantity > 0:
            confirm = input(f"Order {order_quantity} units of '{item_name}' (ID: {item_id})? (y/n): ")
            if confirm.lower() == 'y':
                orders.append((vendor, item_id, item_name, order_quantity))

    # Create orders table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id SERIAL PRIMARY KEY,
        vendor VARCHAR(255) NOT NULL,
        item_id INTEGER NOT NULL REFERENCES inventory_items(item_id),
        item_name VARCHAR(255) NOT NULL,
        order_quantity INTEGER NOT NULL,
        expected_delivery_date DATE NOT NULL,
        status VARCHAR(10) NOT NULL DEFAULT 'open'
    );
    """)
    conn.commit()

    # Get expected delivery date from the user
    expected_delivery_date = input("Enter expected delivery date (YYYY-MM-DD): ")
    try:
        expected_delivery_date = datetime.strptime(expected_delivery_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please enter in YYYY-MM-DD format.")
        return

    # Insert orders into orders table with status
    if orders:
        query = """
        INSERT INTO orders (vendor, item_id, item_name, order_quantity, expected_delivery_date, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(query, [(vendor, item_id, item_name, order_quantity, expected_delivery_date, 'open') for vendor, item_id, item_name, order_quantity in orders])
        conn.commit()
        print(f"Successfully created {len(orders)} orders.")

def search_order(conn, cursor, vendor_filter=None, order_id=None):
    """
    Searches for orders based on vendor or order ID.

    Args:
        conn (psycopg2.connect): Connection to the inventory database.
        cursor (psycopg2.cursor): Database cursor for executing queries.
        vendor_filter (str, optional): Vendor name to filter by. Defaults to None.
        order_id (int, optional): Order ID to filter by. Defaults to None.
    """

    # Filter query based on user input
    filter_clause = ""
    if vendor_filter:
        filter_clause = f" WHERE vendor = '{vendor_filter}'"
    elif order_id:
        filter_clause = f" WHERE order_id = {order_id}"

    # Get orders from the orders table
    query = f"""
    SELECT * FROM orders {filter_clause}
    """
    cursor.execute(query)
    orders = cursor.fetchall()

    if not orders:
        print("No orders found based on your filters.")
        return

    for order in orders:
        print(f"Order ID: {order[0]}, Vendor: {order[1]}, Item ID: {order[2]}, Item Name: {order[3]}, Order Quantity: {order[4]}, Expected Delivery Date: {order[5]}, Status: {order[6]}")

if __name__ == "__main__":
    # Connect to the inventory database
    conn = psycopg2.connect(dbname="inventory")
    cursor = conn.cursor()

    # Prompt user for filter options
    filter_by = input("Filter by vendor (v) or type (t): ")
    if filter_by.lower() == 'v':
        vendor_filter = input("Enter vendor name: ")
        create_order(conn, cursor, vendor_filter=vendor_filter)
    elif filter_by.lower() == 't':
        type_filter = input("Enter item type: ")
        create_order(conn, cursor, type_filter=type_filter)
    else:
        print("Invalid filter option.")

    # Close database connection
    conn.close()
