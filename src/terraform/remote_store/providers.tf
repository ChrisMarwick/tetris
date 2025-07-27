terraform {
    backend "s3" {
        bucket = "unclechris-tetris-terraform-store2"
        key = "remote_store.tfstate"
        region = "ap-southeast-2"
        use_lockfile = true
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
    profile = var.aws_profile
    region = "ap-southeast-2"

    default_tags {
        tags = {
            "app": "tetris"
        }
    }
}