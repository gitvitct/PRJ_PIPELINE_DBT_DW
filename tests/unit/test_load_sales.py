from unittest.mock import MagicMock
from unittest.mock import patch

from scripts.load_sales import load_sales


@patch("scripts.load_sales.get_connection")
def test_load_sales(mock_conn):

    conn = MagicMock()
    cursor = MagicMock()

    conn.cursor.return_value = cursor

    mock_conn.return_value = conn

    load_sales()

    assert cursor.execute.called
    assert conn.commit.called