# Creates the bucket
resource "aws_s3_bucket" "ingestion_bucket" {
  bucket = "s3-ingestion-bucket-team-galena"
}

# Enable version history
resource "aws_s3_bucket_versioning" "ingestion_versioning" {
  bucket = aws_s3_bucket.ingestion_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Encrypts everything automatically
resource "aws_s3_bucket_server_side_encryption_configuration" "default_encryption" {
  bucket = aws_s3_bucket.ingestion_bucket.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Ensures bucket cannot become public
resource "aws_s3_bucket_public_access_block" "public_block" {
  bucket = aws_s3_bucket.ingestion_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  restrict_public_buckets = true
  ignore_public_acls      = true
}