# Infrastructure configuration variables

variable "environment" {
  description = "Environment name (staging or production)"
  type        = string
  validation {
    condition     = contains(["staging", "production"], var.environment)
    error_message = "Environment must be either 'staging' or 'production'."
  }
}

variable "project_id" {
  description = "Scaleway Project ID"
  type        = string
  sensitive   = true
}

variable "scaleway_access_key" {
  description = "Scaleway Access Key"
  type        = string
  sensitive   = true
}

variable "scaleway_secret_key" {
  description = "Scaleway Secret Key"
  type        = string
  sensitive   = true
}

variable "default_region" {
  description = "Default Scaleway region"
  type        = string
  default     = "fr-par"
}

variable "default_zone" {
  description = "Default Scaleway zone"
  type        = string
  default     = "fr-par-2"
}

variable "state_bucket_name" {
  description = "S3 bucket name for Terraform state"
  type        = string
  default     = "evalap-terraform-state"
}

variable "state_lock_table" {
  description = "DynamoDB table name for state locking"
  type        = string
  default     = "terraform-locks"
}
