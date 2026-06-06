# 📖 Overview

Modern Data Warehouse project built with Python, PostgreSQL, Apache Airflow, dbt, Docker and Pytest, implementing Medallion Architecture and Kimball Dimensional Modeling.

This project demonstrates a complete end-to-end Data Engineering workflow.

The pipeline simulates the ingestion, validation, transformation, historization and delivery of analytical data through a modern Data Warehouse architecture.

## Main Features

✅ Automated data ingestion

✅ Data quality validation

✅ Dead Letter Queue for invalid records

✅ dbt transformations

✅ Incremental processing

✅ SCD Type 2 implementation

✅ Dimensional Modeling

✅ Fact and Dimension tables

✅ Workflow orchestration with Airflow

✅ Automated testing

---

# 🏗️ Architecture

```text
                +------------------+
                | Source Systems   |
                +---------+--------+
                          |
                          v
                +------------------+
                |      Bronze      |
                | Raw Data Layer   |
                +---------+--------+
                          |
                          v
                +------------------+
                |      Silver      |
                | Cleansed Data    |
                | Business Rules   |
                +---------+--------+
                          |
                          v
                +------------------+
                |       Gold       |
                | Facts & Dims     |
                +---------+--------+
                          |
                          v
                +------------------+
                | BI / Analytics   |
                +------------------+
```

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/gitvitct/PRJ_PIPELINE_DBT_DW.git
cd PRJ_PIPELINE_DBT_DW
```

---


## ⚙️ Environment Initialization (Bootstrap)

Navigate to the Docker directory:

```bash
cd PRJ_PIPELINE_DBT_DW/docker
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




# 🐳 Docker Execution/Verification

Build:

```bash
docker compose build
```

Start:

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```


---

# 📂 Project Structure

```text
PRJ_PIPELINE_DBT_DW
│
├── dags/
│   ├── sales_pipeline_dw.py
│   └── customer_dimension_pipeline.py
│
├── scripts/
│   ├── create_tables.py
│   ├── load_customers.py
│   ├── load_sales.py
│   ├── validation.py
│   ├── logger_config.py
│   ├── db_connection.py
│   └── make_deadletter_json.py
│
├── dbt_project/
│   ├── models/
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   │
│   ├── snapshots/
│   │   └── customer_snapshot.sql
│   │
│   ├── tests/
│   ├── logs/
│   ├── profiles.yml
│   └── dbt_project.yml
│
├── tests/
│
├── docs/
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Technologies

| Technology | Purpose |
|------------|----------|
| Python | ETL Development |
| PostgreSQL | Data Warehouse |
| Apache Airflow | Workflow Orchestration |
| dbt Core | Data Transformation |
| Docker | Containerization |
| Pytest | Automated Testing |
| SQL | Data Modeling |
| GitHub Actions | CI/CD |

---

# 🔄 Pipeline Flow

## Step 1 – Raw Data Creation

Airflow starts the pipeline by creating source tables:

### raw_customers

```sql
customer_id
customer_name
city
updated_at
```

### raw_sales

```sql
sale_id
customer_id
amount
sale_date
updated_at
```

---

## Step 2 – Customer Load

Customer records are inserted into the source table.

Features:

- Upsert strategy
- Random city assignment
- Timestamp tracking

Example:

```python
ON CONFLICT(customer_id)
DO UPDATE
```

---

## Step 3 – Sales Load

Sales are generated automatically.

Features:

- Random amounts
- Customer assignment
- Validation process

Generated fields:

```text
order_id
customer_id
amount
purchase_date
```

---

## Step 4 – Data Validation

Every sale is validated before insertion.

Example rules:

```text
Amount must be greater than zero
Required fields cannot be null
```

Invalid records are redirected to Dead Letter Queue.

---

## Step 5 – Dead Letter Queue

Invalid records are stored as JSON.

Example:

```json
{
  "record": {
    "order_id": 10,
    "amount": -50
  },
  "error": "Amount cannot be negative"
}
```

Benefits:

- Error auditing
- Reprocessing capability
- Data quality monitoring

---

# 🥉 Bronze Layer

The Bronze layer contains raw source data.

Tables:

```text
raw_customers
raw_sales
```

Responsibilities:

- Preserve source structure
- Store original data
- Enable lineage tracking

---

# 🥈 Silver Layer

The Silver layer standardizes and cleanses data.

Models:

```text
stg_customers
stg_sales
```

Transformations:

- Data type standardization
- Null handling
- Data quality checks
- Naming conventions

Execution:

```bash
dbt run --select silver
```

---

# 📸 Customer Snapshot (SCD Type 2)

The project implements historical tracking using dbt snapshots.

Snapshot:

```text
customer_snapshot
```

Strategy:

```yaml
strategy: timestamp
```

Tracked field:

```yaml
updated_at
```

Benefits:

- Historical customer changes
- Point-in-time analysis
- Slowly Changing Dimension Type 2

Execution:

```bash
dbt snapshot
```

---

# 🥇 Gold Layer

The Gold layer contains analytical models.

## Dimension: dim_customer

Stores customer history.

Attributes:

```text
customer_sk
customer_id
customer_name
city
valid_from
valid_to
current_flag
```

Characteristics:

- Surrogate key
- SCD Type 2
- Historical tracking

---

## Dimension: dim_date

Date dimension used by facts.

Attributes:

```text
date_sk
full_date
year
month
quarter
day_of_week
```

Benefits:

- Faster reporting
- Standardized calendar analysis

---

## Fact Table: fact_sales

Central analytical fact table.

Attributes:

```text
sale_id
customer_sk
date_sk
amount
sale_date
updated_at
```

Relationships:

```text
fact_sales
    |
    +---- dim_customer
    |
    +---- dim_date
```

Execution:

```bash
dbt run --select gold.facts
```

---

# 🔄 Airflow Orchestration

Main DAG:

```text
sales_pipeline_dw
```

Execution Flow:

```text
create_tables
        ↓
load_customers
        ↓
load_sales
        ↓
dbt_silver
        ↓
dbt_snapshot
        ↓
dbt_dimensions
        ↓
dbt_fact
        ↓
dbt_test
```

Schedule:

```python
@daily
```

Catchup:

```python
False
```

---

# ✅ Data Quality

dbt tests validate:

```text
not_null
unique
relationships
accepted_values
```

Execution:

```bash
dbt test
```

Benefits:

- Data reliability
- Referential integrity
- Automated quality checks

---

# 🚀 CI/CD with GitHub Actions

This project uses GitHub Actions to automatically validate code quality and project integrity on every push, pull request, or manual execution.

The CI pipeline helps ensure that all components of the Data Warehouse remain functional and integrated.
## ✅ Detect bugs before deployment
## ✅ Prevent broken code from reaching production
## ✅ Validate database connectivity
## ✅ Automatically execute unit and integration tests
## ✅ Improve repository reliability
## ✅ Increase confidence during refactoring
## ✅ Simulate enterprise-grade development workflows


# 🧪 Testing

Framework:

```text
Pytest
```

Suggested Tests:

### Unit Tests

```text
validate_sale()
create_tables()
load_customers()
load_sales()
```

### Integration Tests

```text
Database Connection
Data Loading
dbt Models
Airflow DAGs
```

Execution:

```bash
pytest
```

---

---

# 📊 dbt Commands

Run Silver Models:

```bash
dbt run --select silver
```

Run Dimensions:

```bash
dbt run --select gold.dimensions
```

Run Facts:

```bash
dbt run --select gold.facts
```

Run Everything:

```bash
dbt run
```

Snapshot:

```bash
dbt snapshot
```

Tests:

```bash
dbt test
```

Documentation:

```bash
dbt docs generate
dbt docs serve
```

---

# 📈 Data Warehouse Model

```text
               dim_customer
                     |
                     |
                     |
                fact_sales
                     |
                     |
                     |
                  dim_date
```

Model Type:

```text
Star Schema
```

Methodology:

```text
Kimball
```

---

# 🎯 Objectives

This project demonstrates:

- Data Warehouse Design
- Kimball Modeling
- Medallion Architecture
- Apache Airflow Orchestration
- dbt Development
- Incremental Processing
- SCD Type 2
- Data Quality Engineering
- PostgreSQL Administration
- Docker Containerization
- CI/CD Readiness

---
