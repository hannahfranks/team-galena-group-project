# Creates the ingestion-bucket
resource "aws_s3_bucket" "ingestion_bucket" {
  bucket = "s3-ingestion-bucket-team-galena"
}

# Enable version history for ingestion-bucket
resource "aws_s3_bucket_versioning" "ingestion_versioning" {
  bucket = aws_s3_bucket.ingestion_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Encrypts everything automatically in ingestion-bucket
resource "aws_s3_bucket_server_side_encryption_configuration" "ingestion_encryption" {
  bucket = aws_s3_bucket.ingestion_bucket.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Ensures ingestion-bucket cannot become public
resource "aws_s3_bucket_public_access_block" "ingestion_public_block" {
  bucket = aws_s3_bucket.ingestion_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  restrict_public_buckets = true
  ignore_public_acls      = true
}

# event notification for ingestion s3 bucket
resource "aws_s3_bucket_notification" "ingestion_notification" {
  bucket = aws_s3_bucket.ingestion_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.transformation_lambda.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix = ".parquet"
  }
  depends_on = [
    aws_lambda_permission.allow_s3
  ]
}

#Create Lambda S3
resource "aws_s3_bucket" "ingestion_lambda" {
  bucket = "galena-s3-ingestion-lambda-bucket"
}

#Create Lambda S3 for transformation
resource "aws_s3_bucket" "transformation_lambda_s3" {
  bucket = "galena-s3-transformation-lambda-bucket"
}

# Creates the transformation-bucket
resource "aws_s3_bucket" "transformation_bucket" {
  bucket = "s3-transformation-bucket-team-galena"
}

# Enable version history for transformation-bucket
resource "aws_s3_bucket_versioning" "transformation_versioning" {
  bucket = aws_s3_bucket.transformation_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Encrypts everything automatically in transformation-bucket
resource "aws_s3_bucket_server_side_encryption_configuration" "transformation_encryption" {
  bucket = aws_s3_bucket.transformation_bucket.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Ensures transformation-bucket cannot become public
resource "aws_s3_bucket_public_access_block" "transformation_public_block" {
  bucket = aws_s3_bucket.transformation_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  restrict_public_buckets = true
  ignore_public_acls      = true
}
