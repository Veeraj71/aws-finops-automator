variable "aws_region" { type = string }
variable "environment" { type = string }
variable "project_name" { type = string }
variable "owner" { type = string }

variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16" # The exact network scale requested by the brief [cite: 26]
}

variable "public_subnet_1_cidr" {
  type    = string
  default = "10.20.1.0/24"
}

variable "public_subnet_2_cidr" {
  type    = string
  default = "10.20.2.0/24"
}