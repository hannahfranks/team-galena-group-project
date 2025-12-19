import pandas as pd
from src.transformation.utils.parser import attach_columns_to_dataframe

DF_DESIGN_COLUMNS = [
    "design_id",
    "created_at",
    "design_name",
    "file_location",
    "file_name",
    "last_updated"
]

DIM_DESIGN_COLUMNS = [
    "design_id",
    "design_name",
    "file_location",
    "file_name"
]

def transform_dim_design(design: pd.DataFrame) -> pd.DataFrame:

    # attach column names to design df
    df_design = attach_columns_to_dataframe(design, DF_DESIGN_COLUMNS)

    # select columns from df_design for dim_design 
    dim_design = df_design[DIM_DESIGN_COLUMNS].copy()

    # standardise design_name values - capitalised and no leading and trailing whitespaces
    dim_design["design_name"] = dim_design["design_name"].str.strip().str.title()
    
    return dim_design



