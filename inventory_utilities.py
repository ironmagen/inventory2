import psycopg2

def connect_to_database():
    """Connects to the inventory database."""
    conn = psycopg2.connect(dbname="inventory")
    return conn

def insert_item(conn, item_name, vendor, quantity, value, last_ordered):
    """Inserts a new item into the database."""
    cur = conn.cursor()
    cur.execute("INSERT INTO items (item_name, vendor, quantity_on_hand, value_on_hand, last_ordered) VALUES (%s, %s, %s, %s, %s)",
                (item_name, vendor, quantity, value, last_ordered))
    conn.commit()
    cur.close()

def get_all_items(conn):
    """Retrieves all items from the database."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM items")
    rows = cur.fetchall()
    cur.close()
    return rows

def update_item(conn, item_id, quantity, value):
    """Updates the quantity and value of an item."""
    cur = conn.cursor()
    cur.execute("UPDATE items SET quantity_on_hand = %s, value_on_hand = %s WHERE item_id = %s",
                (quantity, value, item_id))
    conn.commit()
    cur.close()

def delete_item(conn, item_id):
    """Deletes an item from the database."""
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE item_id = %s", (item_id,))
    conn.commit()
    cur.close()

def get_item_details(conn, item_id, sales_data):
    """Retrieves detailed information about a specific item, including dynamic sales category percentages."""
    cur = conn.cursor()
    cur.execute("""
    SELECT
        items.item_id,
        items.item_name,
        sales_categories1.name AS sales_category1,
        sales_categories2.name AS sales_category2,
        sales_categories3.name AS sales_category3,
        price_history.price,
        price_history.effective_date,
        order_history.order_date,
        order_history.quantity,
        items.quantity_on_hand,
        items.value_on_hand,
        sales_items.item_id AS sales_item_id,
        sales_items.quantity
    FROM
        items
    LEFT JOIN sales_categories1 ON items.sales_category1_id = sales_categories1.id
    LEFT JOIN sales_categories2 ON items.sales_category2_id = sales_categories2.id
    LEFT JOIN sales_categories3 ON items.sales_category3_id = sales_categories3.id
    LEFT JOIN price_history ON items.item_id = price_history.item_id
    LEFT JOIN order_history ON items.item_id = order_history.item_id
    LEFT JOIN sales_items ON items.item_id = sales_items.item_id
    WHERE
        items.item_id = %s
    """, (item_id,))

    # Calculate sales category percentages based on sales data
    total_sales = sum(sales_data.values())
    sales_category1_percentage = (sales_data.get('sales_category1', 0) / total_sales) * 100
    sales_category2_percentage = (sales_data.get('sales_category2', 0) / total_sales) * 100
    sales_category3_percentage = (sales_data.get('sales_category3', 0) / total_sales) * 100

    # Add calculated percentages to the query result
    rows = cur.fetchall()
    for row in rows:
        row = list(row)
        row.append(sales_category1_percentage)
        row.append(sales_category2_percentage)
        row.append(sales_category3_percentage)
        rows[rows.index(row)] = tuple(row)

    cur.close()
    return rows

def calculate_total_inventory_value(conn):
    """Calculates the total value of all inventory items on hand."""
    cur = conn.cursor()
    cur.execute("SELECT SUM(quantity_on_hand * value_on_hand) FROM items")
    total_value = cur.fetchone()[0]
    cur.close()
    return total_value

def calculate_discrepancy(conn, item_id, hard_count):
    """Calculates the discrepancy between recorded quantity and hard count."""
    cur = conn.cursor()
    cur.execute("SELECT quantity_on_hand FROM items WHERE item_id = %s", (item_id,))
    recorded_quantity = cur.fetchone()[0]
    cur.close()
    discrepancy = recorded_quantity - hard_count
    return discrepancy

def update_item_hard_count(conn, item_id, hard_count):
    """Updates the hard count for a specific item."""
    cur = conn.cursor()
    cur.execute("UPDATE items SET hard_count = %s WHERE item_id = %s", (hard_count, item_id))
    conn.commit()
    cur.close()
