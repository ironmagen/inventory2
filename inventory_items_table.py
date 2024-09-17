import psycopg2
from psycopg2 import pool


class InventoryItems:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def connect_to_database(self):
        # Connection pooling handles connection creation
        pass

    def create_inventory_table(self):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    item_id SERIAL PRIMARY KEY,
                    item_name VARCHAR(255) NOT NULL,
                    vendor_name VARCHAR(255) NOT NULL,
                    quantity INTEGER NOT NULL,
                    value FLOAT NOT NULL
                );
            """)
            conn.commit()
        finally:
            self.db_pool.putconn(conn)

    def add_item(self, item_data):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO inventory (item_name, vendor_name, quantity, value)
                VALUES (%s, %s, %s, %s);
            """, (item_data['item_name'], item_data['vendor_name'], item_data['quantity'], item_data['value']))
            conn.commit()
        finally:
            self.db_pool.putconn(conn)

    def get_inventory(self):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM inventory;")
            rows = cur.fetchall()
            return rows
        finally:
            self.db_pool.putconn(conn)

    def update_item(self, item_id, item_name, vendor_name, quantity, value):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE inventory
                SET item_name = %s, vendor_name = %s, quantity = %s, value = %s
                WHERE item_id = %s;
            """, (item_name, vendor_name, quantity, value, item_id))
            conn.commit()
        finally:
            self.db_pool.putconn(conn)

    def delete_item(self, item_id):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM inventory WHERE item_id = %s;", (item_id,))
            conn.commit()
        finally:
            self.db_pool.putconn(conn)


# Use the existing database connection pool from app.py
from app import db_pool


# Initialize InventoryItems class with database connection pool
inventory_items = InventoryItems(db_pool)
