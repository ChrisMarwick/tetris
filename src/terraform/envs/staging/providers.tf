terraform {
    backend "s3" {
        # This is stupid to hard code the profile name but it seems variables are not supported here...
        profile = "tetris"
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
    profile = var.aws_profile
    region = "ap-southeast-2"

    default_tags {
        tags = {
            "env": "staging",
            "app": "tetris"
        }
    }
}