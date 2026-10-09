terraform {
  backend "s3" {
    bucket       = "example-tf-state-bucket"
    key          = "aws/beta/example-beta/ap-northeast-2/cloudtrail/data/terraform.tfstate"
    region       = "ap-northeast-2"
    encrypt      = true
    use_lockfile = true
  }
}