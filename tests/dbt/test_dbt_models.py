# tests/dbt/test_dbt_models.py

import subprocess

from scripts.db_connection import get_connection


DBT_PROJECT_DIR = "/opt/airflow/dbt_project"
DBT_PROFILES_DIR = "/opt/airflow/dbt_project"

########################################################################################################
## test_dbt_run

def test_dbt_run():

    result = subprocess.run(
        [
            "dbt",
            "run",
            "--project-dir",
            DBT_PROJECT_DIR,
            "--profiles-dir",
            DBT_PROFILES_DIR
        ],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    print(result.stderr)

    assert result.returncode == 0

########################################################################################################
## test_dbt_test

def test_dbt_test():

    result = subprocess.run(
        [
            "dbt",
            "test",
            "--project-dir",
            DBT_PROJECT_DIR,
            "--profiles-dir",
            DBT_PROFILES_DIR
        ],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    print(result.stderr)

    assert result.returncode == 0

########################################################################################################
## test_stg_sales_exists

def test_stg_sales_exists():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'stg_sales'
        );
        """
    )

    exists = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    assert exists is True

########################################################################################################
## test_sales_summary_exists

def test_sales_summary_exists():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'sales_summary'
        );
        """
    )

    exists = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    assert exists is True

########################################################################################################
## test_sales_summary_has_data

def test_sales_summary_has_data(db_connection):

    cursor = db_connection.cursor()

    cursor.execute("""
        INSERT INTO raw_sales
        (sale_id, customer_id, amount, sale_date)
        VALUES
        (1, 1, 100, NOW()),
        (2, 2, 200, NOW()),
        (3, 3, 300, NOW())
    """)

    db_connection.commit()
    cursor.close()

    subprocess.run(
        ["dbt", "run"],
        cwd="/opt/airflow/dbt_project",
        check=True
    )

    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT SUM(total_sales)
        FROM sales_summary
    """)

    total = cursor.fetchone()[0]

    cursor.close()

    assert total == 600