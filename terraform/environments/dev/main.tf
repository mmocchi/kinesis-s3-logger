provider "aws" {
  region = "ap-northeast-1"
}

module "log_infrastructure" {
  source = "../../modules/log_infrastructure"

  environment          = "dev"
  project             = "log-system"
  bucket_name         = "mtmt-dev-log-bucket-name"
  lambda_function_name = "mtmt-dev-log-sender"
  firehose_stream_name = "mtmt-dev-log-delivery-stream"
} 