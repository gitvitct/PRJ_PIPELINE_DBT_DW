# tests/airflow/test_dag_loaded.py

from airflow.models import DagBag


def test_dag_loaded():

    dagbag = DagBag(
        dag_folder="dags",
        include_examples=False
    )

    assert dagbag.import_errors == {}

    assert "sales_pipeline_dw" in dagbag.dags