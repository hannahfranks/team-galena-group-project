from datetime import datetime
import boto3

s3 = boto3.client("s3")

def save_ingestion_timestamp():
    timestamp = datetime.now().strftime("%d_%m_%Y_%H:%M:%S")

    filename = "ingestion/last_ingestion_timestamp.txt"

    content = f"Ingestion run at: {timestamp}"

    with open("last_ingestion_timestamp.txt", "w") as f:
        f.write(content)

    s3.put_object(
        Bucket="s3-ingestion-bucket-team-galena",
        Key=filename,
        Body=content.encode("utf-8")
    )


