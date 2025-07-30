terraform {
    backend "s3" {
        bucket = "unclechris-tetris-terraform-store2"
        key = "staging.tfstate"
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
    region = "ap-southeast-2"

    default_tags {
        tags = {
            "env": "staging",
            "app": "tetris"
        }
    }
}