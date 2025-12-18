import pandas as pd
import pytest
from src.transformation.dim_currency import transform_dim_currency, get_currencies

# test 1
def test_transform_dim_currency_returns_pd_df_with_correct_columns():
    # sample ingested currency table
    currency = pd.DataFrame({
        "currency_id": [1, 2, 3],
        "currency_code": ["EUR", "GBP", "USD"],
        "created_at": ["2025-10-12", "2025-17-12", "2025-16-12"],
        "last_updated": ["2025-18-12", "2025-18-12", "2025-18-12"]
    })

    result = transform_dim_currency(currency)
    assert isinstance(result, pd.DataFrame)

# test 2
def test_transform_dim_currency_returns_df_with_columns_if_passed_empty_df():
    # empty currency table
    currency = pd.DataFrame()
    result = transform_dim_currency(currency)
    assert list(result) == ["currency_id", "currency_code", "currency_name"]
    assert result.empty

# test 3
def test_transform_dim_currency_returns_correct_data_types():
    # sample ingested currency table
    currency = pd.DataFrame({
        "currency_id": [1, 2, 3],
        "currency_code": ["EUR", "GBP", "USD"],
        "created_at": ["2025-10-12", "2025-17-12", "2025-16-12"],
        "last_updated": ["2025-18-12", "2025-18-12", "2025-18-12"]
    })
    dim_currency = transform_dim_currency(currency)
    data_types = dim_currency.dtypes
    assert data_types["currency_id"] == int
    assert data_types["currency_code"] == 'O'
    assert data_types["currency_name"] == 'O'

# test 4
def test_transform_dim_currency_creates_currency_name_based_on_currency_code():
    # sample ingested currency table
    currency = pd.DataFrame({
        "currency_id": [1, 2, 3],
        "currency_code": ["EUR", "GBP", "USD"],
        "created_at": ["2025-10-12", "2025-17-12", "2025-16-12"],
        "last_updated": ["2025-18-12", "2025-18-12", "2025-18-12"]
    })
    dim_currency = transform_dim_currency(currency)
    assert dim_currency["currency_name"].to_list() == ['euro', 'british pound', 'us dollar']

# test 5
def test_get_currencies_returns_dict_of_lowercase_currencies():
    result = get_currencies()
    assert isinstance(result, dict)
    assert result["eur"] == "euro"

# test 6
def test_transform_dim_currency_returns_no_duplicate_currencies():
    currency = pd.DataFrame({
        "currency_id": [1, 2, 3],
        "currency_code": ["EUR", "EUR", "USD"],
        "created_at": ["2025-10-12", "2025-17-12", "2025-16-12"],
        "last_updated": ["2025-18-12", "2025-18-12", "2025-18-12"]
    })
    dim_currency = transform_dim_currency(currency)
    assert len(dim_currency) == 2
    assert dim_currency["currency_code"].tolist() == ['eur', 'usd']

# test 7
def test_transform_dim_currency_raises_error_for_invalid_currency_code():
    
    currency = pd.DataFrame({
            "currency_id": [1, 2, 3],
            "currency_code": ["X8?", "EUR", "USD"],
            "created_at": ["2025-10-12", "2025-17-12", "2025-16-12"],
            "last_updated": ["2025-18-12", "2025-18-12", "2025-18-12"]
        })
    
    with pytest.raises(Exception):
        transform_dim_currency(currency)

    





