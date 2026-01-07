from src.transformation.dim_location import transform_dim_location
from src.transformation.utils.save_parquet_to_s3 import write_parquet_to_s3
from src.transformation.dim_staff import transform_dim_staff
from src.transformation.dim_counterparty import transform_dim_counterparty
from src.transformation.dim_date import build_dim_date
from src.transformation.dim_design import transform_dim_design
from src.transformation.dim_currency import transform_dim_currency
from src.transformation.dim_fact_sales import transform_fact_sales_order
from datetime import datetime, timezone

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

# function to write timestamps of most recent transformation for each table to txt file in S3 bucket
def save_transformation_timestamps(table_timestamps):

    s3_key = "transformation/last_transformation_timestamps.txt" # path to upload timestamps to s3
    local_path = "src/transformation/last_transformation_timestamps.txt" # path to save timestamps locally for quick access

    # create timestamps content
    content = "\n".join(
        f"{table}_{timestamp}"
        for table, timestamp in table_timestamps.items()
    )

    # write to local file
    with open(local_path, "w") as f:
        f.write(content)

    # write to s3 
    s3.put_object(
        Bucket="s3-transformation-bucket-team-galena",
        Key=s3_key,
        Body=content.encode("utf-8")
    )

def main_transformer():
    
    transformation_timestamps = {}

    #dim location
    #get data from ingestion layer
    df_address = read_most_recent_ingestion("address")
    #transform 
    dim_location = transform_dim_location(df_address)
    #save to s3
    location_filename = write_parquet_to_s3(
        dim_location,
        bucket="s3-transformation-bucket-team-galena",
        key_prefix="dim_location"
    )
    transformation_timestamps["dim_location"] = location_filename

    #dim staff
    df_staff = read_most_recent_ingestion("staff")
    df_department = read_most_recent_ingestion("department")

    dim_staff = transform_dim_staff(df_staff, df_department)

    staff_filename = write_parquet_to_s3(
        dim_staff, 
        bucket="s3-transformation-bucket-team-galena",
        key_prefix="dim_staff"
    )
    transformation_timestamps["dim_staff"] = staff_filename
    
    #dim counterparty
    df_counterparty = read_most_recent_ingestion("counterparty")
    df_address = read_most_recent_ingestion("address")

    dim_counterparty = transform_dim_counterparty(df_counterparty, df_address)

    counterparty_filename = write_parquet_to_s3(
        dim_counterparty, 
        bucket="s3-transformation-bucket-team-galena",
        key_prefix="dim_counterparty"
    )
    transformation_timestamps["dim_counterparty"] = counterparty_filename
    
    # dim_date
    dim_date = build_dim_date()

    date_filename = write_parquet_to_s3(
        dim_date,
        bucket="s3-transformation-bucket-team-galena",
        key_prefix="dim_date"
    )
    transformation_timestamps["dim_date"] = date_filename

    # sales fact table 
    df_sales = read_most_recent_ingestion('sales_order')
    fact_sales = transform_fact_sales_order(df_sales)
    fact_sales_filename = write_parquet_to_s3(
        fact_sales,
        bucket="s3-transformation-bucket-team-galena",
        key_prefix="fact_sales_order"
    )
    transformation_timestamps["fact_sales"] = fact_sales_filename

    # dim currency
    df_currency = read_most_recent_ingestion("currency")
    dim_currency = transform_dim_currency(df_currency)

    currency_filename = write_parquet_to_s3(
        dim_currency,
        bucket="s3-transformation-bucket-team-galena",
        key_prefix="dim_currency"
    )
    transformation_timestamps["dim_currency"] = currency_filename
    
    # dim design
    df_design = read_most_recent_ingestion("design")
    dim_design = transform_dim_design(df_design)

    design_filename = write_parquet_to_s3(
        dim_design,
        bucket="s3-transformation-bucket-team-galena",
        key_prefix="dim_design"
    )
    transformation_timestamps["dim_design"] = design_filename

    # overwrite transformation timestamps text file with most recent timestamps
    save_transformation_timestamps(transformation_timestamps)

