import psycopg2
from psycopg2 import pool

class DatabaseConnectionPool:
    def __init__(self):
        self.pool = pool.ThreadedConnectionPool(
            1, 10,
            host="localhost",
            database="your_database",
            user="your_username",
            password="your_password"
        )

    def getconn(self):
        return self.pool.getconn()

    def putconn(self, conn):
        self.pool.putconn(conn)
