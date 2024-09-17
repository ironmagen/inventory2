import psycopg2
from psycopg2 import pool


class Deliveries:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def connect_to_database(self):
        # Connection pooling handles connection creation
        pass

    def create_delivery_table(self):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
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
            conn.commit()
        finally:
            self.db_pool.putconn(conn)

    def insert_delivery(self, delivery_date, vendor_name, item_name, quantity, unit_price):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO deliveries (delivery_date, vendor_name, item_name, quantity, unit_price)
                VALUES (%s, %s, %s, %s, %s);
            """, (delivery_date, vendor_name, item_name, quantity, unit_price))
            conn.commit()
        finally:
            self.db_pool.putconn(conn)

    def get_all_deliveries(self):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM deliveries;")
            rows = cur.fetchall()
            return rows
        finally:
            self.db_pool.putconn(conn)

    def get_delivery_by_id(self, delivery_id):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM deliveries WHERE delivery_id = %s;", (delivery_id,))
            row = cur.fetchone()
            return row
        finally:
            self.db_pool.putconn(conn)

    def update_delivery(self, delivery_id, delivery_date, vendor_name, item_name, quantity, unit_price):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE deliveries
                SET delivery_date = %s, vendor_name = %s, item_name = %s, quantity = %s, unit_price = %s
                WHERE delivery_id = %s;
            """, (delivery_date, vendor_name, item_name, quantity, unit_price, delivery_id))
            conn.commit()
        finally:
            self.db_pool.putconn(conn)

    def delete_delivery(self, delivery_id):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM deliveries WHERE delivery_id = %s;", (delivery_id,))
            conn.commit()
        finally:
            self.db_pool.putconn(conn)


# Create a database connection pool
db_host = 'localhost'
db_name = 'inventory'
db_user = 'your_database_user'
db_password = 'your_database_password'
db_port = 5432
min_conns = 1
max_conns = 10

db_pool = pool.ThreadedConnectionPool(
    min_conns, max_conns,
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password,
    port=db_port
)


# Initialize Deliveries class with database connection pool
deliveries = Deliveries(db_pool)


# When shutting down the application, close all database connections
import atexit
atexit.register(db_pool.closeall)
