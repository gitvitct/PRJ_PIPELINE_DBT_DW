from datetime import datetime

from airflow import DAG

from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from scripts.create_tables import create_tables
from scripts.load_customers import load_customers
from scripts.load_sales import load_sales

with DAG(

    dag_id="sales_pipeline_dw",

    start_date=datetime(2026,1,1),

    schedule="@daily",

    catchup=False,

    tags=["dbt","airflow","medallion"]

) as dag:

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

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="""
        cd /opt/airflow/dbt_project &&
        dbt run
        """
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="""
        cd /opt/airflow/dbt_project &&
        dbt test
        """
    )

    create_tables_task >> load_customers_task

    load_customers_task >> load_sales_task

    load_sales_task >> dbt_run

    dbt_run >> dbt_test