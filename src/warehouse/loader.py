import logging
import boto3
from botocore.exceptions import ClientError
import json
from pg8000.native import Connection

logger = logging.getLogger(__name__)

class WarehouseLoader:
    def __init__(self):
        self.conn = None

    def get_secret(self):
        secret_name = "warehouse"
        region_name = "eu-west-2"

        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager",
            region_name=region_name
        )

        try:
            response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            logger.error("Failed to retrieve secret")
            raise e

        return json.loads(response["SecretString"])

    def get_connection(self):
        credentials = self.get_secret()

        self.conn = Connection(
            user=credentials["username"],
            password=credentials["password"],
            host=credentials["host"],
            database=credentials["dbInstanceIdentifier"],
            port=credentials["port"]
        )

        logger.info("Warehouse DB connected")
        return self.conn

    def close_conn(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info("Warehouse DB connection closed")

