module "trails_data" {
  source  = "aws-ss/cloudtrail/aws"
  version = "2.1.0"

  name                       = "example-data-cloudtrail-logs"
  s3_bucket_name             = "example-data-cloudtrail-logs"
  enable_logging             = true
  enable_log_file_validation = true
  is_multi_region_trail      = true

  advanced_event_selector = [
    {
      name = "Advanced Event Selector"
      field_selector = [
        {
          field  = "eventCategory"
          equals = ["Data"]
        },
        {
          field  = "resources.type"
          equals = ["AWS::S3::Object"]
        }
      ]
    }
  ]
}