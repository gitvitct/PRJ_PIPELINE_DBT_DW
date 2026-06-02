from scripts.db_connection import get_connection

def create_tables():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS raw_customers(

        customer_id INTEGER PRIMARY KEY,
        customer_name VARCHAR(100),
        city VARCHAR(100),

        updated_at TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS raw_sales(

        sale_id SERIAL ,
                 

        customer_id INTEGER,

        amount NUMERIC(12,2),

        sale_date TIMESTAMP,

        updated_at TIMESTAMP
    )
    """)

    conn.commit()

    cur.close()
    conn.close()