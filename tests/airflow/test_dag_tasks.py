# tests/airflow/test_dag_tasks.py

from airflow.models import DagBag


def test_dag_tasks():

    dagbag = DagBag(
        dag_folder="dags",
        include_examples=False
    )

    assert dagbag.import_errors == {}

    dag = dagbag.dags["sales_pipeline_dw"]

    task_ids = dag.task_ids

    expected_tasks = [
        "create_tables",
        "load_customers",
        "load_sales",
        "dbt_silver",
        "dbt_snapshot",
        "dbt_dimensions",
        "dbt_fact",
        "dbt_marts",
        "dbt_test"
    ]

    for task in expected_tasks:
        assert task in task_ids