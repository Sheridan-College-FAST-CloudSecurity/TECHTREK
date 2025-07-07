provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "hospital_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "hospital-vpc"
  }
}

# Subnet 1 (AZ a)
resource "aws_subnet" "public_subnet" {
  vpc_id            = aws_vpc.hospital_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "hospital-public-subnet-1"
  }
}

# Subnet 2 (AZ b) ✅ Added for RDS AZ coverage
resource "aws_subnet" "public_subnet_2" {
  vpc_id            = aws_vpc.hospital_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "hospital-public-subnet-2"
  }
}

# EC2 module
module "ec2" {
  source    = "./modules/ec2"
  vpc_id    = aws_vpc.hospital_vpc.id
  subnet_id = aws_subnet.public_subnet.id
}

# Security Group for RDS
resource "aws_security_group" "rds_sg" {
  name        = "rds_sg"
  description = "Allow MySQL access from EC2"
  vpc_id      = aws_vpc.hospital_vpc.id

  ingress {
    description = "MySQL from EC2"
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "HospitalRDSAccess"
  }
}

# RDS module ✅ updated to use 2 subnets (2 AZs)
module "rds" {
  source                 = "./modules/rds"
  db_name                = "hospitaldb"
  username               = "admin"
  password               = "YourSecurePassword123!"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  subnet_ids             = [
    aws_subnet.public_subnet.id,
    aws_subnet.public_subnet_2.id
  ]
}
