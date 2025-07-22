# variables.tf
variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}

variable "public_subnet_id" {
  description = "The ID of the public subnet"
  type        = string
}

variable "private_route_table_id" {
  description = "The route table ID for private subnet"
  type        = string
}

variable "my_ip" {
  description = "Your public IP with CIDR (e.g. 203.0.113.0/32)"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
}

variable "config_bucket_name" {
  description = "S3 bucket name for AWS Config logs"
  type        = string
}
