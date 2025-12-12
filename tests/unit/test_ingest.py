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

import pandas as pd
from unittest.mock import patch, MagicMock
from src.ingestion.ingest import get_table_names, get_secret, db_connection, extract_table_data
import pyarrow as pa

# Mocking secrets, database connection, and table extraction
@patch('src.ingestion.ingest.get_secret')
@patch('src.ingestion.ingest.db_connection')
@patch('src.ingestion.ingest.get_table_names')
@patch('src.ingestion.ingest.extract_table_data')

def test_get_table_names_returns_list_of_eleven_table_names(mock_extract, mock_tables, mock_conn, mock_secret):
    # Mock return values
    #mock_secret.return_value = {'user': 'test', 'password': 'test'}
    #mock_conn.return_value = MagicMock()
    mock_tables.return_value = ['counterparty', 'address', 'department', 'purchase_order', 'staff', 'payment_type', 'payment', 'transaction', 'design', 'sales_order', 'currency']
    #mock_extract.return_value = [{'id': 1}, {'id': 2}]
    
    # Execute pipeline functions with mocks
    credentials = get_secret()
    conn = db_connection(credentials)
    result = get_table_names(conn)
    #result = extract_table_data(table_names, conn) 

    
    # Validate
    # assert credentials == {'user': 'test', 'password': 'test'}
    # assert table_names == ['counterparty', 'address', 'department']
    # assert result == [{'id': 1}, {'id': 2}]
    assert len(result) == 11

@patch('src.ingestion.ingest.get_secret')
@patch('src.ingestion.ingest.db_connection')
@patch('src.ingestion.ingest.get_table_names')
@patch('src.ingestion.ingest.extract_table_data')

def test_get_table_names_returns_correct_table_names(mock_extract, mock_tables, mock_conn, mock_secret):
    mock_tables.return_value = ['counterparty', 'address', 'department', 'purchase_order', 'staff', 'payment_type', 'payment', 'transaction', 'design', 'sales_order', 'currency']
    #mock_extract.return_value = [{'id': 1}, {'id': 2}]
    
    # Execute pipeline functions with mocks
    credentials = get_secret()
    conn = db_connection(credentials)
    result = get_table_names(conn)
    #result = extract_table_data(table_names, conn)
    assert type(result) == list
    assert result == ['counterparty', 'address', 'department', 'purchase_order', 'staff', 'payment_type', 'payment', 'transaction', 'design', 'sales_order', 'currency']


@patch('src.ingestion.ingest.get_secret')
@patch('src.ingestion.ingest.db_connection')
@patch('src.ingestion.ingest.get_table_names')
@patch('src.ingestion.ingest.extract_table_data')
def test_extract_table_data_returns_dict_of_len_11(mock_extract, mock_tables, mock_conn, mock_secret):
    mock_tables.return_value = ['counterparty', 'address', 'department', 'purchase_order', 'staff', 'payment_type', 'payment', 'transaction', 'design', 'sales_order', 'currency']
    credentials = get_secret()
    conn = db_connection(credentials)
    table_names = get_table_names(conn)
    result = extract_table_data(table_names, conn)
    assert len(result.items()) == 11
    assert type(result) == dict