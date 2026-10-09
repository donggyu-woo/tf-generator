data "aws_caller_identity" "current" {}

module "detector" {
  source  = "aws-ss/guardduty/aws"
  version = "4.1.0"

  enable                       = true
  finding_publishing_frequency = "FIFTEEN_MINUTES"
}

module "detector_feature_s3_data_events" {
  source  = "aws-ss/guardduty/aws//modules/detector_feature"
  version = "4.1.0"

  detector_id = module.detector.guardduty_id
  name        = "S3_DATA_EVENTS"
  status      = "ENABLED"
}

module "detector_feature_runtime_monitoring" {
  source  = "aws-ss/guardduty/aws//modules/detector_feature"
  version = "4.1.0"

  detector_id = module.detector.guardduty_id
  name        = "RUNTIME_MONITORING"
  status      = "ENABLED"

  additional_configuration = [
    {
      name   = "EKS_ADDON_MANAGEMENT"
      status = "ENABLED"
    },
    {
      name   = "ECS_FARGATE_AGENT_MANAGEMENT"
      status = "ENABLED"
    },
    {
      name   = "EC2_AGENT_MANAGEMENT"
      status = "DISABLED"
    },
  ]
}

module "organization_admin_account" {
  source  = "aws-ss/guardduty/aws//modules/organization_admin_account"
  version = "4.1.0"

  admin_account_id = data.aws_caller_identity.current.account_id

  depends_on = [module.detector]
}

module "organization_configuration" {
  source  = "aws-ss/guardduty/aws//modules/organization_configuration"
  version = "4.1.0"

  detector_id                      = module.detector.guardduty_id
  auto_enable_organization_members = "ALL"

  depends_on = [module.organization_admin_account]
}

module "organization_configuration_feature_s3_data_events" {
  source  = "aws-ss/guardduty/aws//modules/organization_configuration_feature"
  version = "4.1.0"

  detector_id = module.detector.guardduty_id
  name        = "S3_DATA_EVENTS"
  auto_enable = "ALL"

  depends_on = [module.organization_configuration]
}

module "organization_configuration_feature_runtime_monitoring" {
  source  = "aws-ss/guardduty/aws//modules/organization_configuration_feature"
  version = "4.1.0"

  detector_id = module.detector.guardduty_id
  name        = "RUNTIME_MONITORING"
  auto_enable = "ALL"

  additional_configuration = [
    {
      name        = "EKS_ADDON_MANAGEMENT"
      auto_enable = "ALL"
    },
    {
      name        = "ECS_FARGATE_AGENT_MANAGEMENT"
      auto_enable = "ALL"
    },
    {
      name        = "EC2_AGENT_MANAGEMENT"
      auto_enable = "NONE"
    },
  ]

  depends_on = [module.organization_configuration]
}