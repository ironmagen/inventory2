import psycopg2


class InventoryItems:
    """
    A class to manage the inventory_items table in the database.
    """

    def __init__(self, dbname, user, password, host="localhost", port=5432):
        """
        Initializes the InventoryItems class.

        Args:
            dbname (str): The name of the database to connect to.
            user (str): The username for database access.
            password (str): The password for database access.
            host (str, optional): The hostname or IP address of the database server (defaults to "localhost").
            port (int, optional): The port number of the database server (defaults to 5432).
        """
        try:
            self.conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
            self.cur = self.conn.cursor()
        except psycopg2.OperationalError as e:
            print(f"Error connecting to database: {e}")
            self.conn = None
            self.cur = None

    def create_table(self):
        """
        Creates the inventory_items table.
        """
        if self.conn is None:
            print("Database connection failed. Cannot create table.")
            return

        try:
            create_table_stmt = """
                CREATE TABLE IF NOT EXISTS inventory_items (
                    item_name VARCHAR(255) PRIMARY KEY,
                    item_description TEXT,
                    quantity INTEGER NOT NULL,
                    unit_price FLOAT NOT NULL
                );
            """

            self.cur.execute(create_table_stmt)
            self.conn.commit()
            print("Table 'inventory_items' created successfully.")
        except psycopg2.OperationalError as e:
            print(f"Error creating table: {e}")

    def insert_item(self, item_name, item_description, quantity, unit_price):
        """
        Inserts a new item into the inventory_items table.

        Args:
            item_name (str): The name of the item.
            item_description (str): The description of the item.
            quantity (int): The quantity of the item.
            unit_price (float): The unit price of the item.
        """
        if self.conn is None:
            print("Database connection failed. Cannot insert item.")
            return

        try:
            insert_stmt = """
                INSERT INTO inventory_items (
                    item_name, item_description, quantity, unit_price
                ) VALUES (
                    %s, %s, %s, %s
                );
            """

            self.cur.execute(insert_stmt, (
                item_name, item_description, quantity, unit_price
            ))
            self.conn.commit()
            print("Item inserted successfully.")
        except psycopg2.OperationalError as e:
            print(f"Error inserting item: {e}")

    def update_item(self, item_name, item_description=None, quantity=None, unit_price=None):
        """
        Updates an existing item in the inventory_items table.

        Args:
            item_name (str): The name of the item.
            item_description (str, optional): The new description of the item.
            quantity (int, optional): The new quantity of the item.
            unit_price (float, optional): The new unit price of the item.
        """
        if self.conn is None:
            print("Database connection failed. Cannot update item.")
            return

        try:
            update_stmt = """
                UPDATE inventory_items
                SET {}
                WHERE item_name = %s;
            """.format(
                ', '.join([
                    f"item_description = '{item_description}'" if item_description else '',
                    f"quantity = {quantity}" if quantity else '',
                    f"unit_price = {unit_price}" if unit_price else ''
                ])
            )

            self.cur.execute(update_stmt, (item_name,))
            self.conn.commit()
            print("Item updated successfully.")
        except psycopg2.OperationalError as e:
            print(f"Error updating item: {e}")

    def delete_item(self, item_name):
        """
        Deletes an item from the inventory_items table.

        Args:
            item_name (str): The name of the item.
        """
        if self.conn is None:
            print("Database connection failed. Cannot delete item.")
            return

        try:
            delete_stmt = """
                DELETE FROM inventory_items
                WHERE item_name = %s;
            """

            self.cur.execute(delete_stmt, (item_name,))
            self.conn.commit()
            print("Item deleted successfully.")
        except psycopg2.OperationalError as e:
            print(f"Error deleting item: {e}")

    def close_connection(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.close()


# Example usage in app.py:
# inventory = InventoryItems(
#     dbname="your_database_name",
#     user="your_database_user",
#     password="your_database_password",
#     host="localhost",
#     port=5432
#
