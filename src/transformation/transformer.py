from src.transformation.dim_location import transform_dim_location
from src.transformation.utils.save_parquet_to_s3 import write_parquet_to_s3
from src.transformation.dim_staff import transform_dim_staff
from src.transformation.dim_counterparty import transform_dim_counterparty
from src.transformation.dim_date import build_dim_date

import boto3
import pandas as pd
from io import BytesIO

s3 = boto3.client("s3")
BUCKETNAME = 's3-ingestion-bucket-team-galena'

# util function to get timestamp of most recent ingestion
def get_timestamp(table: str) -> pd.DataFrame:
    
    response = s3.get_object(Bucket=BUCKETNAME, Key='ingestion/last_ingestion_timestamps.txt')
    timestamps = response['Body'].read().decode('utf-8')

    lines = [line.strip() for line in timestamps.splitlines() if line.strip()] # split into lines

    table_timestamp = [line for line in lines if line.startswith(f"{table}_")] # find timestamp for specific table

    if not table_timestamp:
        raise ValueError(f"No timestamp found for: {table}")

    return table_timestamp[0]

# util function to read in most recent data for ingested table
def read_most_recent_ingestion(table: str) -> pd.DataFrame:

    timestamp = get_timestamp(table)

    response = s3.get_object(Bucket=BUCKETNAME, Key=f"{timestamp}.parquet") # get most recent ingestion file for table

    table_data = BytesIO(response["Body"].read())

    return pd.read_parquet(table_data) # read in parquet file


# Transformation for dim_location
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

# transformation for dim_staff
df_staff = pd.DataFrame({
    "staff_id": [101, 102],
    "first_name": ["Alice", "Bob"],
    "last_name": ["Johnson", "Smith"],
    "department_id": [1, 2],
    "email_address": ["alice.johnson@company.com", "bob.smith@company.com"]
})

df_department = pd.DataFrame({
    "department_id": [1, 2],
    "department_name": ["Human Resources", "Engineering"],
    "location": ["New York", "San Francisco"]
})

dim_staff = transform_dim_staff(df_staff, df_department)

write_parquet_to_s3(
    dim_staff, 
    bucket="s3-transformation-bucket-team-galena",
    key_prefix="dim_staff"
)

# transformation for dim_counterparty
df_counterparty = pd.DataFrame({
    "counterparty_id": [1],
    "counterparty_legal_name": ["Acme Corporation Ltd"],
    "legal_address_id": [101]
})        

df_address = pd.date_range({
    "address_id": [101],
    "address_line_1": ["123 Market Street"],
    "address_line_2": ["Suite 400"],
    "district": ["Central Business District"],
    "city": ["London"],
    "postal_code": ["EC2A 3BX"],
    "country": ["United Kingdom"],
    "phone": ["+44 20 7946 0958"]
})

dim_counterparty = transform_dim_counterparty(df_counterparty, df_address)

write_parquet_to_s3(
    dim_counterparty, 
    bucket="s3-transformation-bucket-team-galena",
    key_prefix="dim_counterparty"
)
# dim_date
df_dim_date = build_dim_date()

write_parquet_to_s3(
    df_dim_date,
    bucket="s3-transformation-bucket-team-galena",
    key_prefix="dim_date"
)

df_fact_sales = read_most_recent_ingestion('sales_order')
write_parquet_to_s3(
    df_fact_sales,
    bucket="s3-transformation-bucket-team-galena",
    key_prefix="fact_sales_order"
)