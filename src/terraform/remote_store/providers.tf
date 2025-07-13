terraform {
    backend "s3" {
        bucket = "unclechris-tetris-terraform-store"
        key = "remote_store.tfstate"
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
            "app": "tetris"
        }
    }
}