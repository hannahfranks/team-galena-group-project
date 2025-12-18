from src.transformation.dim_date import build_dim_date

def test_build_dim_date_range():
    df = build_dim_date("2024-01-01", "2024-01-03")

    assert len(df) == 3
    assert df.iloc[0]["date_id"].isoformat() == "2024-01-01"
    assert df.iloc[0]["day_name"] == "Monday"
    assert df.iloc[-1]["quarter"] == 1
