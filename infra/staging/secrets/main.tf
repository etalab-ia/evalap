# Staging Secrets Module
# Manages secrets for staging environment using Scaleway Secret Manager

terraform {
  required_providers {
    scaleway = {
      source  = "scaleway/scaleway"
      version = ">= 2.0"
    }
  }
}

# Note: Scaleway Secret Manager resources will be configured
# For now, we create placeholder outputs for integration

# Outputs
output "database_url_secret_id" {
  description = "Database URL secret ID"
  value       = "staging-database-url"
}

output "api_key_secret_id" {
  description = "API key secret ID"
  value       = "staging-api-key"
}

output "jwt_secret_id" {
  description = "JWT secret ID"
  value       = "staging-jwt-secret"
}

output "secrets_enabled" {
  description = "Whether secrets management is enabled"
  value       = true
}

output "environment" {
  description = "Environment name"
  value       = var.environment
}
