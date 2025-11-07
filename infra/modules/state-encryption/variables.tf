# Variables for state encryption configuration

variable "environment" {
  description = "Environment name (staging or production)"
  type        = string
}

variable "state_bucket_name" {
  description = "Name of the S3 bucket for Terraform state storage"
  type        = string
  default     = "evalap-terraform-state"
}

variable "default_region" {
  description = "Default Scaleway region"
  type        = string
  default     = "fr-par"
}
