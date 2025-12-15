# from src.ingestion.ingest import get_table_names, get_secret, db_connection, close_conn, extract_table_data

# # test get_table_names
# def test_get_table_names_returns_list_of_eleven_table_names():
#     credentials = get_secret()
#     conn = db_connection(credentials)
#     result = get_table_names(conn)
#     assert len(result) == 11

# def test_get_table_names_returns_correct_table_names():
#     credentials = get_secret()
#     conn = db_connection(credentials)
#     result = get_table_names(conn)
#     assert type(result) == list
#     assert result == ['counterparty', 'address', 'department', 'purchase_order', 'staff', 'payment_type', 'payment', 'transaction', 'design', 'sales_order', 'currency']

# # test extract_table_data
# def test_extract_table_data_returns_dict_of_len_11():
#     credentials = get_secret()
#     conn = db_connection(credentials)
#     table_names = get_table_names(conn)
#     result = extract_table_data(table_names, conn)
#     assert len(result) == 11
#     assert type(result) == list

from unittest.mock import MagicMock
from src.ingestion.ingest import get_table_names, get_secret, db_connection, extract_table_data

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