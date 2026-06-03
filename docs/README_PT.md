# 🚀 Instalação, Execução e Arquitetura – PRJ_PIPE_PG_DBT_AIRFLOW

🌎 Idioma:

* 🇧🇷 Português (padrão)
* 🇺🇸 [English](../README.md)

---

## 🧠 1. Visão Geral

Este projeto implementa um pipeline moderno de dados utilizando Apache Airflow, dbt, PostgreSQL, Docker e Pytest, simulando um fluxo completo de ingestão, validação, transformação e disponibilização de dados para análise.

### Tecnologias Utilizadas

* **PostgreSQL** → Data Warehouse e armazenamento dos metadados do Airflow
* **Apache Airflow** → Orquestração dos pipelines
* **dbt (Data Build Tool)** → Transformações ELT e camada analítica
* **Docker Compose** → Provisionamento do ambiente e gerenciamento dos containers
* **Pytest** → Testes unitários, de integração e ponta a ponta (E2E)

### Fluxo de Dados

```text
PostgreSQL (raw_sales)
        ↓
DAG Airflow (ingestão + validação)
        ↓
Modelos dbt (staging + marts)
        ↓
Tabelas Analíticas (sales_summary)
```

---

## 📦 2. Pré-requisitos

Antes da instalação, certifique-se de possuir as seguintes ferramentas:

```bash
Docker Engine 20+
Docker Compose v2+
Git
WSL2 (Windows) ou Linux/MacOS
```

### Validando a Instalação

```bash
docker --version
docker compose version
git --version
```

---

## 📥 3. Clonando o Repositório

```bash
git clone https://github.com/gitvitct/PRJ_PIPE_PG_DBT_AIRFLOW_GIT.git

cd ${prj_dir}/PRJ_PIPE_PG_DBT_AIRFLOW_GIT
```

---

## ⚙️ 4. Inicialização do Ambiente (Bootstrap)

Acesse o diretório Docker:

```bash
cd ${prj_dir}/PRJ_PIPE_PG_DBT_AIRFLOW_GIT/docker
```

Conceda permissão de execução ao script:

```bash
chmod +x bootstrap.sh
```

Inicie todo o ambiente:

```bash
./bootstrap.sh
```

### O que o Script Bootstrap Faz

O script executa automaticamente as seguintes tarefas:

* Cria o arquivo `.env`
* Define as variáveis de ambiente
* Cria os bancos PostgreSQL (`AIRFLOW_DB` e `DW_DB`)
* Configura credenciais padrão (`admin/admin`)
* Constrói as imagens Docker (Airflow, dbt e PostgreSQL)
* Inicializa os serviços Docker Compose
* Cria diretórios de logs e permissões necessárias
* Inicializa o banco de metadados do Airflow

### Serviços Inicializados

* PostgreSQL
* pgAdmin
* Airflow Webserver
* Airflow Scheduler
* Airflow Triggerer

---

## 🧩 5. Validação da Infraestrutura

Verifique os containers em execução:

```bash
docker ps
```

Saída esperada:

```text
postgres              (healthy)
airflow-webserver     (healthy)
airflow-scheduler     (healthy)
airflow-triggerer     (running)
dpage/pgadmin4        (running)
```

---

## 📊 6. Executando os Testes (Pytest)

Execute toda a suíte de testes:

```bash
cd ${prj_dir}/PRJ_PIPE_PG_DBT_AIRFLOW_GIT/docker

docker compose exec airflow-webserver pytest -v -p no:cacheprovider
```

---

## 🌐 7. Acessando a Interface do Airflow

### URL

```text
http://localhost:8080
```

### Credenciais Padrão

```text
Usuário: airflow
Senha: airflow
```

---

## 🔄 8. Executando o Pipeline (DAG)

Na interface do Airflow:

### Habilite a DAG

```text
sales_pipeline
```

### Execute Manualmente

Clique em **Trigger DAG**.

### Etapas do Pipeline

```text
create_table  → Criação das tabelas de origem
load_sales    → Ingestão e validação dos dados
run_dbt       → Transformações analíticas
```

---

## 🗄️ 9. Validação do Banco de Dados

### Conectar via CLI

```bash
docker exec -it docker-postgres-1 psql -U admin -d sales_dw
```

ou

```bash
psql -h postgres -p 5432 -U admin -d sales_dw
```

### Verificar Tabelas

```sql
\dt

SELECT * FROM public.raw_sales LIMIT 10;

SELECT * FROM public.sales_summary;
```

Saída esperada:

```text
Schema |      Name       | Type  | Owner
-------+-----------------+-------+-------
public | raw_sales       | table | admin
public | sales_summary   | table | admin
```

---

## 🧪 10. Executando o dbt Manualmente (Opcional)

Acesse o container do Airflow:

```bash
docker exec -it docker-airflow-webserver-1 bash
```

Acesse o projeto dbt:

```bash
cd /opt/airflow/dbt_project
```

Execute:

```bash
dbt debug --profiles-dir .

dbt run --profiles-dir .
```

---

## 🧯 11. Dead Letter Queue (Tratamento de Registros Inválidos)

Localização:

```text
/opt/airflow/data/deadletter.json
```

Dentro da DAG `sales_pipeline`, a **Dead Letter Queue (DLQ)** armazena registros que falham nas validações de qualidade durante o processo de ingestão (`load_sales`).

Esse mecanismo evita que registros inválidos sejam descartados silenciosamente, permitindo auditoria, investigação de falhas e possível reprocessamento futuro.

### Exemplo

```json
{
  "record": {
    "order_id": 14,
    "customer_id": 16,
    "amount": -11.28,
    "purchase_date": "2026-05-31 20:33:31"
  },
  "error": "Valor inválido"
}
```

---

## 📊 12. Monitoramento e Observabilidade

### Logs do Airflow

```bash
docker logs -f docker-airflow-scheduler-1

docker logs -f docker-airflow-webserver-1
```

### Logs Customizados do Pipeline

```bash
tail -f logs/pipeline.log
```

---

## 🔁 13. Reinicialização Completa do Ambiente

Para reconstruir totalmente o ambiente:

```bash
docker compose down -v

docker compose up -d
```

---

# 📂 Estrutura do Projeto

```text
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
│   │
│   ├── logs/
│   │   └── dbt.log
│   │
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── tests/
│   ├── unit/
│   │   ├── test_db_connection.py
│   │   ├── test_deadletter.py
│   │   ├── test_logger.py
│   │   └── test_validation.py
│   │
│   ├── integration/
│   │   ├── test_create_tables.py
│   │   ├── test_insert_raw_sales.py
│   │   ├── test_load_sales.py
│   │   └── test_postgres_connection.py
│   │
│   ├── airflow/
│   │   ├── test_dag_integrity.py
│   │   ├── test_dag_loaded.py
│   │   └── test_dag_tasks.py
│   │
│   ├── dbt/
│   │   ├── test_dbt_mart.py
│   │   ├── test_dbt_models.py
│   │   └── test_dbt_staging.py
│   │
│   └── e2e/
│       └── test_end_to_end_pipeline.py
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
```

---

## 🎯 Objetivos do Projeto

Este projeto demonstra experiência prática em:

* Fundamentos de Engenharia de Dados
* Pipelines ELT com dbt
* Orquestração de workflows com Airflow
* Ambientes containerizados com Docker
* Validação de qualidade de dados
* Implementação de Dead Letter Queue (DLQ)
* Data Warehousing com PostgreSQL
* Testes automatizados com Pytest
* Modelagem de dados para Analytics

O projeto foi desenvolvido como peça de portfólio para demonstrar boas práticas modernas de Engenharia de Dados e uma arquitetura próxima a ambientes produtivos.
