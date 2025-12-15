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

<<<<<<< HEAD
# transformation lambda
resource "aws_lambda_function" "transformation_lambda" {
  function_name = "transformation_lambda_function"
  role          = aws_iam_role.transformation_lambda_role.arn

  runtime = "python3.12"
  handler = "lambda_handler.lambda_handler"

  s3_bucket = var.transformation_bucket
  s3_key    = aws_s3_object.transformation_lambda_zip.key

  source_code_hash = data.archive_file.transformation_lambda_zip.output_base64sha256

  tags = {
    Application = "transformation"
  }
}

# Package the transformation Lambda function code
data "archive_file" "transformation_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/src/transformation"
  output_path = "${path.module}/build/transformation_lambda.zip"
}

#Upload to lambda s3 bucket 
resource "aws_s3_object" "transformation_lambda_zip" {
  bucket = var.transformation_bucket
  key    = "transformation_lambda.zip"
  source = data.archive_file.transformation_lambda_zip.output_path
}
=======
>>>>>>> b0654bb (Feat: trigger for ingestion lambda)
