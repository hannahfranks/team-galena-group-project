import boto3
import pandas as pd
from io import BytesIO

s3 = boto3.client("s3")
BUCKETNAME = 's3-ingestion-bucket-team-galena'

# util function to get timestamp of most recent ingestion
def get_timestamp(table):
    
    response = s3.get_object(Bucket=BUCKETNAME, Key='ingestion/last_ingestion_timestamp.txt')
    timestamps = response['Body'].read().decode('utf-8')

    lines = [line.strip() for line in timestamps.splitlines() if line.strip()] # split into lines

    table_timestamp = [line for line in lines if line.startswith(f"{table}_")] # find timestamp for specific table

    if not table_timestamp:
        raise ValueError("No timestamp found for '{table}'")

    return table_timestamp

# function to read in most recent data for ingested table
def read_most_recent_ingestion(table):

    timestamp = get_timestamp(table)

    response = s3.get_object(Bucket=BUCKETNAME, Key=f"{timestamp}.parquet") # get most recent ingestion file for table

    table_data = BytesIO(response["Body"].read())

    return pd.read_parquet(table_data)


