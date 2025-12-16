import pandas as pd
import pytest
from src.transformation.dim_location import transform_dim_location, DIM_LOCATION_COLUMNS

def test_transform_dim_location_basic():
    # Sample input address data
    df_address = pd.DataFrame({
        "address_id": [1, 2],
        "address_line_1": ["123 High St", "456 Low St"],
        "address_line_2": [None, "Apt 5"],
        "district": ["Central", "West"],
        "city": ["London", "Manchester"],
        "postal_code": ["E1 6AN", "M1 2AB"],
        "country": ["UK", "UK"],
        "phone": ["0123456789", "0987654321"],
        "created_at": ["2024-01-01", "2024-01-02"],
        "last_updated": ["2024-01-02", "2024-01-03"],
    })

    # Expected DataFrame after transformation
    df_expected = pd.DataFrame({
        "location_id": [1, 2],
        "address_line_1": ["123 High St", "456 Low St"],
        "address_line_2": [None, "Apt 5"],
        "district": ["Central", "West"],
        "city": ["London", "Manchester"],
        "postal_code": ["E1 6AN", "M1 2AB"],
        "country": ["UK", "UK"],
        "phone": ["0123456789", "0987654321"],
    })

    # Call the function
    df_result = transform_dim_location(df_address)

    # Check columns order
    assert list(df_result.columns) == DIM_LOCATION_COLUMNS

    # Check equality
    pd.testing.assert_frame_equal(df_result, df_expected)

def test_transform_dim_location_empty():
    # Empty input DataFrame
    df_empty = pd.DataFrame()

    df_result = transform_dim_location(df_empty)

    # Should return empty DataFrame with correct columns
    assert list(df_result.columns) == DIM_LOCATION_COLUMNS
    assert df_result.empty
