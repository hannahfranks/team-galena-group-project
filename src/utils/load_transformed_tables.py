import boto3
import pandas as pd
from io import BytesIO

s3 = boto3.client("s3")
BUCKETNAME = 's3-transformation-bucket-team-galena'

# util function to get timestamp of most recent transformation
def get_timestamp(table: str) -> pd.DataFrame:
    
    response = s3.get_object(Bucket=BUCKETNAME, Key='transformation/last_transformation_timestamps.txt')
    timestamps = response['Body'].read().decode('utf-8')

    lines = [line.strip() for line in timestamps.splitlines() if line.strip()] # split into lines

    table_timestamp = [line for line in lines if line.startswith(f"{table}_")] # find timestamp for specific table

    if not table_timestamp:
        raise ValueError(f"No timestamp found for: {table}")

    return table_timestamp[0]

# util function to read in tables after transformation
def read_dimension_table(table: str) -> pd.DataFrame:

    timestamp = get_timestamp(table)

    response = s3.get_object(Bucket=BUCKETNAME, Key=f"{timestamp}.parquet") # get most recent transformation file for table

    table_data = BytesIO(response["Body"].read())

    return pd.read_parquet(table_data) # read in parquet file

