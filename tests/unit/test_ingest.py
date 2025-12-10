from src.ingestion.ingest import get_table_names

# test get_table_names
def test_get_table_names_returns_list_of_eleven_table_names():
    result = get_table_names()
    assert len(result) == 11
