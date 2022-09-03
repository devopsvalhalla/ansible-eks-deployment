terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.29.0"
    }
  }
}

provider "aws" {
  # Configuration options
}

data "aws_subnets" "available_subnets" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
    state = "available"
  }
}

data "aws_subnet" "example" {
  for_each = toset(data.aws_subnets.available_subnets.ids)
  id       = each.value
}