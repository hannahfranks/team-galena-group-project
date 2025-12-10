terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}

#Backend config

terraform {
    backend "s3" {
        bucket = "galena-remote-state-backend"
        key = "global/s3/terraform.tfstate"
        region = "eu-west-2"
        dynamodb_table = "backend-dynamo"
        encrypt = true
    }
}