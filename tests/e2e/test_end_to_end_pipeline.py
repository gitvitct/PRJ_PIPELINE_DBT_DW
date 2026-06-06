# tests/integration/test_end_to_end_pipeline.py

import subprocess

from scripts.create_tables import create_tables
from scripts.load_sales import load_sales
from scripts.load_customers import load_customers


def test_end_to_end_pipeline(db_connection):

    create_tables()
    load_customers()
    load_sales()

    subprocess.run(
        ["dbt", "run"],
        cwd="/opt/airflow/dbt_project",
        check=True
    )

    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM public.sales_summary
    """)

    count = cursor.fetchone()[0]

    assert count > 0

    cursor.close()