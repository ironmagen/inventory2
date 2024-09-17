import psycopg2
from datetime import datetime


class Deliveries:
    """
    A class to manage deliveries.
    """

    def __init__(self, dbname="deliveries"):
        """
        Initializes the Deliveries class.

        Args:
            dbname (str, optional): The name of the database to connect to (defaults to "deliveries").
        """
        try:
            self.conn = psycopg2.connect(dbname=dbname)
        except psycopg2.OperationalError as e:
            print(f"Error connecting to database: {e}")
            self.conn = None

    def connect_to_database(self, dbname="deliveries"):
        """
        Connects to the deliveries database.

        Args:
            dbname (str, optional): The name of the database to connect to (defaults to "deliveries").
        """
        try:
            self.conn = psycopg2.connect(dbname=dbname)
        except psycopg2.OperationalError as e:
            print(f"Error connecting to database: {e}")

    def create_delivery_table(self):
        """
        Creates the deliveries table.
        """
        if self.conn is None:
            print("Database connection failed. Cannot create table.")
            return

        try:
            cur = self.conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS deliveries (
                    delivery_id SERIAL PRIMARY KEY,
                    delivery_date DATE NOT NULL,
                    vendor_name VARCHAR(255) NOT NULL,
                    item_name VARCHAR(255) NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price FLOAT NOT NULL
                );
            """)
            self.conn.commit()
            cur.close()
            print("Table 'deliveries' created successfully.")
        except psycopg2.OperationalError as e:
            print(f"Error creating table: {e}")

    def insert_delivery(self, delivery_date, vendor_name, item_name, quantity, unit_price):
        """
        Inserts a new delivery into the database.

        Args:
            delivery_date (date): The date of the delivery.
            vendor_name (str): The name of the vendor.
            item_name (str): The name of the item.
            quantity (int): The quantity of the item.
            unit_price (float): The unit price of the item.
        """
        if self.conn is None:
            print("Database connection failed. Cannot insert delivery.")
            return

        try:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO deliveries (delivery_date, vendor_name, item_name, quantity, unit_price)
                VALUES (%s, %s, %s, %s, %s);
            """, (delivery_date, vendor_name, item_name, quantity, unit_price))
            self.conn.commit()
            cur.close()
            print("Delivery inserted successfully.")
        except psycopg2.OperationalError as e:
            print(f"Error inserting delivery: {e}")

    def get_all_deliveries(self):
        """
        Retrieves all deliveries from the database.

        Returns:
            list: A list of tuples containing delivery information.
        """
        if self.conn is None:
            print("Database connection failed. Cannot retrieve deliveries.")
            return []

        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM deliveries;")
            rows = cur.fetchall()
            cur.close()
            return rows
        except psycopg2.OperationalError as e:
            print(f"Error retrieving deliveries: {e}")
            return []

    def get_delivery_by_id(self, delivery_id):
        """
        Retrieves a delivery by ID.

        Args:
            delivery_id (int): The ID of the delivery.

        Returns:
            tuple: A tuple containing delivery information.
        """
        if self.conn is None:
            print("Database connection failed. Cannot retrieve delivery.")
            return None

        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM deliveries WHERE delivery_id = %s;", (delivery_id,))
            row = cur.fetchone()
            cur.close()
            return row
        except psycopg2.OperationalError as e:
            print(f"Error retrieving delivery: {e}")
            return None

def update_delivery(self, delivery_id, delivery_date, vendor_name, item_name, quantity, unit_price):
    """
    Updates a delivery.

    Args:
        delivery_id (int): The ID of the delivery.
        delivery_date (date): The date of the delivery.
        vendor_name (str): The name of the vendor.
        item_name (str): The name of the item.
        quantity (int): The quantity of the item.
        unit_price (float): The unit price of the item.
    """
    if self.conn is None:
        print("Database connection failed. Cannot update delivery.")
        return

    try:
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE deliveries
            SET delivery_date = %s, vendor_name = %s, item_name = %s, quantity = %s, unit_price = %s
            WHERE delivery_id = %s;
        """, (delivery_date, vendor_name, item_name, quantity, unit_price, delivery_id))
        self.conn.commit()
        cur.close()
        print("Delivery updated successfully.")
    except psycopg2.OperationalError as e:
        print(f"Error updating delivery: {e}")
    def delete_delivery(self, delivery_id):
        """
        Deletes a delivery.

        Args:
            delivery_id (int): The ID of the delivery.
        """
        if self.conn is None:
            print("Database connection failed. Cannot delete delivery.")
            return

        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM deliveries WHERE delivery_id = %s;", (delivery_id,))
            self.conn.commit()
            cur.close()
            print("Delivery deleted successfully.")
        except psycopg2.OperationalError as e:
            print(f"Error deleting delivery: {e}")

    def get_total_deliveries_value(self):
        """
        Calculates the total value of all deliveries.

        Returns:
            float: The total value of all deliveries.
        """
        if self.conn is None:
            print("Database connection failed. Cannot calculate total deliveries value.")
            return 0

        try:
            cur = self.conn.cursor()
            cur.execute("SELECT SUM(quantity * unit_price) FROM deliveries;")
            total_value = cur.fetchone()[0]
            cur.close()
            return total_value
        except psycopg2.OperationalError as e:
            print(f"Error calculating total deliveries value: {e}")
            return 0

    def get_deliveries_by_vendor(self, vendor_name):
        """
        Retrieves deliveries by vendor.

        Args:
            vendor_name (str): The name of the vendor.

        Returns:
            list: A list of tuples containing delivery information.
        """
        if self.conn is None:
            print("Database connection failed. Cannot retrieve deliveries by vendor.")
            return []

        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM deliveries WHERE vendor_name = %s;", (vendor_name,))
            rows = cur.fetchall()
            cur.close()
            return rows
        except psycopg2.OperationalError as e:
            print(f"Error retrieving deliveries by vendor: {e}")
            return []

    def close_connection(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.close()


# Example usage in app.py:
# deliveries = Deliveries()
# deliveries.create_delivery_table()
# deliveries.insert_delivery(datetime.now(), "Example Vendor", "Example Item", 10, 100.0)
# deliveries_list = deliveries.get_all_deliveries()
# delivery = deliveries.get_delivery_by_id(1)
# deliveries.update_delivery(1, datetime.now(), "Example Vendor", "Example Item", 20, 100.0)
# deliveries.delete_delivery(1)
# total_value = deliveries.get_total_deliveries_value()
# vendor_deliveries = deliveries.get_deliveries_by_vendor("Example Vendor")
# deliveries.close_connection()
