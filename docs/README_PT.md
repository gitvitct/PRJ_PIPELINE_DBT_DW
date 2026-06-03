# 🚀 Instalação, Execução e Arquitetura – PRJ_PIPE_PG_DBT_AIRFLOW 
## 🧠 1. Visão Geral

Pipeline desenvolvido com Apache Airflow, dbt, PostgreSQL, Docker e Pytest, simulando um fluxo completo de ingestão, validação, transformação e disponibilização de dados para análise.

- Este projeto implementa um pipeline moderno de dados em ambiente containerizado, integrando:

      - PostgreSQL              → camada de armazenamento (DW + metadata Airflow)
      - Apache Airflow          → orquestração do pipeline (DAGs)
      - dbt (data build tool)   → transformação ELT (camada analítica)
      - Docker Compose          → provisionamento completo do ambiente
      - Pytest                  → Testes unitários e integrados

- Fluxo de dados:

      Postgres (raw_sales)
            ↓
      Airflow DAG (ingestão + validação)
            ↓
      dbt models (staging + marts)
            ↓
      tabelas analíticas (sales_summary)


## 📦 2. Pré-requisitos 

Antes da instalação:

      Docker Engine 20+
      Docker Compose v2+
      Git
      WSL2 (Windows) ou Linux/MacOS

Verificação:

      docker --version
      docker compose version
      git --version


## 📥 3. Clonagem do Repositório 

      git clone https://github.com/gitvitct/PRJ_PIPE_PG_DBT_AIRFLOW_GIT.git
      
      cd ${prj_dir}/PRJ_PIPE_PG_DBT_AIRFLOW_GIT


## ⚙️ 4. Inicialização do Ambiente (Bootstrap) 

      cd ${prj_dir}/PRJ_PIPE_PG_DBT_AIRFLOW_GIT/docker

            - Permissão de execução:
                  chmod +x bootstrap.sh

            - Execução do ambiente completo:
                  ./bootstrap.sh


### O que este script executa internamente:

            Criação do ficheiro .env
            Definição de variáveis de ambiente
            Postgres (AIRFLOW_DB + DW_DB)
            Credenciais padrão (admin/admin)
            Build das imagens Docker (Airflow + dbt + Postgres)
            Inicialização do Docker Compose
            Criação de diretórios de logs e permissões
            Inicialização do Airflow metadata database
            
            Subida dos serviços:
                  postgres
                  dpage/pgadmin4
                  airflow-webserver
                  airflow-scheduler
                  airflow-triggerer


## 🧩 5. Validação da Infraestrutura 

      - Verificação dos containers:
            docker ps

      - Esperado:
            postgres          (healthy)
            airflow-webserver (healthy)
            airflow-scheduler (healthy)
            airflow-triggerer (up)
            dpage/pgadmin4    (up)


## 📊 6. Execução dos Testes (pytest) 

      cd ${prj_dir}/PRJ_PIPE_PG_DBT_AIRFLOW_GIT/docker
      docker compose exec airflow-webserver pytest -v -p no:cacheprovider


# 🌐 7. Acesso à Interface Airflow 

- URL:

      http://localhost:8080

- Credenciais padrão:

      user: airflow
      password: airflow


## 🔄 8. Execução do Pipeline (DAG) 

- No Airflow:

Ativar DAG:

      sales_pipeline
            Executar manualmente (Trigger DAG)

      Monitorar etapas:
            create_table      → criação do schema raw
            load_sales        → ingestão e validação de dados
            run_dbt           → transformação analítica


## 🗄️ 9. Validação no Banco de Dados 

- Acesso via CLI:

      docker exec -it docker-postgres-1 psql -U admin -d sales_dw
      psql -h postgres -p 5432 -U admin -d sales_dw


- Verificação:

      \dt

      SELECT * FROM public.raw_sales LIMIT 10;
      SELECT * FROM public.sales_summary;


            List of relations
      Schema |     Name      | Type  | Owner 
      --------+---------------+-------+-------
      public | raw_sales     | table | admin
      public | sales_summary | table | admin


## 🧪 10. Execução Manual do dbt (Opcional) 

- Acesso ao container:

      docker exec -it docker-airflow-webserver-1 bash

- Execução:

      cd /opt/airflow/dbt_project

            dbt debug --profiles-dir .
            dbt run --profiles-dir .

## 🧯 11. Dead Letter (Tratamento de Registros Inválidos)

**/opt/airflow/data/deadletter.json**

No pipeline `sales_pipeline`, o **Dead Letter** é responsável por armazenar registros que falham nas validações de qualidade durante a etapa de ingestão de dados (`load_sales`).

Ele garante que nenhum dado inválido seja perdido silenciosamente, permitindo auditoria e reprocessamento posterior.

      Ex:
      {
            "record": {
                  "order_id": 14,
                  "customer_id": 16,
                  "amount": -11.28,
                  "purchase_date": "2026-05-31 20:33:31"
            },
            "error": "Amount inv\u00e1lido"
      }

## 📊 12. Monitoramento e Observabilidade 

      - Logs Airflow:
            docker logs -f docker-airflow-scheduler-1
            docker logs -f docker-airflow-webserver-1

      - Logs de pipeline customizado:
            tail -f logs/pipeline.log


## 🔁 13. Reset / Rebuild do Ambiente 

- Para reinicialização completa:

      docker compose down -v
      docker compose up -d
      
   


## 📂 Estrutura do Projeto ################################################################################

PRJ_PIPE_PG_DBT_AIRFLOW/
      │
      ├── dags/
      │   └── sales_pipeline.py
      │
      ├── scripts/
      │   ├── create_tables.py
      │   ├── load_sales.py
      │   ├── validation.py
      │   ├── db_connection.py
      │   ├── logger_config.py
      │   └── make_deadletter_json.py
      │
      ├── dbt_project/
      │   ├── models/
      │   │   ├── staging/
      │   │   │   └── stg_sales.sql
      │   │   └── marts/
      │   │       └── sales_summary.sql
      │   ├── logs/
      │   │   └── dbt.log
      │   │
      │   ├── dbt_project.yml
      │   └── profiles.yml
      │
      ├── tests/
      │   ├── unit/
      │   │      ├── test_db_connection.py
      │   │      ├── test_deadletter.py
      │   │      ├── test_logger.py
      │   │      └── test_validation.py
      |   │
      │   ├── integration/
      │   │      ├── test_create_tables.py
      │   │      ├── test_insert_raw_sales.py
      │   │      ├── test_load_sales.py
      │   │      └── test_postgres_connection.py
      │   │
      │   ├── airflow/
      │   │      ├── test_dag_integrity.py
      │   │      ├── test_dag_loaded.py
      │   │      └── test_dag_tasks.py
      │   │
      │   ├── dbt/
      │   │     ├── test_dbt_mart.py
      │   │     ├── test_dbt_models.py
      │   │     └── test_dbt_staging.py
      │   │
      │   └── e2e/
      │         └── test_end_to_end_pipeline.py
      │
      ├── data/
      │   └── deadletter/
      │
      ├── logs/
      │   └── pipeline.log
      │
      ├── Dockerfile
      ├── docker-compose.yml
      ├── requirements.txt
      └── README.md

