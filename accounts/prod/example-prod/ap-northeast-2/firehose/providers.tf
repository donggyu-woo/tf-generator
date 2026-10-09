provider "aws" {
  region = "ap-northeast-2"
  assume_role {
    role_arn = "arn:aws:iam::222222222222:role/SampleAccountProvisioningRole"
  }
}