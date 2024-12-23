resource "aws_kinesis_firehose_delivery_stream" "log_stream" {
  name        = "${var.lambda_function_name}-stream"
  destination = "extended_s3"

  extended_s3_configuration {
    role_arn   = aws_iam_role.firehose_role.arn
    bucket_arn = aws_s3_bucket.log_bucket.arn
    prefix     = "logs/"

    cloudwatch_logging_options {
      enabled         = true
      log_group_name  = "/aws/firehose/${var.lambda_function_name}-stream"
      log_stream_name = "S3Delivery"
    }
  }
}

resource "aws_iam_role" "firehose_role" {
  name = "${var.lambda_function_name}-firehose-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "firehose.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "firehose_policy" {
  name = "${var.lambda_function_name}-firehose-policy"
  role = aws_iam_role.firehose_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.log_bucket.arn,
          "${aws_s3_bucket.log_bucket.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "firehose_logs" {
  name              = "/aws/firehose/${var.lambda_function_name}-stream"
  retention_in_days = 14  # ログの保持期間を14日に設定
}

resource "aws_cloudwatch_log_stream" "firehose_logs" {
  name           = "S3Delivery"
  log_group_name = aws_cloudwatch_log_group.firehose_logs.name
}