## Documentation

- 🇺🇸 English
- 🇧🇷 [Português](docs/README_PT.md)


# 🚀 Installation, Execution and Architecture – PRJ_PIPE_PG_DBT_AIRFLOW

## 🧠 1. Overview

This project implements a modern data pipeline using Apache Airflow, dbt, PostgreSQL, Docker, and Pytest, simulating a complete workflow for data ingestion, validation, transformation, and analytics delivery.

### Technologies Used

* **PostgreSQL** → Data Warehouse and Airflow metadata storage
* **Apache Airflow** → Pipeline orchestration
* **dbt (Data Build Tool)** → ELT transformations and analytical layer
* **Docker Compose** → Environment provisioning and container management
* **Pytest** → Unit, integration, and end-to-end testing

### Data Flow

```text
PostgreSQL (raw_sales)
        ↓
Airflow DAG (ingestion + validation)
        ↓
dbt Models (staging + marts)
        ↓
Analytical Tables (sales_summary)
```

---

## 📦 2. Prerequisites

Before installation, ensure the following tools are available:

```bash
Docker Engine 20+
Docker Compose v2+
Git
WSL2 (Windows) or Linux/MacOS
```

### Verify Installation

```bash
docker --version
docker compose version
git --version
```

---

## 📥 3. Clone the Repository

```bash
git clone https://github.com/gitvitct/PRJ_PIPE_PG_DBT_AIRFLOW_GIT.git

cd ${prj_dir}/PRJ_PIPE_PG_DBT_AIRFLOW_GIT
```

---

## ⚙️ 4. Environment Initialization (Bootstrap)

Navigate to the Docker directory:

```bash
cd ${prj_dir}/PRJ_PIPE_PG_DBT_AIRFLOW_GIT/docker
```

Grant execution permission:

```bash
chmod +x bootstrap.sh
```

Start the complete environment:

```bash
./bootstrap.sh
```

### What the Bootstrap Script Does

The script automatically performs the following tasks:

* Creates the `.env` file
* Defines environment variables
* Creates PostgreSQL databases (`AIRFLOW_DB` and `DW_DB`)
* Configures default credentials (`admin/admin`)
* Builds Docker images (Airflow, dbt, PostgreSQL)
* Starts Docker Compose services
* Creates log directories and permissions
* Initializes the Airflow metadata database

### Services Started

* PostgreSQL
* pgAdmin
* Airflow Webserver
* Airflow Scheduler
* Airflow Triggerer

---

## 🧩 5. Infrastructure Validation

Verify running containers:

```bash
docker ps
```

Expected output:

```text
postgres              (healthy)
airflow-webserver     (healthy)
airflow-scheduler     (healthy)
airflow-triggerer     (running)
dpage/pgadmin4        (running)
```

---

## 📊 6. Running Tests (Pytest)

Execute the test suite:

```bash
cd ${prj_dir}/PRJ_PIPE_PG_DBT_AIRFLOW_GIT/docker

docker compose exec airflow-webserver pytest -v -p no:cacheprovider
```

---

## 🌐 7. Accessing the Airflow UI

### URL

```text
http://localhost:8080
```

### Default Credentials

```text
Username: airflow
Password: airflow
```

---

## 🔄 8. Executing the Pipeline (DAG)

Within the Airflow UI:

### Enable DAG

```text
sales_pipeline
```

### Trigger DAG Manually

Click **Trigger DAG**.

### Pipeline Stages

```text
create_table  → Create raw schema and tables
load_sales    → Data ingestion and validation
run_dbt       → Analytical transformations
```

---

## 🗄️ 9. Database Validation

### Connect via CLI

```bash
docker exec -it docker-postgres-1 psql -U admin -d sales_dw
```

or

```bash
psql -h postgres -p 5432 -U admin -d sales_dw
```

### Verify Tables

```sql
\dt

SELECT * FROM public.raw_sales LIMIT 10;

SELECT * FROM public.sales_summary;
```

Expected output:

```text
Schema |      Name       | Type  | Owner
-------+-----------------+-------+-------
public | raw_sales       | table | admin
public | sales_summary   | table | admin
```

---

## 🧪 10. Running dbt Manually (Optional)

Access the Airflow container:

```bash
docker exec -it docker-airflow-webserver-1 bash
```

Navigate to the dbt project:

```bash
cd /opt/airflow/dbt_project
```

Execute:

```bash
dbt debug --profiles-dir .

dbt run --profiles-dir .
```

---

## 🧯 11. Dead Letter Queue (Invalid Record Handling)

Location:

```text
/opt/airflow/data/deadletter.json
```

Within the `sales_pipeline`, the **Dead Letter Queue (DLQ)** stores records that fail data quality validations during the ingestion process (`load_sales`).

This mechanism prevents invalid records from being silently discarded and enables auditing, troubleshooting, and future reprocessing.

### Example

```json
{
  "record": {
    "order_id": 14,
    "customer_id": 16,
    "amount": -11.28,
    "purchase_date": "2026-05-31 20:33:31"
  },
  "error": "Invalid amount"
}
```

---

## 📊 12. Monitoring and Observability

### Airflow Logs

```bash
docker logs -f docker-airflow-scheduler-1

docker logs -f docker-airflow-webserver-1
```

### Custom Pipeline Logs

```bash
tail -f logs/pipeline.log
```

---

## 🔁 13. Environment Reset / Rebuild

To completely rebuild the environment:

```bash
docker compose down -v

docker compose up -d
```

---

# 📂 Project Structure

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

## 🎯 Project Objectives

This project demonstrates practical experience with:

* Data Engineering fundamentals
* ELT pipelines using dbt
* Workflow orchestration with Airflow
* Containerized environments using Docker
* Data quality validation
* Dead Letter Queue implementation
* PostgreSQL Data Warehousing
* Automated testing with Pytest
* Analytics-ready data modeling

It was designed as a portfolio project to showcase modern Data Engineering best practices and production-like architecture.
