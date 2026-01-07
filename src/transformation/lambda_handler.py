import logging
from src.transformation.transformer import main_transformer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Transformation Lambda triggered")
    logger.info(event)

    # perform transformations and upload to S3 transformation bucket 
    main_transformer()

    return {
        "statusCode": 200,
    }

if __name__ == "__main__":
    lambda_handler("test", "")
