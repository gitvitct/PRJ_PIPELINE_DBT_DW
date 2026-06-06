# tests/integration/test_create_tables.py

from scripts.create_tables import create_tables


def test_create_raw_sales_table(db_connection):

    create_tables()

    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = 'raw_sales'
        )
    """)

    exists = cursor.fetchone()[0]

    assert exists is True

    cursor.close()