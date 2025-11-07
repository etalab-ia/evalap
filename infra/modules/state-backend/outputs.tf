# Outputs for state backend configuration

output "state_bucket_name" {
  description = "Name of the created S3 bucket"
  value       = scaleway_object_bucket.terraform_state.name
}

output "state_bucket_arn" {
  description = "ARN of the created S3 bucket"
  value       = scaleway_object_bucket.terraform_state.id
}

output "state_bucket_endpoint" {
  description = "Endpoint URL for the S3 bucket"
  value       = scaleway_object_bucket.terraform_state.endpoint
}

output "state_bucket_region" {
  description = "Region where the bucket is located"
  value       = scaleway_object_bucket.terraform_state.region
}
