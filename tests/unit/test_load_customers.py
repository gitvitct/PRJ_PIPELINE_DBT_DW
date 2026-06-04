from unittest.mock import MagicMock
from unittest.mock import patch

from scripts.load_customers import load_customers


@patch("scripts.load_customers.get_connection")
def test_load_customers(mock_conn):

    conn = MagicMock()
    cursor = MagicMock()

    conn.cursor.return_value = cursor

    mock_conn.return_value = conn

    load_customers()

    assert cursor.execute.called
    assert conn.commit.called