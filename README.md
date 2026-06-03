🌎 Language:
- 🇺🇸 English (default)
- 🇧🇷 [Português](docs/README_PT.md)

# 🚀 PRJ_PIPELINE_DBT_DW

A modern Data Warehouse project built with **dbt**, **Apache Airflow**, **PostgreSQL**, **Docker**, and **Pytest**, following the **Medallion Architecture (Bronze → Silver → Gold)** and **Dimensional Modeling (Kimball)** principles.

This project simulates a complete analytical data platform, including data ingestion, transformation, historical tracking (SCD Type 2), fact and dimension modeling, orchestration, testing, and documentation.

---

# 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Technologies Used](#-technologies-used)
- [Data Pipeline Flow](#-data-pipeline-flow)
- [Data Modeling](#-data-modeling)
- [Snapshots (SCD Type 2)](#-snapshots-scd-type-2)
- [Airflow DAGs](#-airflow-dags)
- [Testing](#-testing)
- [Installation](#-installation)
- [Execution](#-execution)
- [Useful Commands](#-useful-commands)
- [Future Improvements](#-future-improvements)

---

# 🧠 Project Overview

The objective of this project is to demonstrate an end-to-end modern Data Engineering workflow.

The pipeline performs:

- Data ingestion into PostgreSQL
- Data quality validation
- Data transformation using dbt
- Historical tracking with snapshots (SCD Type 2)
- Dimensional modeling
- Fact table generation
- Workflow orchestration with Airflow
- Automated testing with Pytest and dbt tests

---

# 🏗️ Architecture

```text
                +------------------+
                |   Source Data    |
                +---------+--------+
                          |
                          v
                +------------------+
                |      Bronze      |
                | Raw Source Data  |
                +---------+--------+
                          |
                          v
                +------------------+
                |      Silver      |
                | Cleaned Data     |
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

---

# 📂 Project Structure

```text
PRJ_PIPELINE_DBT_DW
│
├── dags/
│   ├── customer_dimension_pipeline.py
│   └── sales_pipeline_dw.py
│
├── data/
│
├── dbt_project/
│
├── models/
│   ├── bronze/
│   │   └── sources.yml
│   │
│   ├── silver/
│   │
│   ├── gold/
│   │   ├── dimensions/
│   │   └── facts/
│   │
│   └── marts/
│
├── snapshots/
│   └── customer_snapshot.sql
│
├── scripts/
│
├── tests/
│
├── workflows/
│
├── docker/
│
├── docs/
│
├── dbt_project.yml
├── profiles.yml
├── requirements.txt
├── pytest.ini
└── README.md
```

---

# ⚙️ Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Pipeline Development |
| PostgreSQL | Data Warehouse |
| dbt Core | Data Transformation |
| Apache Airflow | Workflow Orchestration |
| Docker | Containerization |
| Pytest | Unit Testing |
| GitHub Actions | CI/CD |
| SQL | Data Modeling |

---

# 🔄 Data Pipeline Flow

## 1. Bronze Layer

Raw data is ingested from source systems and registered as dbt sources.

Example:

```sql
source('public', 'customers')
source('public', 'sales')
```

### Responsibilities

- Store raw data
- Preserve source structure
- Enable lineage tracking

---

## 2. Silver Layer

Data is standardized and cleansed.

Typical transformations:

- Null handling
- Data type standardization
- Deduplication
- Business rule validation

---

## 3. Gold Layer

Business-ready analytical models.

Contains:

### Dimensions

- Dim Customer
- Dim Date

### Facts

- Fact Sales

---

# 📊 Data Modeling

This project follows the **Kimball Dimensional Modeling** approach.

## Star Schema

```text
              +--------------+
              |  Dim_Date    |
              +------+-------+
                     |
                     |
+--------------+     |
| Dim_Customer |-----+
+------+-------+     |
       |             |
       |             |
       v             v
      +------------------+
      |    Fact_Sales    |
      +------------------+
```

### Benefits

- Fast analytical queries
- Simpler BI integration
- Better reporting performance
- Clear business definitions

---

# 🕒 Snapshots (SCD Type 2)

The project uses dbt snapshots to maintain customer history.

File:

```text
snapshots/customer_snapshot.sql
```

Tracked fields:

- customer_name
- city
- other customer attributes

dbt automatically creates:

```sql
dbt_valid_from
dbt_valid_to
```

This enables:

- Historical analysis
- Customer evolution tracking
- Point-in-time reporting

---

# 🌬️ Airflow DAGs

## Customer Dimension Pipeline

```text
customer_dimension_pipeline.py
```

Responsible for:

1. Run Snapshot
2. Build Customer Dimension
3. Execute Data Quality Tests

---

## Sales Pipeline

```text
sales_pipeline_dw.py
```

Responsible for:

1. Load Sales Data
2. Build Fact Table
3. Execute dbt Tests

---

# ✅ Testing

## Pytest

Run unit tests:

```bash
pytest
```

Or:

```bash
pytest -v
```

---

## dbt Tests

Run all tests:

```bash
dbt test
```

Examples:

```yaml
tests:
  - not_null
  - unique
```

---

# 🐳 Installation

## Clone Repository

```bash
git clone https://github.com/your-user/PRJ_PIPELINE_DBT_DW.git

cd PRJ_PIPELINE_DBT_DW
```

---

## Create Virtual Environment

### Linux / Mac

```bash
python -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🚀 Execution

## Validate Connection

```bash
dbt debug
```

---

## Load Sources

```bash
dbt seed
```

---

## Execute Snapshots

```bash
dbt snapshot
```

---

## Execute Models

```bash
dbt run
```

---

## Execute Tests

```bash
dbt test
```

---

## Generate Documentation

```bash
dbt docs generate

dbt docs serve
```

---

# 🛠️ Useful Commands

## Run Specific Model

```bash
dbt run --select dim_customer
```

---

## Run Fact Models

```bash
dbt run --select facts
```

---

## Run Dimensions

```bash
dbt run --select dimensions
```

---

## Run Snapshots

```bash
dbt snapshot
```

---

## Execute Airflow DAGs

```bash
airflow dags list
```

```bash
airflow dags trigger sales_pipeline_dw
```

```bash
airflow dags trigger customer_dimension_pipeline
```

---

# 📈 CI/CD

GitHub Actions can be configured to automatically execute:

```text
✔ dbt debug
✔ dbt run
✔ dbt test
✔ pytest
```

On every:

- Push
- Pull Request

---

# 🔮 Future Improvements

- CDC integration using Debezium
- Kafka event ingestion
- Schema Registry integration
- Data Quality monitoring with Great Expectations
- Data Observability
- Cloud deployment (AWS / Azure / GCP)
- dbt Semantic Layer
- Data Catalog integration
- Incremental Fact Processing
- Lakehouse Architecture support

---

# 👨‍💻 Author

**Vitor Melo**

Data Engineer | Analytics Engineer | BI Specialist

### Expertise

- Data Warehousing
- Dimensional Modeling
- dbt
- Apache Airflow
- PostgreSQL
- Python
- Kafka & CDC
- Oracle Analytics
- ETL / ELT Pipelines

---

⭐ If you found this project useful, consider giving it a star on GitHub.