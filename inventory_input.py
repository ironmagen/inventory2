import psycopg2
from psycopg2 import pool


class InventoryUtilities:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def get_utilities(self):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM utilities;")
            rows = cur.fetchall()
            return rows
        finally:
            self.db_pool.putconn(conn)

    def run_utility(self, utility_data):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO utilities (utility_name, parameters)
                VALUES (%s, %s);
            """, (utility_data['utility_name'], utility_data['parameters']))
            conn.commit()
        finally:
            self.db_pool.putconn(conn)

    def update_utility(self, utility_id, utility_name, parameters):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE utilities
                SET utility_name = %s, parameters = %s
                WHERE utility_id = %s;
            """, (utility_name, parameters, utility_id))
            conn.commit()
        finally:
            self.db_pool.putconn(conn)

    def delete_utility(self, utility_id):
        conn = self.db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM utilities WHERE utility_id = %s;", (utility_id,))
            conn.commit()
        finally:
            self.db_pool.putconn(conn)


# Use the existing database connection pool from app.py
from app import db_pool


# Initialize InventoryUtilities class with database connection pool
inventory_utilities = InventoryUtilities(db_pool)
