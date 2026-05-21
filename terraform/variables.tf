variable "aws_region" {
  type        = string
  description = "The AWS region to deploy resources into"
  default     = "us-east-1"
}

variable "environment" {
  type        = string
  description = "Deployment environment name"
  default     = "staging"
}

variable "project_name" {
  type    = string
  default = "NimbusKart"
}

variable "owner" {
  type    = string
  default = "DevOpsTeam"
}

variable "ssh_allowed_cidr" {
  type        = string
  description = "CRITICAL SECURITY WARNING: Defaulting to 0.0.0.0/0 allows global SSH access. Override this in production."
  default     = "0.0.0.0/0"
}