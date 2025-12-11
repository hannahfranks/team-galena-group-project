import boto3
from botocore.exceptions import ClientError
import json
from pg8000.native import Connection

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

# function to get table names from db
def get_table_names(conn, credentials):
    
    credentials = get_secret()
    conn = db_connection(credentials)

    query = """
        SELECT table_name 
        FROM information_schema.tables
        WHERE table_schema='public'
    """
    result = conn.run(sql=query)

    # convert to list of strings and remove _prisma_migrations
    table_names = []
    for name in result:
        if type(name) is list:
            for item in name:
                table_names.append(item)
    table_names.remove('_prisma_migrations')
    return table_names






