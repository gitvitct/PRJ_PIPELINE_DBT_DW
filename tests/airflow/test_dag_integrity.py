# tests/airflow/test_dag_integrity.py

from airflow.models import DagBag

#############################################################################################
def test_dag_loaded():

    dagbag = DagBag()

    assert dagbag.import_errors == {}



#############################################################################################
def test_sales_pipeline_exists():

    dagbag = DagBag()

    dag = dagbag.get_dag("sales_pipeline_dw")

    assert dag is not None


#############################################################################################
def test_tasks_exist():

    dagbag = DagBag()

    dag = dagbag.get_dag("sales_pipeline_dw")

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

    dagbag = DagBag()

    dag = dagbag.get_dag("sales_pipeline_dw")

    create_table = dag.get_task("create_tables")

    assert create_table.downstream_task_ids == {"load_customers"}