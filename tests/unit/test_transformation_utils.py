import pandas as pd
from unittest.mock import MagicMock, patch
import pytest

from src.transformation.transformer import get_timestamp
from src.transformation.utils.save_parquet_to_s3 import write_parquet_to_s3
from src.transformation.utils.parser import attach_columns_to_dataframe

@patch("src.transformation.utils.save_parquet_to_s3.s3_client")
def test_write_parquet_to_s3_uploads_file(mock_s3_client):
    df = pd.DataFrame({
        "id": [1, 2],
        "name": ["London", "Manchester"]
    })

    bucket = "galena-s3-transformation-lambda-bucket"
    key_prefix = "dim_location"

    write_parquet_to_s3(df, bucket, key_prefix)

    mock_s3_client.put_object.assert_called_once()

    args, kwargs = mock_s3_client.put_object.call_args

    assert kwargs["Bucket"] == bucket
    assert kwargs["Key"].startswith(key_prefix)
    assert kwargs["Key"].endswith(".parquet")
    assert isinstance(kwargs["Body"], (bytes, bytearray))
    assert kwargs["ContentType"] == "application/octet-stream"

# test timestamp 
def test_get_timestamps_returns_str_of_most_recent_ingestion_time_for_table():
    result = get_timestamp('address')
    assert isinstance(result, str)
    
#test parser
def test_attach_columns_to_dataframe():
    df = pd.DataFrame([[1, "A"], [2, "B"]])
    columns = ["id", "name"]

    result = attach_columns_to_dataframe(df, columns)

    assert list(result.columns) == columns
    assert result.iloc[0]["name"] == "A"
    
def test_attach_columns_mismatch_raises():
    df = pd.DataFrame([[1, "A"]])
    columns = ["id"]

    with pytest.raises(ValueError):
        attach_columns_to_dataframe(df, columns)
