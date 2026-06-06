# tests/integration/test_dag_tasks.py
# DagBag É como um "catálogo" de DAGs.

from airflow.models import DagBag


def test_dag_tasks():

    dagbag = DagBag()

    dag = dagbag.get_dag("sales_pipeline_dw")

    assert dag is not None

    task_ids = dag.task_ids

    assert "create_tables" in task_ids
    assert "load_customers" in task_ids
    assert "load_sales" in task_ids
    assert "dbt_silver" in task_ids
    assert "dbt_snapshot" in task_ids
    assert "dbt_dimensions" in task_ids
    assert "dbt_fact" in task_ids
    assert "dbt_marts" in task_ids
    assert "dbt_test" in task_ids