from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="customer_dimension_pipeline",
    start_date=datetime(2026,1,1),
    schedule="@daily",
    catchup=False
) as dag:

    run_scd2 = BashOperator(
        task_id="run_dim_customer",
        bash_command="""
        cd /opt/airflow/dbt_project &&
        dbt run --select dim_customer
        """
    )