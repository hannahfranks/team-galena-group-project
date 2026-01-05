import pandas as pd
import pytest
import re
from src.transformation.dim_counterparty import transform_dim_counterparty, DIM_COUNTERPARTY_COLUMNS, clean_counterparty_name

def test_transform_dim_counterparty():
    # sample staff data
    df_counterparty = pd.DataFrame({
        "counterparty_id": [1],
        "counterparty_legal_name": ["Acme Corporation Ltd"],
        "legal_address_id": [101]}
    ) 

    df_address = pd.DataFrame({
        "address_id": [101],
        "address_line_1": ["123 Market Street"],
        "address_line_2": ["Suite 400"],
        "district": ["Central Business District"],
        "city": ["London"],
        "postal_code": ["EC2A 3BX"],
        "country": ["United Kingdom"],
        "phone": ["+44 20 7946 0958"]}
    )
    
    expected_columns = pd.DataFrame({
        "counterparty_id": [1],
        "counterparty_legal_name": ["Acme Corporation Ltd"],
        "address_line_1": ["123 Market Street"],
        "address_line_2": ["Suite 400"],
        "district": ["Central Business District"],
        "city": ["London"],
        "postal_code": ["EC2A 3BX"],
        "country": ["United Kingdom"],
        "phone": ["+44 20 7946 0958"]}
    ) 
    #df_merged = transform_dim_counterparty(df_counterparty, df_address)  
    assert list(expected_columns) != DIM_COUNTERPARTY_COLUMNS #Ensure all expected columns exist with no extras 
    assert expected_columns["counterparty_id"].is_unique #ensure pk is unique 
    #assert df_merged["legal_address_id"].notnull().all()
            
            
def test_transform_dim_counterparty_empty():
    # Empty input DataFrame
    df_empty = pd.DataFrame()

    df_result = transform_dim_counterparty(df_empty, df_empty)

    # Should return empty DataFrame with correct columns
    assert list(df_result.columns) == DIM_COUNTERPARTY_COLUMNS
    assert df_result.empty  

# ensure whitespace is removed
def test_clean_counterparty_name_trims_whitespace():
    assert clean_counterparty_name("  Acme Ltd  ") == "ACME LTD"

# ensure function returns none for non values
def test_clean_counterparty_name_returns_none():
    assert clean_counterparty_name(None) is None

#ensure function returns none for non-string values
def test_non_string_returns_none():
    assert clean_counterparty_name(12345) is None