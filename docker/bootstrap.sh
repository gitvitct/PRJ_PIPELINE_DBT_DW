#!/bin/bash

set -e

echo "========================================="
echo "Criando arquivo .env"
echo "========================================="

cat <<EOF > .env
# =========================
# POSTGRES
# =========================

POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_SCHEMA=public
POSTGRES_DB=POSTGRES_DB

# =========================
# AIRFLOW METADATA DB
# =========================

AIRFLOW_DB=airflow

# =========================
# DATA WAREHOUSE DB
# =========================

DW_DB=sales_dw

# =========================
# DBT
# =========================

DBT_TARGET=dev
DBT_THREADS=2
EOF

echo ".env criado com sucesso."

echo ""
echo "========================================="
echo "Ajustando permissões do dbt"
echo "========================================="

sudo chown -R 50000:root ../dbt_project/


echo ""
echo "========================================="
echo "Ajustando permissões do LOG"
echo "========================================="

sudo chown -R 50000:root ../logs/


echo ""
echo "========================================="
echo "Subindo containers"
echo "========================================="

docker compose up -d

echo ""
echo "========================================="
echo "Aguardando Airflow inicializar"
echo "========================================="

echo "Aguardando banco do Airflow..."

until docker exec docker-airflow-scheduler-1 airflow db check >/dev/null 2>&1
do
    echo "Aguardando Airflow..."
    sleep 5
done

echo ""
echo "========================================="
echo "Criando usuário Airflow"
echo "========================================="

docker exec -i docker-airflow-webserver-1 airflow users create \
    --username airflow \
    --firstname F_name \
    --lastname L_name \
    --role Admin \
    --email admin@email.com \
    --password airflow

echo ""
echo "========================================="
echo "Bootstrap concluído"
echo "========================================="
echo ""
echo "Airflow:"
echo "  URL      : http://localhost:8080"
echo "  Usuário  : airflow"
echo "  Senha    : airflow"
echo ""
echo "pgAdmin:"
echo "  URL      : http://localhost:5050"