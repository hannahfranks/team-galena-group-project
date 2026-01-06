#IAM role for S3 and DynamoDB access for backend

resource "aws_iam_role" "terraform" {
    name = "terraform-execution-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Principal = {
                    AWS = "arn:aws:iam::891807086100:root"
                }
            }
        ]
    })
}

#IAM policy for terraform state

resource "aws_iam_policy" "terraform_state_access" {
    name = "terraform-state-access"
    description = "permissions for terraform to use s3 and dynamoDB"

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Sid = "TerraformStateS3Access"
                Effect = "Allow"
                Action = [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject",
                    "s3:ListBucket"
                ]
                Resource = [
                    "arn:aws:s3:::galena-remote-state-backend",
                    "arn:aws:s3:::galena-remote-state-backend/*"
                ]
            },
            {
                Sid = "TerraformDynamoDBStateLockAccess"
                Effect = "Allow"
                Action = [
                    "dynamodb:DescribeTable",
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                    "dynamodb:DeleteItem"
                ]
                Resource = "arn:aws:dynamodb:eu-west-2:891807086100:table/backend-dynamo"
            }
        ]
    })
}

#Attach policy to role

resource "aws_iam_role_policy_attachment" "state_access" {
    role = aws_iam_role.terraform.name
    policy_arn = aws_iam_policy.terraform_state_access.arn
}

#IAM role for Ingestion Lambda

resource "aws_iam_role" "ingestion_lambda_role" {
    name = "ingestion_lambda_role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Principal = {
                    Service = "lambda.amazonaws.com"
                }
            }
        ]
    })
}

#IAM Policy for write-only s3 access

resource "aws_iam_policy" "ingestion_lambda_policy" {
    name = "ingestion_lambda_write_to_s3"
    description = "write-only access data in ingestion s3"

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Effect = "Allow"
            Action = [
                "s3:PutObject"
            ]
            Resource = "arn:aws:s3:::s3-ingestion-bucket-team-galena/*"
        },
        {
            Effect = "Allow"
            Action = [
                "secretsmanager:GetSecretValue"
            ]
            Resource = "arn:aws:secretsmanager:eu-west-2:891807086100:secret:totesys/rds/credentials*"
        }
        ]
    })
}

#Attach policy to role

resource "aws_iam_role_policy_attachment" "ingestion_lambda_policy" {
    role = aws_iam_role.ingestion_lambda_role.name
    policy_arn = aws_iam_policy.ingestion_lambda_policy.arn
}

#IAM role for transformation Lambda
resource "aws_iam_role" "transformation_lambda_role" {
  name = "transformation-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

#IAM Policy for transformation_lambda_role to s3 access 
resource "aws_iam_policy" "transformation_lambda_policy" {
    name = "transformation-lambda-policy"
    description = "write-only access data in transformation s3"

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
{
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::s3-transformation-bucket-team-galena",
          "arn:aws:s3:::s3-transformation-bucket-team-galena/*"
        ]
      }
        ]
    })
}

#Attach policy to role
resource "aws_iam_role_policy_attachment" "transformation_lambda_policy" {
    role = aws_iam_role.transformation_lambda_role.name
    policy_arn = aws_iam_policy.transformation_lambda_policy.arn
}

#IAM role for cloudwatch logging 
resource "aws_iam_policy" "cloudwatch_logs" {
    name = "cloudwatch_logs"
    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
            Effect = "Allow"
            Action = [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ]
            Resource = "*"
        }
        ]
    })
}

#Attach policy to ingestion lambda role 
resource "aws_iam_role_policy_attachment" "ingestion_lambda_logs" {
    role = aws_iam_role.ingestion_lambda_role.name
    policy_arn = aws_iam_policy.cloudwatch_logs.arn
}

#Attach policy to transformation lambda role 
resource "aws_iam_role_policy_attachment" "transformation_lambda_logs" {
    role = aws_iam_role.transformation_lambda_role.name
    policy_arn = aws_iam_policy.cloudwatch_logs.arn
}

# allow ingestion s3 to invoke transformation lambda
resource "aws_lambda_permission" "allow_ingestion_s3_access" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.transformation_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.ingestion_bucket.arn
}
