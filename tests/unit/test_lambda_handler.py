import json
import os
import pytest
from src.transformation.lambda_handler import lambda_handler, extract_s3_info


def test_successful_transformation():
    #correct path test
    event = {"data": "event"}
    context = {}
    response = lambda_handler(event, context)
    assert response["statusCode"] == 200

    body = json.loads(response["body"])
    assert body["message"] == "Transformation successful"


#Verify S3 bucket and file name extraction
def test_s3_event_extraction():
    event = {
        "Records": [
            {
                "eventSource": "aws:s3",
                "s3": {
                    "bucket": {"name": "test-bucket"},
                    "object": {"key": "input/test_file.csv"}
                }
            }
        ]
    }
    s3_objects = extract_s3_info(event)

    assert len(s3_objects) == 1
    assert s3_objects[0][0] == "test-bucket"
    assert s3_objects[0][1] == "input/test_file.csv"


#ensure non-s3 events return an empty list
def test_non_s3_event_returns_empty_list():
    event = {"data": "event"}
    s3_objects = extract_s3_info(event)
    assert s3_objects == []


#SNS_TOPIC_ARN missing should not crash Lambda
def test_missing_sns_topic_does_not_crash():
    event = {"data": "event"}
    context = {}
    if "SNS_ALERT_TOPIC_ARN" in os.environ:
        del os.environ["SNS_ALERT_TOPIC_ARN"]

    response = lambda_handler(event, context)
    assert response["statusCode"] == 200