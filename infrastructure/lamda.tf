# Lambda function

resource "aws_lambda_function" "ingestion_lambda" {
  function_name = "ingestion_lambda_function"
  role = aws_iam_role.ingestion_lambda_role.arn
  handler = "lambda_function.lambda_handler"
  runtime = "Python 3.14"
  filename = data.archive_file.ingestion_lambda_zip.output_path

  environment {    
    variables = {
      BUCKET_NAME = aws_s3_bucket.ingestion_lambda_bucket.bucket #check this variable
      LOG_LEVEL   = "info"
    }
  }

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
