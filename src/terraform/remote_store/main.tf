resource "aws_s3_bucket" "remote_store_bucket" {
  bucket = "unclechris-tetris-terraform-store2"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "remote_store_encryption" {
  bucket = aws_s3_bucket.remote_store_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "remote_store_versioning" {
  bucket = aws_s3_bucket.remote_store_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "remote_store_lock_table" {
  name = "tetris-terraform-store-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}