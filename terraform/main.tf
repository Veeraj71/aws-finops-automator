terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Call the custom network module
module "network" {
  source       = "./modules/network"
  aws_region   = var.aws_region
  environment  = var.environment
  project_name = var.project_name
  owner        = var.owner
}

# 1. Create a Security Group inside our new VPC
resource "aws_security_group" "web_sg" {
  name        = "${var.environment}-web-sg"
  description = "Allow web and SSH traffic"
  vpc_id      = module.network.vpc_id # Pulls the ID directly out of our module!

  # Inbound HTTP (Port 80) from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Inbound HTTPS (Port 443) from anywhere
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Inbound SSH (Port 22) - Configurable, but defaults to open (FLAGGED)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  # Outbound traffic - allow the servers to talk to the internet
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.environment}-web-sg"
    Environment = var.environment
    Project     = var.project_name
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

# 2. Create Two EC2 Instances (Web Tier)
resource "aws_instance" "web" {
  count         = 2
  ami           = "ami-df5dbec3" # Fake AMI ID for LocalStack
  instance_type = "t3.micro"

  # Alternates placing instances between Subnet 1 and Subnet 2
  subnet_id              = module.network.public_subnet_ids[count.index]
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name        = "${var.environment}-web-server-${count.index + 1}"
    Tier        = "web" # Required tag by brief
    Environment = var.environment
    Project     = var.project_name
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

# 3. Create an S3 Bucket for App Logs
resource "aws_s3_bucket" "app_logs" {
  bucket        = "nimbuskart-logs-${var.environment}-unique-suffix"
  force_destroy = true

  tags = {
    Environment = var.environment
    Project     = var.project_name
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

# Enable Versioning on the Bucket
resource "aws_s3_bucket_versioning" "logs_versioning" {
  bucket = aws_s3_bucket.app_logs.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Add Lifecycle Rule: Expire old versions after 30 days
resource "aws_s3_bucket_lifecycle_configuration" "logs_lifecycle" {
  bucket = aws_s3_bucket.app_logs.id

  rule {
    id     = "expire-noncurrent-versions"
    status = "Enabled"
    
    filter {}

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}



resource "aws_ebs_volume" "orphaned_volume" {
  availability_zone = "${var.aws_region}a"
  size              = 10 # 10 GB
  type              = "gp3"

  tags = {
    Name        = "${var.environment}-orphaned-ebs"
    Environment = var.environment
    Project     = var.project_name
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}