import pandas as pd

FACT_SALES_ORDER_COLUMNS = [
    "sales_order_id",
    "created_date",
    "created_time",
    "last_updated_date",
    "last_updated_time",
    "sales_staff_id",
    "counterparty_id",
    "units_sold",
    "unit_price",
    "currency_id",
    "design_id",
    "agreed_payment_date",
    "agreed_delivery_date",
    "agreed_delivery_location_id",
]

def transform_fact_sales_order(df_sales_order: pd.DataFrame) -> pd.DataFrame:
    
    if df_sales_order.empty:
        return pd.DataFrame(columns=FACT_SALES_ORDER_COLUMNS)

    df = df_sales_order.copy()

    # Convert timestamps
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["last_updated"] = pd.to_datetime(df["last_updated"])

    # Split timestamps
    df["created_date"] = df["created_at"].dt.date
    df["created_time"] = df["created_at"].dt.time
    df["last_updated_date"] = df["last_updated"].dt.date
    df["last_updated_time"] = df["last_updated"].dt.time

    # Convert string dates
    df["agreed_payment_date"] = pd.to_datetime(
        df["agreed_payment_date"]
    ).dt.date

    df["agreed_delivery_date"] = pd.to_datetime(
        df["agreed_delivery_date"]
    ).dt.date

    df = df.rename(columns={
        "staff_id": "sales_staff_id"
    })

    # Select columns
    df_fact = df[FACT_SALES_ORDER_COLUMNS]

    return df_fact
