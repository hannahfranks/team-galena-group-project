import pandas as pd
import requests

DIM_CURRENCY_COLUMNS = [
    "currency_id",
    "currency_code",
    "currency_name"
]

# function to get dict of currencies from api 
def get_currencies():
    try:
        response = requests.get("https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json")
        currencies_dict = response.json()
        print(requests.__version__)
        lower_dict = {k.lower(): v.lower() for k, v in currencies_dict.items()}
        return lower_dict
    except Exception as e:
        print(e.message, e.args)

# function to create dim_currency from df_currency 
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

    # convert currency_code to lowercase
    dim_currency["currency_code"] = dim_currency["currency_code"].str.lower() 
    
    # only keep unique currency_code rows to avoid duplicates
    dim_currency = (dim_currency.drop_duplicates(subset=["currency_code"]))
    
    # generate currency_name column based on currency_code
    currencies = get_currencies()
    # check for and handle invalid currency codes
    invalid_codes = set(dim_currency["currency_code"]) - set(currencies.keys())
    if invalid_codes:
        raise ValueError(f"Invalid currency code: {invalid_codes}")
    dim_currency["currency_code"] = dim_currency["currency_code"].str.lower() # convert currency_code to lowercase
    dim_currency["currency_name"] = dim_currency["currency_code"].map(currencies) # map names to codes

    return dim_currency 

