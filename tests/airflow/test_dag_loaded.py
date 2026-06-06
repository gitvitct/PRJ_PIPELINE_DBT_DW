# tests/integration/test_dag_loaded.py
# Importa a classe que carrega todas as DAGs do Airflow

from airflow.models import DagBag


def test_dag_loaded():

    # Carrega todas as DAGs encontradas na pasta dags/
    dagbag = DagBag()

    # Procura a DAG chamada "sales_pipeline_dw"
    dag = dagbag.get_dag("sales_pipeline_dw")

    # Verifica se a DAG foi carregada com sucesso
    assert dag is not None