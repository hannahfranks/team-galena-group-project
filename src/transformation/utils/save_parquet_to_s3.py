import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO
from datetime import datetime

s3_client = boto3.client("s3")

def write_parquet_to_s3(df: pd.DataFrame, bucket: str, key_prefix: str):
    if df.empty:
        print("DataFrame is empty. Skipping Parquet write.")
        return

    # Timestamped path
    timestamp = datetime.now().strftime("%d_%m_%Y_%H:%M:%S")

    # Convert DataFrame → Parquet in memory
    buffer = BytesIO()
    table = pa.Table.from_pandas(df)
    pq.write_table(table, buffer)
    buffer.seek(0)

    # Upload to S3
    s3_client.put_object(
        Bucket=bucket,
        Key=f"{key_prefix}_{timestamp}.parquet",
        Body=buffer.getvalue(),
        ContentType="application/octet-stream"
    )