terraform {
    backend "s3" {
        # This is stupid to hard code the profile name but it seems variables are not supported here...
        profile = "tetris"
        bucket = "unclechris-tetris-terraform-store2"
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