import pandas as pd

DIM_CURRENCY_COLUMNS = [
    "currency_id",
    "currency_code",
    "currency_name"
]

def transform_dim_currency(df_currency: pd.DataFrame) -> pd.DataFrame:

    # return empty dim_currency columns whens passed empty df_currency
    if df_currency.empty:
        return pd.DataFrame(columns=DIM_CURRENCY_COLUMNS)
    
    # create dim_currency df and add empty 'currency_name' column
    dim_currency = df_currency[
        [
            "currency_id",
            "currency_code"
        ]
    ].copy()
    dim_currency["currency_name"] = None

    return dim_currency 


