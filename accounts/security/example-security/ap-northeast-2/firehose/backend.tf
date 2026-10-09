terraform {
  backend "s3" {
    bucket       = "example-tf-state-bucket"
    key          = "aws/security/example-security/ap-northeast-2/firehose/terraform.tfstate"
    region       = "ap-northeast-2"
    encrypt      = true
    use_lockfile = true
  }
}