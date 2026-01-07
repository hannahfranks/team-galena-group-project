import logging
import json
import os
import traceback
import boto3
import sys
from urllib.parse import unquote_plus
from src.transformation.transformer import main_transformer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns_client = boto3.client("sns")

SNS_TOPIC_ARN = os.environ.get("SNS_ALERT_TOPIC_ARN")
FILE_NAME = os.path.basename(__file__)


def send_sns_alert(subject: str, message: str):
    if not SNS_TOPIC_ARN:
        logger.error("SNS_ALERT_TOPIC_ARN not set")
        return

    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message
    )

def extract_s3_info(event):
    #Extract bucket name and object key(s) from an S3-triggered event.Returns a list of (bucket, key) tuples.
    s3_objects = []

    try:
        records = event.get("Records", [])
        for record in records:
            if record.get("eventSource") == "aws:s3":
                bucket = record["s3"]["bucket"]["name"]
                key = unquote_plus(record["s3"]["object"]["key"])
                s3_objects.append((bucket, key))
    except Exception as e:
        logger.warning("Failed to extract S3 info: %s", str(e))

    return s3_objects

def transform_data():
    #transformation logic
    main_transformer()

def lambda_handler(event, context):
    logger.info("Transformation Lambda triggered")
    logger.info(event)
    #logger.info("Incoming event: %s", json.dumps(event))

    s3_objects = extract_s3_info(event)

    if s3_objects:
        for bucket, key in s3_objects:
            logger.info("Detected input file: s3://%s/%s", bucket, key)
    else:
        logger.info("No S3 input file detected")

    try:
        transform_data()

        logger.info("Transformation successful")

        return {
            "statusCode": 200,
            "body": json.dumps({
                    "message": "Transformation successful",
                    "processed_files": [
                    f"s3://{bucket}/{key}" for bucket, key in s3_objects
                ]
                })
        }

    except Exception as e:
        error_message = str(e)
        stack_trace = traceback.format_exc()

        logger.error("Transformation failed")
        logger.error("Error: %s", error_message)
        logger.error("Stack trace:\n%s", stack_trace)

        s3_file_list = (
            "\n".join([f"s3://{b}/{k}" for b, k in s3_objects])
            if s3_objects else "N/A"
        )

        sns_message = (
            f"🚨 Lambda Transformation Failure 🚨\n\n"
            f"File: {FILE_NAME}\n"
            f"Function: {context.function_name}\n"
            f"Request ID: {context.aws_request_id}\n\n"
            f"S3 Input File(s):\n{s3_file_list}\n\n"
            f"Error Message:\n{error_message}\n\n"
            f"Stack Trace:\n{stack_trace}"
        )

        send_sns_alert(
            subject="Lambda Transformation Failure",
            message=sns_message
        )

        # Re-raise so Lambda marks the execution as failed
        raise
    # perform transformations and upload to S3 transformation bucket 
    

    return {
        "statusCode": 200,
    }

if __name__ == "__main__":
    lambda_handler("test", "")
