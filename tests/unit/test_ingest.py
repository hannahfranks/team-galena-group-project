from src.ingestion.ingest import get_table_names, get_secret, db_connection, close_conn

# test get_table_names
def test_get_table_names_returns_list_of_eleven_table_names():
    credentials = get_secret()
    conn = db_connection(credentials)
    result = get_table_names(conn, credentials)
    assert len(result) == 11

def test_get_table_names_returns_correct_table_names():
    credentials = get_secret()
    conn = db_connection(credentials)
    result = get_table_names(conn, credentials)
    assert type(result) == list
    assert result == ['counterparty', 'address', 'department', 'purchase_order', 'staff', 'payment_type', 'payment', 'transaction', 'design', 'sales_order', 'currency']
