import psycopg2
from psycopg2 import pool


class SalesItems:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def create_sales_table(self):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    sale_id SERIAL PRIMARY KEY,
                    sale_date DATE NOT NULL,
                    item_name VARCHAR(255) NOT NULL,
                    quantity INTEGER NOT NULL,
                    price FLOAT NOT NULL
                );
            """)
            conn.commit()
        finally:
            self.db_pool.putconn(conn)

    def add_sale(self, sale_data):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO sales (sale_date, item_name, quantity, price)
                VALUES (%s, %s, %s, %s);
            """, (sale_data['sale_date'], sale_data['item_name'], sale_data['quantity'], sale_data['price']))
            conn.commit()
        finally:
            self.db_pool.putconn(conn)

    def get_sales(self):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM sales;")
            rows = cur.fetchall()
            return rows
        finally:
            self.db_pool.putconn(conn)

    def update_sale(self, sale_id, sale_date, item_name, quantity, price):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE sales
                SET sale_date = %s, item_name = %s, quantity = %s, price = %s
                WHERE sale_id = %s;
            """, (sale_date, item_name, quantity, price, sale_id))
            conn.commit()
        finally:
            self.db_pool.putconn(conn)

    def delete_sale(self, sale_id):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM sales WHERE sale_id = %s;", (sale_id,))
            conn.commit()
        finally:
            self.db_pool.putconn(conn)


# Use the existing database connection pool from app.py
from app import db_pool


# Initialize SalesItems class with database connection pool
sales_items = SalesItems(db_pool)
