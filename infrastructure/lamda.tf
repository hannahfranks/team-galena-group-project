# Package the Lambda function code
data "archive_file" "example" {
  type        = "zip"
  source_file = "${path.module}/lambda/index.js"
  output_path = "${path.module}/lambda/function.zip"
}

# Lambda function
resource "aws_lambda_function" "ingestion_lambda_function" {
  filename         = data.archive_file.example.output_path
  function_name    = "ingestion_lambda_function"
  role             = aws_iam_role.lambda_role.arn
  handler          = "handler.lambda_handler"
  source_code_hash = data.archive_file.example.output_base64sha256

  runtime = "Python 3.13.7"

  environment {    
    variables = {
      ENVIRONMENT = "production" 
      LOG_LEVEL   = "info"
    }
  }

  tags = {
    Environment = "production"  
    Application = "example"
  }
}

#Secrets Manager
# resource "aws_secretsmanager_secret" "example" {
#   name = "example"
# }

# data "aws_iam_policy_document" "example" {
#   statement {
#     sid    = "EnableAnotherAWSAccountToReadTheSecret"
#     effect = "Allow"

#     principals {
#       type        = "AWS"
#       identifiers = ["arn:aws:iam::123456789012:root"]
#     }

#     actions   = ["secretsmanager:GetSecretValue"]
#     resources = ["*"]
#   }  
# }

# resource "aws_secretsmanager_secret_policy" "example" {
#   secret_arn = aws_secretsmanager_secret.example.arn
#   policy     = data.aws_iam_policy_document.example.json
# }