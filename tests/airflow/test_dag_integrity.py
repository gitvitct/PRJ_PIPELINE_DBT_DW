# tests/airflow/test_dag_integrity.py

from airflow.models import DagBag


def get_dag():

    dagbag = DagBag(
        dag_folder="dags",
        include_examples=False
    )

    assert dagbag.import_errors == {}

    return dagbag.dags["sales_pipeline_dw"]


#############################################################################################

def test_dag_loaded():

    dag = get_dag()

    assert dag is not None


#############################################################################################

def test_sales_pipeline_exists():

    dag = get_dag()

    assert dag.dag_id == "sales_pipeline_dw"


#############################################################################################

def test_tasks_exist():

    dag = get_dag()

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
        assert task in dag.task_ids


#############################################################################################

def test_task_dependencies():

    dag = get_dag()

    create_table = dag.get_task("create_tables")

    assert create_table.downstream_task_ids == {"load_customers"}