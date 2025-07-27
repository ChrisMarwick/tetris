data "aws_vpc" "vpc" {
  default = true
}

data "aws_subnets" "subnets" {
  filter {
    name = "vpc-id"
    values = [data.aws_vpc.vpc.id]
  }
}

data "aws_security_group" "default_security_group" {
    vpc_id = data.aws_vpc.vpc.id

    filter {
        name = "group-name"
        values = ["default"]
    }
}