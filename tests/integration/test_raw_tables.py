from scripts.db_connection import get_connection


def test_raw_sales_exists():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name='raw_sales'
        )
    """)

    assert cursor.fetchone()[0]


def test_raw_customers_exists():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name='raw_customers'
        )
    """)

    assert cursor.fetchone()[0]