from unittest.mock import MagicMock
from src.ingestion.ingest import get_table_names, extract_table_data, get_table_columns

def test_get_table_names_returns_list_of_eleven_table_names():
    mock_conn = MagicMock()
    mock_conn.run.return_value = [['_prisma_migrations'], ['counterparty'], ['address'], ['department'], ['purchase_order'], ['staff'], ['payment_type'], ['payment'], ['transaction'], ['design'], ['sales_order'], ['currency']]
    result = get_table_names(mock_conn)
    assert len(result) == 11
    assert isinstance(result, list)

def test_get_table_names_returns_correct_table_names():
    mock_conn = MagicMock()
    mock_conn.run.return_value = [['_prisma_migrations'], ['counterparty'], ['address'], ['department'], ['purchase_order'], ['staff'], ['payment_type'], ['payment'], ['transaction'], ['design'], ['sales_order'], ['currency']]
    result = get_table_names(mock_conn)
    assert result == ['counterparty', 'address', 'department', 'purchase_order', 'staff', 'payment_type', 'payment', 'transaction', 'design', 'sales_order', 'currency']

def test_extract_table_data_returns_dict_of_len_11():
    mock_conn = MagicMock()
    mock_conn.run.return_value = [['_prisma_migrations'], ['counterparty'], ['address'], ['department'], ['purchase_order'], ['staff'], ['payment_type'], ['payment'], ['transaction'], ['design'], ['sales_order'], ['currency']]
    table_names = get_table_names(mock_conn)
    result = extract_table_data(table_names, mock_conn)
    assert len(result.items()) == 11
    assert type(result) == dict
    
import pytest
from unittest.mock import MagicMock
from src.ingestion.ingest import get_table_columns

def test_get_table_columns_success():
    mock_conn = MagicMock()
    mock_conn.run.return_value = [
        ("sales_order_id",),
        ("created_at",),
        ("last_updated",),
        ("design_id",),
    ]
    result = get_table_columns(mock_conn, "sales_order")
    assert result == [
        "sales_order_id",
        "created_at",
        "last_updated",
        "design_id",
    ]
    expected_query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = 'sales_order'
        ORDER BY ordinal_position;
    """
    mock_conn.run.assert_called_once_with(expected_query)