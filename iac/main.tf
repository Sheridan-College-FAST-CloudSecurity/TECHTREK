provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

# (Other resources: subnet, internet gateway, route table, security group, EC2 instance, etc.)

resource "aws_instance" "web" {
  ami                         = "ami-0261755bbcb8c4a84" # Ubuntu 22.04
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.web_sg.id]
  associate_public_ip_address = true
  key_name                    = var.key_name

  tags = {
    Name = "FastAPI-Server"
  }
}