import pandas as pd
from datetime import date

DIM_DATE_COLUMNS = [
    "date_id",
    "year",
    "month",
    "day",
    "day_of_week",
    "day_name",
    "month_name",
    "quarter",
]

def build_dim_date(start_date: str = "2000-01-01",end_date: str | None = None) -> pd.DataFrame:

    if end_date is None:
        end_date = date.today().isoformat()

    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    df = pd.DataFrame({"date_id": dates.date})

    df["year"] = dates.year
    df["month"] = dates.month
    df["day"] = dates.day
    df["day_of_week"] = dates.weekday + 1  # Mon=1
    df["day_name"] = dates.strftime("%A")
    df["month_name"] = dates.strftime("%B")
    df["quarter"] = dates.quarter

    return df[DIM_DATE_COLUMNS]