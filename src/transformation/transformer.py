from src.transformation.dim_location import transform_dim_location
from src.transformation.utils.save_parquet_to_s3 import write_parquet_to_s3

import pandas as pd

df_address = pd.DataFrame({
    "address_id": [1],
    "address_line_1": ["123 High St"],
    "address_line_2": [None],
    "district": ["Central"],
    "city": ["London"],
    "postal_code": ["E1 6AN"],
    "country": ["UK"],
    "phone": ["0123456789"],
    "created_at": ["2024-01-01"],
    "last_updated": ["2024-01-02"],
})

df_location = transform_dim_location(df_address)

write_parquet_to_s3(
    df_location,
    bucket="s3-transformation-bucket-team-galena",
    key_prefix="dim_location"
)