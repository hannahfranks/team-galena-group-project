import pandas as pd

DIM_STAFF_COLUMNS = [
    "staff_id",
    "first_name",
    "last_name",
    "department_name",
    "location",
    "email_address"
]

def transform_dim_staff(df_staff: pd.DataFrame, df_department: pd.DataFrame) -> pd.DataFrame:
    if df_staff.empty or df_department.empty:
        return pd.DataFrame(columns=DIM_STAFF_COLUMNS)
    
    df_staff = df_staff[
        [ 
            "staff_id",
            "first_name",
            "last_name",
            "department_id",
            "email_address"
        ]
    ].copy()
    
    df_department = df_department[
        [
            "department_id",
            "department_name",
            "location"
        ]
    ].copy()
    
# merge data tables based on department id (pk)
    df_merged = df_staff.merge(
        df_department,
        on="department_id",
        how="left"
    )

    df_staff = df_merged[DIM_STAFF_COLUMNS]

    return df_staff
        