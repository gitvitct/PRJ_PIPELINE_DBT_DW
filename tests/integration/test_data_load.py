from scripts.db_connection import get_connection


def test_sales_loaded():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM raw_sales"
    )

    count = cursor.fetchone()[0]

    assert count > 0


def test_customers_loaded():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM raw_customers"
    )

    count = cursor.fetchone()[0]

    assert count > 0