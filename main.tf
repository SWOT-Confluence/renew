terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  default_tags {
    tags = local.default_tags
  }
  region  = var.aws_region
  profile = var.profile
}

# Data sources
data "aws_caller_identity" "current" {}

data "aws_iam_policy" "get_put_parameter" {
  name = "amazon-ssm-get-put-parameter"
}

# Local variables
locals {
  account_id = data.aws_caller_identity.current.account_id
  default_tags = length(var.default_tags) == 0 ? {
    application : var.app_name,
    version : var.app_version
  } : var.default_tags
}