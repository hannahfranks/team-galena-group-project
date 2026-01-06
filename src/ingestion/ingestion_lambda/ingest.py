import boto3
from botocore.exceptions import ClientError
import json
from pg8000.native import Connection

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO
from datetime import datetime

s3 = boto3.client("s3")

# function to get db credentials from aws secrets manager
def get_secret():

    secret_name = "totesys/rds/credentials"
    region_name = "eu-west-2"

    # create Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    
    secret = get_secret_value_response['SecretString']
    credentials = json.loads(secret)

    return credentials

# function to create db connection
def db_connection(credentials):
    conn = Connection(
        user=credentials["username"], 
        password=credentials["password"], 
        host=credentials["host"],
        database=credentials["dbname"],
        port=credentials["port"]
    )
    return conn

# function to close connection
def close_conn(conn):
    conn.close()

# function to get list of table names from db
def get_table_names(conn):
    
    query = """
        SELECT table_name 
        FROM information_schema.tables
        WHERE table_schema='public';
    """
    result = conn.run(query)

    # convert to list of strings and remove _prisma_migrations
    table_names = []
    for name in result:
        if type(name) is list:
            for item in name:
                table_names.append(item)
    table_names.remove('_prisma_migrations')
    return table_names

# function to extract data from each table
# use parameterized query to avoid sql injection
def extract_table_data(table_names, conn):

    data = {}
    for table_name in table_names:
        query = f"SELECT * FROM {table_name}"
        result = conn.run(query)
        data[table_name] = result

    return data

# function to write timestamps of most recent ingestion for each table to txt file in S3 bucket
def save_ingestion_timestamps(table_timestamps):

    s3_key = "ingestion/last_ingestion_timestamps.txt" # path to upload timestamps to s3
    local_path = "src/ingestion/last_ingestion_timestamps.txt" # path to save timestamps locally for quick access

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
        Bucket="s3-ingestion-bucket-team-galena",
        Key=s3_key,
        Body=content.encode("utf-8")
    )

# function to write tables to s3 
def save_tables_as_parquet(tables_data, bucket_name):
    
    table_timestamps = {}

    for table_name, rows in tables_data.items():
        if not rows:
            continue
       
        # Convert result rows to a DataFrame
        df = pd.DataFrame(rows)

        # Create timestamp for table
        timestamp = datetime.now().strftime("%d_%m_%Y_%H:%M:%S")
        table_timestamps[table_name] = timestamp
        
        # Convert to Parquet in memory
        table = pa.Table.from_pandas(df)
        buffer = BytesIO()
        pq.write_table(table, buffer)

        # Upload to S3
        s3.put_object(
            Bucket=bucket_name,
            Key=f"{table_name}_{timestamp}.parquet",
            Body=buffer.getvalue(),
            ContentType="application/octet-stream"
        )

    # Overwrite timestamps of current ingestion to ingestion/last_ingestion_timestamps S3 object 
    save_ingestion_timestamps(table_timestamps)

# lambda handler to execute ingestion process
def lambda_handler(event, context):
    
    # get the db secrets from aws secret manager
    credentials = get_secret()

    # connect to db
    conn = db_connection(credentials)

    # get all the table names 
    table_names = get_table_names(conn)

    # extract data from all the tables and return a dictionary of tables
    tables_data = extract_table_data(table_names, conn)

    # transform data to parquet and save to s3
    save_tables_as_parquet(tables_data, "s3-ingestion-bucket-team-galena") 

    # close db connection
    close_conn(conn) 

lambda_handler('test', '')

