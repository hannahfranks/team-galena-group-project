import pandas as pd
import pytest
from src.transformation.dim_staff import transform_dim_staff, DIM_STAFF_COLUMNS

def test_transform_dim_staff():
    # sample staff data
    df_staff = pd.DataFrame({
        "staff_id": [101, 102],
        "first_name": ["Alice", "Bob"],
        "last_name": ["Johnson", "Smith"],
        "department_id": [1, 2],
        "email_address": ["alice.johnson@company.com", "bob.smith@company.com"]
    })
    # sample department data
    df_department = pd.DataFrame({
        "department_id": [1, 2],
        "department_name": ["Human Resources", "Engineering"],
        "location": ["New York", "San Francisco"]
    })
    
    expected_columns = {
        "staff_id": [101, 102],
        "first_name": ["Alice", "Bob"],
        "last_name": ["Johnson", "Smith"],
        "department_name": ["Human Resources", "Engineering"],
        "location": ["New York", "San Francisco"],
        "email_address": ["alice.johnson@company.com", "bob.smith@company.com"]
    }

    df_merged = transform_dim_staff(df_staff, df_department)
    assert set(df_merged.columns) == set(DIM_STAFF_COLUMNS) #Ensure all expected columns exist and no extras slipped in
    assert len(df_merged) == len(df_staff) # row count test / left join should not change the number of staff rows
    #assert df_merged["department_name"].is_unique # department_id must be unique in department table
    assert df_merged["staff_id"].is_unique # staff_id must be unique in merged table 
    #assert df_merged["department_id"].notnull().all() # no missing department_id's in merged table 