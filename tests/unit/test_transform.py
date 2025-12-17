from src.transformation.transformer import get_timestamp

def test_get_timestamp_returns_str_of_most_recent_ingestion_time():
    result = get_timestamp('adress')
    assert isinstance(result, str)
