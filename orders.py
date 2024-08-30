import psycopg2


def create_order(conn, cursor, vendor_filter=None, type_filter=None):
    """
    Filters items based on vendor or type, allows user input for quantity,
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

    # Get items from inventory table
    query = f"""
    SELECT item_id, item_name, vendor, quantity_on_hand, par, value_on_hand
    FROM items
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
        item_id INTEGER NOT NULL REFERENCES items(item_id),
        item_name VARCHAR(255) NOT NULL,
        order_quantity INTEGER NOT NULL
    );
    """)
    conn.commit()

    # Insert orders into orders table
    if orders:
        query = """
        INSERT INTO orders (vendor, item_id, item_name, order_quantity)
        VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(query, orders)
        conn.commit()
        print(f"Successfully created {len(orders)} orders.")


if __name__ == "__main__":
    # Connect to the inventory database (replace with your connection details)
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
