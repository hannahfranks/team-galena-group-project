import pandas as pd
import requests

DF_DESIGN_COLUMNS = [
    "currency_id",
    "currency_code",
    "created_at",
    "last_updated"
]

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
        lower_dict = {k.upper(): v.lower() for k, v in currencies_dict.items()}
        return lower_dict
    except Exception as e:
        print(e.message, e.args)

# function to create dim_currency from df_currency 
def transform_dim_currency(currency: pd.DataFrame) -> pd.DataFrame:
 
    # create dim_currency df and add empty 'currency_name' column
    dim_currency = currency[
        [
            "currency_id",
            "currency_code"
        ]
    ].copy()

    # convert currency_id to numeric
    dim_currency["currency_id"] = pd.to_numeric(dim_currency["currency_id"])
    
    # only keep unique currency_code rows to avoid duplicates
    dim_currency = (dim_currency.drop_duplicates(subset=["currency_code"]))
    
    # generate currency_name column based on currency_code
    currencies = get_currencies()
    # check for and handle invalid currency codes
    invalid_codes = set(dim_currency["currency_code"]) - set(currencies.keys())
    if invalid_codes:
        raise ValueError(f"Invalid currency code: {invalid_codes}")
    dim_currency["currency_code"] = dim_currency["currency_code"].str.upper() # convert currency_code to uppercase
    dim_currency["currency_name"] = dim_currency["currency_code"].map(currencies) # map names to codes

    # ensure correct column order
    dim_currency = dim_currency[DIM_CURRENCY_COLUMNS]

    return dim_currency 
