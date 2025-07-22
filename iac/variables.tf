variable "key_name" {
  description = "Name of the EC2 key pair"
  type        = string
}

variable "private_key_path" {
  description = "Path to the EC2 private key"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}
