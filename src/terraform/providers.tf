terraform {
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