provider "aws" {
  region = "ap-northeast-2"
  assume_role {
    role_arn = "arn:aws:iam::111111111111:role/SampleAccountProvisioningRole"
  }
}