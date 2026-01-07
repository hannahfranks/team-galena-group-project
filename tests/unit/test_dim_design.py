from src.transformation.dim_design import transform_dim_design
import pandas as pd
import pytest

# test 1
def test_transform_dim_design_returns_pd_df():
    # sample ingested design table
    d = {
        "design_id": [1, 2, 3],
        "created_at": ["2022-11-03 14:20:49.962", "2023-11-28 09:51:09.985", "2025-10-10 09:58:09.712"],
        "design_name": ["Plastic", "Concrete", "Wooden"],
        "file_location": ["/test", "/test/xyz", "/hello/test"],
        "file_name": ["test1.json", "test2.json", "test3.json"],
        "last_updated": ["2023-01-14 09:14:09.775", "2024-01-16 09:14:09.775", "2025-11-16 09:14:09.775"]
    }
    design = pd.DataFrame(data=d)
    result = transform_dim_design(design)
    assert isinstance(result, pd.DataFrame)

# test 2
def test_transform_dim_design_returns_df_with_empty_columns_if_passed_empty_df():
    # empty design table
    design = pd.DataFrame()
    result = transform_dim_design(design)
    assert list(result) == ["design_id", "design_name", "file_location", "file_name"]
    assert result.empty

# test 3
def test_transform_dim_design_returns_correct_num_of_rows():
    d = {
        "design_id": [1, 2, 3],
        "created_at": ["2022-11-03 14:20:49.962", "2023-11-28 09:51:09.985", "2025-10-10 09:58:09.712"],
        "design_name": ["Plastic", "Concrete", "Wooden"],
        "file_location": ["/test", "/test/xyz", "/hello/test"],
        "file_name": ["test1.json", "test2.json", "test3.json"],
        "last_updated": ["2023-01-14 09:14:09.775", "2024-01-16 09:14:09.775", "2025-11-16 09:14:09.775"]
    }
    design = pd.DataFrame(data=d)
    result = transform_dim_design(design)
    assert result.shape == (3,4)

# test 4
def test_transform_dim_design_standardises_design_name():
    d = {
        "design_id": [1, 2, 3],
        "created_at": ["2022-11-03 14:20:49.962", "2023-11-28 09:51:09.985", "2025-10-10 09:58:09.712"],
        "design_name": ["plastic cHair", "CONCreTe", "  Wooden"],
        "file_location": ["/test", "/test/xyz", "/hello/test"],
        "file_name": ["test1.json", "test2.json", "test3.json"],
        "last_updated": ["2023-01-14 09:14:09.775", "2024-01-16 09:14:09.775", "2025-11-16 09:14:09.775"]
    }
    design = pd.DataFrame(data=d)
    result = transform_dim_design(design)
    assert result["design_name"].to_list() == ['Plastic Chair', 'Concrete', 'Wooden']

# test 5
def test_transform_dim_design_catches_missing_values():
    d = {
        "design_id": [1, 2, 3],
        "created_at": ["", "2023-11-28 09:51:09.985", "2025-10-10 09:58:09.712"],
        "design_name": ["Plastic", "Concrete", "Wooden"],
        "file_location": ["/test", "/test/xyz", "/hello/test"],
        "file_name": ["test1.json", None, "test3.json"],
        "last_updated": ["2023-01-14 09:14:09.775", "2024-01-16 09:14:09.775", "2025-11-16 09:14:09.775"]
    }
    design = pd.DataFrame(data=d)
    with pytest.raises(ValueError):
        transform_dim_design(design)


