provider "aws" {
  region = "ap-northeast-2"
  assume_role {
    role_arn = "arn:aws:iam::333333333333:role/SampleAccountProvisioningRole"
  }
}