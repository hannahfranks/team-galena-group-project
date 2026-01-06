# ingestion Lambda function
resource "aws_lambda_function" "ingestion_lambda" {
  function_name = "ingestion_lambda_function"
  role = aws_iam_role.ingestion_lambda_role.arn
  handler = "ingestion_lambda.ingest.lambda_handler"
  runtime = "python3.12"
  timeout = 300

  s3_bucket = "galena-s3-ingestion-lambda-bucket"
  s3_key = aws_s3_object.ingestion_lambda_zip.key

  #filename = data.archive_file.ingestion_lambda_zip.output_path

  layers = [
    "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python312:1",
    aws_lambda_layer_version.ingestion_db_layer.arn
    ]

  tags = { 
    Application = "ingestion"
  }
}

# Package the Lambda ingestion function code
data "archive_file" "ingestion_lambda_zip" {
  type = "zip"
  source_dir  = "${path.module}/../src/ingestion/ingestion_lambda"
  output_path = "${path.module}/build/ingestion_lambda.zip"
}

#Create ingestion lambda layers 
resource "aws_lambda_layer_version" "ingestion_db_layer" {
  layer_name = "ingestion-dependencies-db"
  filename = data.archive_file.ingestion_db_layer_zip.output_path
  compatible_runtimes = ["python3.12"]
  source_code_hash = filebase64sha256("${path.module}/build/ingestion_db_layer.zip")
}

#Package ingestion lambda layers
data "archive_file" "ingestion_db_layer_zip" {
  type = "zip"
  source_dir = "${path.module}/../src/ingestion/layers/db_layer"
  output_path = "${path.module}/build/ingestion_db_layer.zip"
}

#Upload to lambda ingestion s3 bucket 
resource "aws_s3_object" "ingestion_lambda_zip" {
  bucket = "galena-s3-ingestion-lambda-bucket"
  key    = "ingestion_lambda.zip"
  source = data.archive_file.ingestion_lambda_zip.output_path
  etag = filemd5(data.archive_file.ingestion_lambda_zip.output_path)
}

# transformation lambda
resource "aws_lambda_function" "transformation_lambda" {
  function_name = "transformation_lambda_function"
  role          = aws_iam_role.transformation_lambda_role.arn

  runtime = "python3.12"
  handler = "lambda_handler.lambda_handler"

  s3_bucket = "galena-s3-transformation-lambda-bucket"
  s3_key    = aws_s3_object.transformation_lambda_zip.key

  tags = {
    Application = "transformation"
  }
}

# Package the transformation Lambda function code
data "archive_file" "transformation_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src/transformation"
  output_path = "${path.module}/build/transformation_lambda.zip"
}

#Upload transformation lambda to lambda s3 bucket 
resource "aws_s3_object" "transformation_lambda_zip" {
  bucket = "galena-s3-transformation-lambda-bucket"
  key    = "transformation_lambda.zip"
  source = data.archive_file.transformation_lambda_zip.output_path
  etag = filemd5(data.archive_file.transformation_lambda_zip.output_path)
}
