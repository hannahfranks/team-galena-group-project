import pandas as pd
import requests

DIM_CURRENCY_COLUMNS = [
    "currency_id",
    "currency_code",
    "currency_name"
]

def get_currencies():
    try:
        response = requests.get("https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json")
        currencies_dict = response.json()
        print(requests.__version__)
        lower_dict = {k.lower(): v.lower() for k, v in currencies_dict.items()}
        return lower_dict
    except Exception as e:
        print(e.message, e.args)

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

    # generate currency_name based on currency_code
    currencies = get_currencies()
    dim_currency["currency_code"] = dim_currency["currency_code"].str.lower() # convert code to lowercase
    dim_currency["currency_name"] = dim_currency["currency_code"].map(currencies) # map names to codes

    return dim_currency 

