from datetime import datetime
from random import choice

from scripts.db_connection import get_connection

cities = [
    "Florianopolis",
    "Sao Paulo",
    "Curitiba",
    "Porto Alegre",
    "Maringá"
]

def load_customers():

    conn = get_connection()
    cur = conn.cursor()

    customers = [

        (1, "Joao Silva"),
        (2, "Maria Souza"),
        (3, "Rock Balboa"),
        (4, "Ana Costa"),
        (5, "Mano Brown"),
        (6, "Vitor Melo"),
        (7, "Jon Bone Jones")
    ]

    for customer in customers:

        cur.execute(
            """
            INSERT INTO raw_customers
            (
                customer_id,
                customer_name,
                city,
                updated_at
            )

            VALUES (%s,%s,%s,%s)

            ON CONFLICT(customer_id)

            DO UPDATE SET

                customer_name = EXCLUDED.customer_name,
                city = EXCLUDED.city,
                updated_at = EXCLUDED.updated_at
            """,
            (
                customer[0],
                customer[1],
                choice(cities),
                datetime.now()
            )
        )

    conn.commit()

    cur.close()
    conn.close()