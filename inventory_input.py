import inventory_utils


class InventoryInput:
    def __init__(self, conn):
        """
        Initializes the InventoryInput class.

        Args:
            conn (psycopg2.connect): Connection to the inventory database.
        """
        self.conn = conn

    def get_inventory_items(self, vendor=None):
        """
        Retrieves inventory items from the inventory_items_table, optionally filtered by vendor.

        Args:
            vendor (str, optional): Vendor name to filter by. Defaults to None.

        Returns:
            list: Inventory items.
        """
        if vendor:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM inventory_items_table WHERE vendor = %s", (vendor,))
            items = cur.fetchall()
            cur.close()
        else:
            items = inventory_utils.get_all_items(self.conn)
        return items

    def get_user_input(self, item):
        """
        Prompts user to input quantity on hand for a given item.

        Args:
            item (tuple): Inventory item.

        Returns:
            str: User-input quantity.
        """
        quantity = input(f"Enter quantity on hand for {item[1]}: ")
        return quantity

    def update_inventory_with_user_input(self, items):
        """
        Updates inventory quantities based on user input.

        Args:
            items (list): Inventory items.
        """
        for item in items:
            quantity = self.get_user_input(item)
            inventory_utils.update_item(self.conn, item[0], quantity, item[4])

    def run_input_process(self, vendor=None):
        """
        Runs the inventory input process.

        Args:
            vendor (str, optional): Vendor name to filter by. Defaults to None.
        """
        items = self.get_inventory_items(vendor)
        if not items:
            print("No items found for the specified vendor.")
        else:
            self.update_inventory_with_user_input(items)


# Example usage:
if __name__ == "__main__":
    conn = inventory_utils.connect_to_database()
    vendor = input("Enter vendor (leave blank for all): ")
    input_process = InventoryInput(conn)
    input_process.run_input_process(vendor)
    conn.close()
