terraform {
    backend "s3" {
        bucket = "unclechris-tetris-terraform-store"
        key = "live.tfstate"
        region = "ap-southeast-2"
        dynamodb_table = "tetris-terraform-store-locks"
        encrypt = true
    }

    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "6.2.0"
        }
    }
}

provider "aws" {
    region = "ap-southeast-2"

    default_tags {
        tags = {
            "env": "live",
            "app": "tetris"
        }
    }
}