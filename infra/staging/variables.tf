# Staging Environment Variables

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

variable "database_password" {
  description = "Database password for staging"
  type        = string
  sensitive   = true
  default     = "changeme-staging-password-16" # Should be overridden
}

variable "database_url" {
  description = "Database connection URL"
  type        = string
  sensitive   = true
  default     = "postgresql://postgres:changeme@localhost:5432/evalap_staging" # Will be populated
}

variable "api_key" {
  description = "API key for services"
  type        = string
  sensitive   = true
  default     = "changeme-staging-api-key-32-chars-minimum" # Should be overridden
}

variable "jwt_secret" {
  description = "JWT signing secret"
  type        = string
  sensitive   = true
  default     = "changeme-staging-jwt-secret-64-chars-minimum-for-security" # Should be overridden
}
