resource "aws_kinesis_firehose_delivery_stream" "example_security" {
  name        = "aws-waf-logs-ap-northeast-2"
  destination = "extended_s3"

  extended_s3_configuration {
    role_arn            = "arn:aws:iam::333333333333:role/firehose_delivery_role"
    bucket_arn          = "arn:aws:s3:::example-aws-waf-logs"
    prefix              = "333333333333/ap-northeast-2/"
    error_output_prefix = "errors/"

    buffering_size     = 128
    buffering_interval = 300

    compression_format = "GZIP"

    cloudwatch_logging_options {
      enabled = false
    }
  }
}