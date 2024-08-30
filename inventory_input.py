import inventory_utils

def get_inventory_items(conn, vendor=None):
    """Retrieves inventory items from the inventory_items_table, optionally filtered by vendor."""
    if vendor:
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory_items_table WHERE vendor = %s", (vendor,))
        items = cur.fetchall()
        cur.close()
    else:
        items = inventory_utils.get_all_items(conn)
    return items

def get_user_input(item):
    """Prompts user to input quantity on hand for a given item."""
    quantity = input(f"Enter quantity on hand for {item[1]}: ")
    return quantity

def update_inventory_with_user_input(conn, items):
    """Updates inventory quantities based on user input."""
    for item in items:
        quantity = get_user_input(item)
        inventory_utils.update_item(conn, item[0], quantity, item[4])

def main():
    conn = inventory_utils.connect_to_database()

    vendor = input("Enter vendor (leave blank for all): ")
    items = get_inventory_items(conn, vendor)

    if not items:
        print("No items found for the specified vendor.")
    else:
        update_inventory_with_user_input(conn, items)

    conn.close()

if __name__ == "__main__":
    main()
