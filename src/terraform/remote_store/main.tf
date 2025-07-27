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
