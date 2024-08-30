import psycopg2

conn = psycopg2.connect(dbname="inventory")
cur = conn.cursor()

cur.execute("""
CREATE TABLE items (
    item_id SERIAL PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    vendor VARCHAR(255),
    type VARCHAR(255),
    quantity_on_hand INTEGER NOT NULL,
    par INTGER NOT NULL,
    value_on_hand FLOAT NOT NULL,
    last_ordered DATE
);
""")
conn.commit()
