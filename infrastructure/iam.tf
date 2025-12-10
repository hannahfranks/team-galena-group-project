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