output "vpc_id" {
  description = "The ID of the provisioned VPC"
  value       = module.network.vpc_id
}

output "public_subnet_ids" {
  description = "The IDs of the public subnets"
  value       = module.network.public_subnet_ids
}

output "log_bucket_name" {
  description = "The name of the application log S3 bucket"
  value       = aws_s3_bucket.app_logs.id
}