# tests/integration/test_insert_raw_sales.py

from datetime import datetime


def test_insert_raw_sale(db_connection):

    cursor = db_connection.cursor()

    # massa de teste
    customer_id = 1
    amount = 150.00
    sale_date = datetime.now()

    # insert
    insert_sql = """
        INSERT INTO public.raw_sales (
            customer_id,
            amount,
            sale_date
        )
        VALUES (%s, %s, %s)
    """

    cursor.execute(
        insert_sql,
        (
            customer_id,
            amount,
            sale_date
        )
    )

    db_connection.commit()

    # valida persistência
    cursor.execute("""
        SELECT
            customer_id,
            amount
        FROM public.raw_sales
        WHERE customer_id = %s
        ORDER BY sale_date DESC
        LIMIT 1
    """, (customer_id,))

    result = cursor.fetchone()

    # assertions
    assert result is not None
    assert result[0] == customer_id
    assert float(result[1]) == amount

    cursor.close()