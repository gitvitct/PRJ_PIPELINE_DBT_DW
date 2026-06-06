# tests/integration/conftest.py

import pytest
import psycopg2
import os

from scripts.create_tables import create_tables


@pytest.fixture(scope="session")
def db_connection():

    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("DW_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT")
    )

    yield conn

    conn.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Garante que a tabela exista antes dos testes.
    """
    create_tables()


@pytest.fixture(autouse=True)
def clean_raw_sales(db_connection):
    """
    Limpa a tabela antes de cada teste.
    """

    cursor = db_connection.cursor()

    cursor.execute("""
        TRUNCATE TABLE public.raw_sales
        RESTART IDENTITY;
    """)

    db_connection.commit()

    yield

    cursor.close()