import random
from datetime import datetime

from scripts.validation import validate_sale
from scripts.logger_config import logger
from scripts.db_connection import get_connection
from scripts.make_deadletter_json import save_deadletter


def load_sales():

    deadletter = []

    logger.info("Iniciando carga de vendas")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        for i in range(1, 201):

            sale = {
                "order_id": i,
                "customer_id": random.randint(1, 7),
                "amount": round(random.uniform(-50, 500), 2),
                "purchase_date": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }

            is_valid, error = validate_sale(sale)

            if not is_valid:

                logger.error(
                    f"Registro inválido: {sale} - {error}"
                )

                deadletter.append({
                    "record": sale,
                    "error": error
                })

                continue

            cursor.execute(
                """
                INSERT INTO raw_sales
                VALUES (%s, %s, %s, %s)
                """,
                (
                    sale["order_id"],
                    sale["customer_id"],
                    sale["amount"],
                    sale["purchase_date"]
                )
            )

        conn.commit()

        logger.info("Carga finalizada")

        print(
            f"Registros inválidos: {len(deadletter)}"
        )

        save_deadletter(deadletter)

    except Exception as e:

        logger.error(
            f"Erro durante a carga: {str(e)}"
        )

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()


if __name__ == "__main__":
    load_sales()