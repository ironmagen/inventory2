import psycopg2
from datetime import datetime

def show_open_orders(conn, cursor, filter_date=None, vendor_filter=None):
    """
    Shows all open orders with optional filtering by date and vendor.

    Args:
        conn (psycopg2.connect): Connection to the inventory database.
        cursor (psycopg2.cursor): Database cursor for executing queries.
        filter_date (str, optional): Date to filter by (YYYY-MM-DD). Defaults to None.
        vendor_filter (str, optional): Vendor name to filter by. Defaults to None.
    """

    # Filter query based on user input
    filter_clause = " WHERE status = 'open'"
    if filter_date:
        try:
            filter_date = datetime.strptime(filter_date, "%Y-%m-%d")
            filter_clause += f" AND expected_delivery_date = '{filter_date.date()}'"
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")
            return
    if vendor_filter:
        filter_clause += f" AND vendor = '{vendor_filter}'"

    # Get open orders from the orders table
    query = f"""
    SELECT * FROM orders {filter_clause}
    """
    cursor.execute(query)
    orders = cursor.fetchall()

    if not orders:
        print("No open orders found based on your filters.")
        return

    print("Open Orders:")
    for order in orders:
        print(f"Order ID: {order[0]}, Vendor: {order[1]}, Expected Delivery Date: {order[5]}")

def view_order_details(conn, cursor, order_id):
    """
    Views details of a specific order by order ID.

    Args:
        conn (psycopg2.connect): Connection to the inventory database.
        cursor (psycopg2.cursor): Database cursor for executing queries.
        order_id (int): Order ID to view details for.
    """

    query = f"""
    SELECT o.item_id, i.item_name, oi.quantity_unit_expected, i.quantity_unit, i.unit_price, (oi.quantity_unit_expected * i.unit_price) AS total_item_price
    FROM orders o
    INNER JOIN inventory_items i ON o.item_id = i.item_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_id = {order_id}
    """
    cursor.execute(query)
    order_details = cursor.fetchall()

    if not order_details:
        print(f"Order ID {order_id} not found.")
        return

    print("\nOrder Details:")
    print("Item ID\tItem Name\tQuantity Expected\tQuantity Unit\tUnit Price\tTotal Item Price")
    for item in order_details:
        print(f"{item[0]}\t{item[1]}\t{item[2]}\t{item[3]}\t${item[4]:.2f}\t${item[5]:.2f}")

def process_delivery(conn, cursor, order_id):
    """
    Processes a delivery for a specific order, allowing verification/override
    of quantities and prices, and saving to the deliveries table.

    Args:
        conn (psycopg2.connect): Connection to the inventory database.
        cursor (psycopg2.cursor): Database cursor for executing queries.
        order_id (int): Order ID to process delivery for.
    """

    view_order_details(conn, cursor, order_id)

    # Get user confirmation to proceed
    proceed = input("Do you want to proceed with processing this delivery? (y/n): ")
    if proceed.lower() != 'y':
        return

    # Get user input for quantity and price delivered (optional)
    quantity_delivered_list = []
    price_delivered_list = []
    for item in order_details:
        quantity_expected = item[2]
        quantity_delivered = input(f"Enter quantity delivered for '{item[1]}' (expected: {quantity_expected}): ")
        if quantity_delivered:
            try:
                quantity_delivered = int(quantity_delivered)
                if quantity_delivered < quantity_expected - 5 or quantity_delivered > quantity_expected + 5:
                    print("Quantity delivered is significantly different from expected. Please review.")
            except ValueError:
                print("Invalid quantity. Please enter an integer.")
                return

        price_delivered = input(f"Enter price delivered for '{item[1]}' (expected: ${item[4]:.2f}): ")
        if price_delivered:
            try:
                price_delivered = float(price_delivered)
                if price_delivered < item[4] - 0.5 or price_delivered > item[4] + 0.5:
                    print("Price delivered is significantly different from expected. Please review.")
            except ValueError:
                print("Invalid price. Please enter a decimal number.")
                return

        quantity_delivered_list.append((order_id, quantity_delivered))
        price_delivered_list.append((order_id, item[0], price_delivered))


      # Create deliveries table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deliveries (
        delivery_id SERIAL PRIMARY KEY,
        order_id INTEGER NOT NULL REFERENCES orders(order_id),
        item_id INTEGER NOT NULL,
        quantity_delivered INTEGER NOT NULL,
        total_item_price FLOAT NOT NULL
    );
    """)
    conn.commit()

    # Insert delivery data into the deliveries table
    for i, item in enumerate(order_details):
        # Calculate total item price based on verified quantity and price
        total_item_price = quantity_delivered_list[i][1] * price_delivered_list[i][2]

        # Insert delivery data
        cursor.execute("""
            INSERT INTO deliveries (order_id, item_id, quantity_delivered, total_item_price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, item[0], quantity_delivered_list[i][1], total_item_price))
    conn.commit()

    # Update order status to "closed"
    cursor.execute("""
    UPDATE orders SET status = 'closed' WHERE order_id = %s
    """, (order_id,))
    conn.commit()
