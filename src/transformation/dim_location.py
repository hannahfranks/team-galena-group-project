import pandas as pd


DIM_LOCATION_COLUMNS = [
    "location_id",
    "address_line_1",
    "address_line_2",
    "district",
    "city",
    "postal_code",
    "country",
    "phone",
]

def transform_dim_location(df_address: pd.DataFrame) -> pd.DataFrame:

    if df_address.empty:
        return pd.DataFrame(columns=DIM_LOCATION_COLUMNS)

    df_location = df_address[
        [
            "address_id",
            "address_line_1",
            "address_line_2",
            "district",
            "city",
            "postal_code",
            "country",
            "phone",
        ]
    ].copy()

    # Rename PK to warehouse-friendly name
    df_location = df_location.rename(
        columns={"address_id": "location_id"}
    )

    # Ensure correct column order
    df_location = df_location[DIM_LOCATION_COLUMNS]

    return df_location
