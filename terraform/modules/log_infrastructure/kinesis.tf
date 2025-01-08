resource "aws_kinesis_firehose_delivery_stream" "log_stream" {
  name        = "${var.lambda_function_name}-stream"
  destination = "extended_s3"

  extended_s3_configuration {
    # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/kinesis_firehose_delivery_stream#extended_s3_configuration-block

    role_arn   = aws_iam_role.firehose_role.arn
    bucket_arn = aws_s3_bucket.log_bucket.arn

    # Dynamic Partitioningの設定
    prefix              = "logs/year=!{partitionKeyFromQuery:year}/month=!{partitionKeyFromQuery:month}/day=!{partitionKeyFromQuery:day}/"
    error_output_prefix = "errors/!{firehose:error-output-type}/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/"

    # バッファリングの設定
    buffering_size     = 64  # Dynamic Partitioning有効時の最小サイズ
    buffering_interval = 300 # 5分

    # データ形式の設定
    dynamic_partitioning_configuration {
      enabled = true
    }

    processing_configuration {
      enabled = true

      processors {
        type = "MetadataExtraction"
        parameters {
          parameter_name  = "JsonParsingEngine"
          parameter_value = "JQ-1.6"
        }
        parameters {
          parameter_name  = "MetadataExtractionQuery"
          parameter_value = "{year: (.timestamp[0:4]), month: (.timestamp[5:7]), day: (.timestamp[8:10])}"
        }
      }
    }

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
      },
      {
        Effect = "Allow"
        Action = [
          "glue:GetTableVersions",
          "glue:GetPartitions",
          "glue:GetTable",
          "glue:GetDatabase"
        ]
        Resource = [
          "arn:aws:glue:*:*:catalog",
          "arn:aws:glue:*:*:database/${aws_glue_catalog_database.logs_db.name}",
          "arn:aws:glue:*:*:table/${aws_glue_catalog_database.logs_db.name}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:PutLogEvents",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = [
          "${aws_cloudwatch_log_group.firehose_logs.arn}:*"
        ]
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "firehose_logs" {
  name              = "/aws/firehose/${var.lambda_function_name}-stream"
  retention_in_days = 14 # ログの保持期間を14日に設定
}

resource "aws_cloudwatch_log_stream" "firehose_logs" {
  name           = "S3Delivery"
  log_group_name = aws_cloudwatch_log_group.firehose_logs.name
}