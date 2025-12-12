# Lambda function

resource "aws_lambda_function" "ingestion_lambda" {
  function_name = "ingestion_lambda_function"
  role = aws_iam_role.ingestion_lambda_role.arn
  handler = "lambda_function.lambda_handler"
  runtime = "python3.14"

  s3_bucket = "galena-s3-ingestion-lambda-bucket"
  s3_key = aws_s3_bucket_object.ingestion_lambda_zip.key

  tags = { 
    Application = "ingestion"
  }
}

# Package the Lambda function code

data "archive_file" "ingestion_lambda_zip" {
  type = "zip"
  source_file = "${path.module}/src/ingestion/ingest.py"
  output_path = "${path.module}/src/ingestion/ingestion_lambda_function.zip"
}

#Upload to lambda s3 bucket 

resource "aws_s3_object" "ingestion_lambda_zip" {
  bucket = "galena-s3-ingestion-lambda-bucket"
  key = "ingestion_lambda_function.zip"
  source = data.archive_file.ingestion_lambda_zip.output_path
}