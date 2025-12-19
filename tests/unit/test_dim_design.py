from src.transformation.dim_design import transform_dim_design
import pandas as pd

# test 1
def test_transform_dim_design_returns_pd_df():
    # sample ingested currency table
    design = pd.DataFrame([
        [1, 2, 3],
        ["2022-11-03 14:20:49.962", "2023-11-28 09:51:09.985", "2025-10-10 09:58:09.712"],
        ["Plastic", "Concrete", "Wooden"],
        ["/test", "/test/xyz", "/hello/test"],
        ["test1.json", "test2.json", "test3.json"],
        ["2023-01-14 09:14:09.775", "2024-01-16 09:14:09.775", "2025-11-16 09:14:09.775"]
    ]).T
    result = transform_dim_design(design)
    assert isinstance(result, pd.DataFrame)
   


