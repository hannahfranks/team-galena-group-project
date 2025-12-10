import boto3
from botocore.exceptions import ClientError

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


