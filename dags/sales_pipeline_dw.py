from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from scripts.create_tables import create_tables
from scripts.load_customers import load_customers
from scripts.load_sales import load_sales


with DAG(

    dag_id="sales_pipeline_dw",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=[
        "airflow",
        "dbt",
        "postgres",
        "medallion",
        "kimball"
    ]

) as dag:

    # =================================================================
    # RAW LAYER
    # =================================================================

    create_tables_task = PythonOperator(
        task_id="create_tables",
        python_callable=create_tables
    )

    load_customers_task = PythonOperator(
        task_id="load_customers",
        python_callable=load_customers
    )

    load_sales_task = PythonOperator(
        task_id="load_sales",
        python_callable=load_sales
    )

    # =================================================================
    # SILVER LAYER
    # Executa:
    # - stg_customers
    # - stg_sales
    # =================================================================

    dbt_silver = BashOperator(
        task_id="dbt_silver",
        bash_command="""
        cd /opt/airflow/dbt_project &&
        dbt deps &&
        dbt run --select silver
        """
    )

    # =================================================================
    # SNAPSHOT LAYER
    # Executa:
    # - customer_snapshot
    # =================================================================

    dbt_snapshot = BashOperator(
        task_id="dbt_snapshot",
        bash_command="""
        cd /opt/airflow/dbt_project &&
        dbt snapshot
        """
    )

    # =================================================================
    # GOLD - DIMENSIONS
    # Executa:
    # - dim_customer
    # - dim_date
    # =================================================================

    dbt_dimensions = BashOperator(
        task_id="dbt_dimensions",
        bash_command="""
        cd /opt/airflow/dbt_project &&
        dbt deps &&
        dbt run --select gold.dimensions
        """
    )

    # =================================================================
    # GOLD - FACTS
    # Executa:
    # - fact_sales
    # =================================================================

    dbt_fact = BashOperator(
        task_id="dbt_fact",
        bash_command="""
        cd /opt/airflow/dbt_project &&
        dbt deps &&
        dbt run --select gold.facts
        """
    )

    # =================================================================
    # MARTS - FACTS
    # Executa:
    # - sales_summary
    # =================================================================

    dbt_marts = BashOperator(
        task_id="dbt_marts",
        bash_command="""
        cd /opt/airflow/dbt_project &&
        dbt deps &&
        dbt run --select marts
        """
    )


    # =================================================================
    # DATA QUALITY
    # =================================================================

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="""
        cd /opt/airflow/dbt_project &&
        dbt deps &&
        dbt test
        """
    )

    # =================================================================
    # PIPELINE FLOW
    # =================================================================

    create_tables_task >> load_customers_task

    load_customers_task >> load_sales_task

    load_sales_task >> dbt_silver

    dbt_silver >> dbt_snapshot

    dbt_snapshot >> dbt_dimensions

    dbt_dimensions >> dbt_fact

    dbt_fact >> dbt_marts

    dbt_marts >> dbt_test