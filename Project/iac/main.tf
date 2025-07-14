provider "aws" {
  region = "us-east-1"
}

# VPC, Subnets, and other resources here (assumed already done)...

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "hospital-vpc"
  }
}

resource "aws_subnet" "public_1a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-1a"
  }
}

resource "aws_subnet" "private_1a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "private-subnet-1a"
  }
}

# Call EC2 module
module "ec2" {
  source = "./modules/ec2"

  vpc_id           = aws_vpc.main.id
  public_subnet_id = aws_subnet.public_1a.id
  private_subnet_id = aws_subnet.private_1a.id

  ami_id        = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"
}

