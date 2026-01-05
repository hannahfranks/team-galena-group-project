import pandas as pd
import re


# Function to ensures consistent naming across schema
def clean_counterparty_name(name: str) -> str:
    if not isinstance(name, str):
        return None

    name = name.strip()
    name = re.sub(r"\s+", " ", name)        # collapse spaces
    name = name.upper()                     # standard case

    # standardise legal suffixes
    replacements = {
        r"\bLIMITED\b": "LTD",
        r"\bLIMITED LIABILITY COMPANY\b": "LLC",
        r"\bPUBLIC LIMITED COMPANY\b": "PLC",
        r"\bCORPORATION\b": "CORP",
        r"\bINCORPORATED\b": "INC",
    }

    for pattern, repl in replacements.items():
        name = re.sub(pattern, repl, name)

    return name

DIM_COUNTERPARTY_COLUMNS = [
    "counterparty_id",
    "counterparty_legal_name",
    "counterparty_legal_address_line_1",
    "counterparty_legal_address_line_2",
    "counterparty_legal_district",
    "counterparty_legal_city",
    "counterparty_legal_postal_code",
    "counterparty_legal_country",
    "counterparty_legal_phone_number"  
]

def transform_dim_counterparty(df_counterparty: pd.DataFrame, df_address: pd.DataFrame) -> pd.DataFrame:
    if df_counterparty.empty or df_address.empty:
        return pd.DataFrame(columns=DIM_COUNTERPARTY_COLUMNS)
    
    df_counterparty = df_counterparty[
        [
            "counterparty_id",
            "counterparty_legal_name",
            "legal_address_id" 
        ]
    ].copy 

    df_address = df_address[
        [
            "address_id",
            "address_line_1",
            "address_line_2",
            "district",
            "city",
            "postal_code",
            "country",
            "phone"
        ]
    ].copy

    df_merged = df_counterparty.merge(
        df_address,
        left_on="legal_address_id",
        right_on="address_id",
        how="left",
        validate="many_to_one"
    ).drop(columns=["address_id", "legal_address_id"])

    #standardise counterparty names
    df_merged["counterparty_legal_name"] = df_merged["counterparty_legal_name"].apply(
        clean_counterparty_name
    )

    df_merged = df_merged.rename(columns={
    "address_line_1": "counterparty_legal_address_line_1",
    "address_line_2": "counterparty_legal_address_line_2",
    "district": "counterparty_legal_district",
    "city": "counterparty_legal_city",
    "postal_code": "counterparty_legal_postal_code",
    "country": "counterparty_legal_country",
    "phone": "counterparty_legal_phone_number",
    })
    #DIM_COUNTERPARTY = DIM_COUNTERPARTY.rename(columns=rename_map)
    df_merged = df_merged[DIM_COUNTERPARTY_COLUMNS]

    return df_merged
    
