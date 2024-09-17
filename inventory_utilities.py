import psycopg2


class InventoryUtilities:
    """
    A class to manage inventory utilities.
    """

    def __init__(self, dbname="inventory"):
        """
        Initializes the InventoryUtilities class.

        Args:
            dbname (str, optional): The name of the database to connect to (defaults to "inventory").
        """
        try:
            self.conn = psycopg2.connect(dbname=dbname)
        except psycopg2.OperationalError as e:
            print(f"Error connecting to database: {e}")
            self.conn = None

    def connect_to_database(self, dbname="inventory"):
        """
        Connects to the inventory database.

        Args:
            dbname (str, optional): The name of the database to connect to (defaults to "inventory").
        """
        try:
            self.conn = psycopg2.connect(dbname=dbname)
        except psycopg2.OperationalError as e:
            print(f"Error connecting to database: {e}")

    def insert_item(self, item_name, vendor, quantity, value, last_ordered):
        """
        Inserts a new item into the database.

        Args:
            item_name (str): The name of the item.
            vendor (str): The vendor of the item.
            quantity (int): The quantity of the item.
            value (float): The value of the item.
            last_ordered (date): The date the item was last ordered.
        """
        if self.conn is None:
            print("Database connection failed. Cannot insert item.")
            return

        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO items (item_name, vendor, quantity_on_hand, value_on_hand, last_ordered) VALUES (%s, %s, %s, %s, %s)",
                        (item_name, vendor, quantity, value, last_ordered))
            self.conn.commit()
            cur.close()
            print("Item inserted successfully.")
        except psycopg2.OperationalError as e:
            print(f"Error inserting item: {e}")

    def get_all_items(self):
        """
        Retrieves all items from the database.

        Returns:
            list: A list of tuples containing item information.
        """
        if self.conn is None:
            print("Database connection failed. Cannot retrieve items.")
            return []

        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM items")
            rows = cur.fetchall()
            cur.close()
            return rows
        except psycopg2.OperationalError as e:
            print(f"Error retrieving items: {e}")
            return []

    def update_item(self, item_id, quantity, value):
        """
        Updates the quantity and value of an item.

        Args:
            item_id (int): The ID of the item.
            quantity (int): The new quantity of the item.
            value (float): The new value of the item.
        """
        if self.conn is None:
            print("Database connection failed. Cannot update item.")
            return

        try:
            cur = self.conn.cursor()
            cur.execute("UPDATE items SET quantity_on_hand = %s, value_on_hand = %s WHERE item_id = %s",
                        (quantity, value, item_id))
            self.conn.commit()
            cur.close()
            print("Item updated successfully.")
        except psycopg2.OperationalError as e:
            print(f"Error updating item: {e}")

    def delete_item(self, item_id):
        """
        Deletes an item from the database.

        Args:
            item_id (int): The ID of the item.
        """
        if self.conn is None:
            print("Database connection failed. Cannot delete item.")
            return

        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM items WHERE item_id = %s", (item_id,))
            self.conn.commit()
            cur.close()
            print("Item deleted successfully.")
        except psycopg2.OperationalError as e:
            print(f"Error deleting item: {e}")

    def get_item_details(self, item_id, sales_data):
        """
        Retrieves detailed information about a specific item.

        Args:
            item_id (int): The ID of the item.
            sales_data (dict): A dictionary containing sales data.

        Returns:
            list: A list of tuples containing item details.
        """
        if self.conn is None:
            print("Database connection failed. Cannot retrieve item details.")
            return []

        try:
            cur = self.conn.cursor()
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
        except psycopg2.OperationalError as e:
            print(f"Error retrieving item details: {e}")
            return []

    def calculate_total_inventory_value(self):
        """
        Calculates the total value of all inventory items on hand.

        Returns:
            float: The total value of all inventory items.
        """
        if self.conn is None:
            print("Database connection failed. Cannot calculate total inventory value.")
            return 0

        try:
            cur = self.conn.cursor()
            cur.execute("SELECT SUM(quantity_on_hand * value_on_hand) FROM items")
            total_value = cur.fetchone()[0]
            cur.close()
            return total_value
        except psycopg2.OperationalError as e:
            print(f"Error calculating total inventory value: {e}")
            return 0

    def calculate_discrepancy(self, item_id, hard_count):
        """
        Calculates the discrepancy between recorded quantity and hard count.

        Args:
            item_id (int): The ID of the item.
            hard_count (int): The hard count of the item.

        Returns:
            int: The discrepancy between recorded quantity and hard count.
        """
        if self.conn is None:
            print("Database connection failed. Cannot calculate discrepancy.")
            return 0

        try:
            cur = self.conn.cursor()
            cur.execute("SELECT quantity_on_hand FROM items WHERE item_id = %s", (item_id,))
            recorded_quantity = cur.fetchone()[0]
            cur.close()
            discrepancy = recorded_quantity - hard_count
            return discrepancy
        except psycopg2.OperationalError as e:
            print(f"Error calculating discrepancy: {e}")
            return 0

    def update_item_hard_count(self, item_id, hard_count):
        """
        Updates the hard count for a specific item.

        Args:
            item_id (int): The ID of the item.
            hard_count (int): The new hard count of the item.
        """
        if self.conn is None:
            print("Database connection failed. Cannot update item hard count.")
            return

        try:
            cur = self.conn.cursor()
            cur.execute("UPDATE items SET hard_count = %s WHERE item_id = %s", (hard_count, item_id))
            self.conn.commit()
            cur.close()
            print("Item hard count updated successfully.")
        except psycopg2.OperationalError as e:
            print(f"Error updating item hard count: {e}")

    def close_connection(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.close()


# Example usage in app.py:
# inventory = InventoryUtilities()
# inventory.insert_item("Example Item", "Example Vendor", 10, 100.0, "2022-01-01")
# items = inventory.get_all_items()
# item_details = inventory.get_item_details(1, {"sales_category1": 100, "sales_category2": 200, "sales_category3": 300})
# total
