import psycopg2


def create_sales_items_table(dbname, user, password, host="localhost", port=5432, max_ingredients=3):
    """
    Creates a table named "sales_items" with the following columns:

    - sales_item (VARCHAR(255) NOT NULL): The name of the sales item.
    - sales_item_category (VARCHAR(255)): The category of the sales item.
    - ingredient{n} (VARCHAR(255) FOREIGN KEY REFERENCES inventory_items(item_name)):
      The name of ingredient {n} (up to 3 ingredients), referencing items in the "inventory_items" table.
    - ingredient{n}_useage (FLOAT NOT NULL): The volume used per sales_item for each ingredient.

    Args:
        dbname (str): The name of the database to connect to.
        user (str): The username for database access.
        password (str): The password for database access.
        host (str, optional): The hostname or IP address of the database server (defaults to "localhost").
        port (int, optional): The port number of the database server (defaults to 5432).
        max_ingredients (int, optional): The maximum number of ingredients to include (defaults to 3).

    Raises:
        psycopg2.OperationalError: If an error occurs while connecting to the database or executing the CREATE TABLE statement.
    """

    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # Create the table with dynamic column names for ingredients and usage
        ingredient_cols = []
        usage_cols = []
        for i in range(1, max_ingredients + 1):
            ingredient_cols.append(f"ingredient{i} VARCHAR(255) FOREIGN KEY REFERENCES inventory_items(item_name)")
            usage_cols.append(f"ingredient{i}_useage FLOAT NOT NULL")

        create_table_stmt = f"""
            CREATE TABLE sales_items (
                sales_item VARCHAR(255) NOT NULL,
                sales_item_category VARCHAR(255),
                {', '.join(ingredient_cols)},
                {', '.join(usage_cols)}
            );
        """

        cur.execute(create_table_stmt)
        conn.commit()
        print("Table 'sales_items' created successfully.")

    except psycopg2.OperationalError as e:
        print(f"Error connecting to database or creating table: {e}")
    finally:
        if conn:
            conn.close()
