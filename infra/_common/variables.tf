# Common variables shared across all environments

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "evalap"
}

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

variable "extra_tags" {
  description = "Additional tags to apply to resources"
  type        = map(string)
  default     = {}
}

variable "enable_monitoring" {
  description = "Enable monitoring for resources"
  type        = bool
  default     = true
}

variable "enable_backup" {
  description = "Enable backup for supported resources"
  type        = bool
  default     = true
}

# Variables for state backend (optional)
variable "create_state_backend" {
  description = "Whether to create the state backend resources"
  type        = bool
  default     = false
}

variable "state_bucket_name" {
  description = "Name of the S3 bucket for Terraform state storage"
  type        = string
  default     = "evalap-terraform-state"
}

variable "state_lock_table" {
  description = "Name of the DynamoDB table for state locking"
  type        = string
  default     = "terraform-locks"
}
