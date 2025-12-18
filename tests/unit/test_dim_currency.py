import pandas as pd
from src.transformation.dim_currency import transform_dim_currency

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

def test_transform_dim_currency_returns_df_with_columns_if_passed_empty_df():
    # empty currency table
    currency = pd.DataFrame()
    result = transform_dim_currency(currency)
    assert list(result) == ["currency_id", "currency_code", "currency_name"]
    assert result["currency_id"].to_list() == []
    assert result["currency_code"].to_list() == []
    assert result["currency_name"].to_list() == []




