import boto3

s3 = boto3.client("s3")

# util function to get timestamp of most recent ingestion
def get_timestamp():
    
    response = s3.get_object(Bucket='s3-ingestion-bucket-team-galena', Key='ingestion/last_ingestion_timestamp.txt')
    ingest_timestamp = response['Body'].read().decode('utf-8')

    return ingest_timestamp
