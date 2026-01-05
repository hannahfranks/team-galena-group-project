import pandas as pd
from src.transformation.dim_fact_sales import transform_fact_sales_order

def test_transform_fact_sales_order_happy_path():
    df_sales_order = pd.DataFrame({
        "sales_order_id": [1],
        "created_at": ["2024-01-10 09:30:45"],
        "last_updated": ["2024-01-11 10:15:30"],
        "design_id": [101],
        "staff_id": [12],
        "counterparty_id": [200],
        "units_sold": [5000],
        "unit_price": [3.25],
        "currency_id": [1],
        "agreed_delivery_date": ["2024-02-01"],
        "agreed_payment_date": ["2024-01-20"],
        "agreed_delivery_location_id": [55],
    })

    # Act
    df_fact = transform_fact_sales_order(df_sales_order)

    assert len(df_fact) == 1

    expected_columns = [
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
    assert list(df_fact.columns) == expected_columns

    row = df_fact.iloc[0]

    assert row["sales_order_id"] == 1
    assert row["sales_staff_id"] == 12
    assert row["units_sold"] == 5000
    assert row["unit_price"] == 3.25

    # Date/time split validation
    assert str(row["created_date"]) == "2024-01-10"
    assert str(row["created_time"]) == "09:30:45"
    assert str(row["last_updated_date"]) == "2024-01-11"
    assert str(row["last_updated_time"]) == "10:15:30"

    assert str(row["agreed_payment_date"]) == "2024-01-20"
    assert str(row["agreed_delivery_date"]) == "2024-02-01"
