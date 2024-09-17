import psycopg2

class InventoryItemsTable:
    def __init__(self):
        self.conn = psycopg2.connect(dbname="inventory")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS inventory_items (
                item_id SERIAL PRIMARY KEY,
                item_name VARCHAR(255) NOT NULL,
                vendor VARCHAR(255),
                type VARCHAR(255),
                quantity_on_hand INTEGER NOT NULL,
                par INTEGER NOT NULL,
                value_on_hand FLOAT NOT NULL,
                last_ordered DATE
            );
        """)
        self.conn.commit()

    def insert_item(self, item_name, vendor, type, quantity_on_hand, par, value_on_hand, last_ordered):
        self.cur.execute("""
            INSERT INTO inventory_items (item_name, vendor, type, quantity_on_hand, par, value_on_hand, last_ordered)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (item_name, vendor, type, quantity_on_hand, par, value_on_hand, last_ordered))
        self.conn.commit()

    def get_all_items(self):
        self.cur.execute("SELECT * FROM inventory_items;")
        return self.cur.fetchall()

    def get_item_by_id(self, item_id):
        self.cur.execute("SELECT * FROM inventory_items WHERE item_id = %s;", (item_id,))
        return self.cur.fetchone()

    def update_item(self, item_id, item_name, vendor, type, quantity_on_hand, par, value_on_hand, last_ordered):
        self.cur.execute("""
            UPDATE inventory_items
            SET item_name = %s, vendor = %s, type = %s, quantity_on_hand = %s, par = %s, value_on_hand = %s, last_ordered = %s
            WHERE item_id = %s;
        """, (item_name, vendor, type, quantity_on_hand, par, value_on_hand, last_ordered, item_id))
        self.conn.commit()

    def delete_item(self, item_id):
        self.cur.execute("DELETE FROM inventory_items WHERE item_id = %s;", (item_id,))
        self.conn.commit()

    def close_connection(self):
        self.cur.close()
        self.conn.close()

