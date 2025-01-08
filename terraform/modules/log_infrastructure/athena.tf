# Athenaのクエリ結果を保存するためのS3バケット
resource "aws_s3_bucket" "athena_results" {
  bucket = "${var.bucket_name}-athena-results"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "athena_results" {
  bucket = aws_s3_bucket.athena_results.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "athena_results" {
  bucket = aws_s3_bucket.athena_results.id

  rule {
    id     = "query_results_lifecycle"
    status = "Enabled"

    # クエリ結果は30日後に削除
    expiration {
      days = 30
    }
  }
}

# Athenaワークグループの作成
resource "aws_athena_workgroup" "logs_analysis" {
  name = "${var.environment}_${var.project}_logs_analysis"

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true

    result_configuration {
      output_location = "s3://${aws_s3_bucket.athena_results.bucket}/output/"

      encryption_configuration {
        encryption_option = "SSE_S3"
      }
    }
  }

  force_destroy = true

  tags = {
    Environment = var.environment
    Project     = var.project
  }
} 