import pandas as pd
from typing import List

def attach_columns_to_dataframe(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:

    if df.empty:
        return pd.DataFrame(columns=columns)

    if df.shape[1] != len(columns):
        raise ValueError(
            f"Column count mismatch: "
            f"DataFrame has {df.shape[1]} columns, "
            f"but {len(columns)} column names were provided"
        )
        
    df = df.copy()
    df.columns = columns
    return df

