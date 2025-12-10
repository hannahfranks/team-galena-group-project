import boto3
from botocore.exceptions import ClientError
import json
import pg8000

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
    conn = pg8000.connect(
        user=credentials["username"], 
        password=credentials["password"], 
        host=credentials["host"],
        database=credentials["database"],
        port=credentials["port"]
    )
    return conn

# function to close connection
def close_conn(conn):
    conn.close()

# function to get table names from db
def get_table_names():
    return [
        "counterparty", 
        "currency", 
        "department", 
        "design", 
        "staff", 
        "sales_order", 
        "address", 
        "payment", 
        "purchase_order", 
        "payment_type", 
        "transaction"
        ]




