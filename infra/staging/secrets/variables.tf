# Staging Secrets Variables

variable "environment" {
  description = "Environment name (staging)"
  type        = string
}

variable "project_id" {
  description = "Scaleway project ID"
  type        = string
}

variable "region" {
  description = "Scaleway region"
  type        = string
  default     = "fr-par"
}

variable "secret_names" {
  description = "List of secret names to create"
  type        = list(string)

  default = [
    "database_url",
    "api_key",
    "jwt_secret"
  ]
}

variable "database_url" {
  description = "Database connection URL"
  type        = string
  sensitive   = true
}

variable "api_key" {
  description = "API key for services"
  type        = string
  sensitive   = true

  validation {
    condition     = length(var.api_key) >= 32
    error_message = "API key must be at least 32 characters long."
  }
}

variable "jwt_secret" {
  description = "JWT signing secret"
  type        = string
  sensitive   = true

  validation {
    condition     = length(var.jwt_secret) >= 64
    error_message = "JWT secret must be at least 64 characters long for security."
  }
}

variable "enable_redis" {
  description = "Enable Redis secret"
  type        = bool
  default     = false
}

variable "redis_url" {
  description = "Redis connection URL"
  type        = string
  sensitive   = true
  default     = ""
}

variable "enable_albert_api" {
  description = "Enable Albert API secret"
  type        = bool
  default     = false
}

variable "albert_api_key" {
  description = "Albert API key"
  type        = string
  sensitive   = true
  default     = ""
}

variable "secret_rotation_config" {
  description = "Secret rotation configuration"
  type = object({
    enable_rotation        = bool
    rotation_interval_days = number
    auto_rotate            = bool
  })

  default = {
    enable_rotation        = true
    rotation_interval_days = 30 # Rotate every 30 days in staging
    auto_rotate            = true
  }
}

variable "access_logging_config" {
  description = "Secret access logging configuration"
  type = object({
    enable_logging    = bool
    retention_days    = number
    log_failed_access = bool
  })

  default = {
    enable_logging    = true
    retention_days    = 30 # Keep logs for 30 days in staging
    log_failed_access = true
  }
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)

  default = {
    "Project"     = "EvalAP"
    "Environment" = "staging"
    "ManagedBy"   = "OpenTofu"
    "Component"   = "secrets"
  }
}

variable "iam_permissions" {
  description = "IAM permissions for secret access"
  type = object({
    read_permissions   = list(string)
    write_permissions  = list(string)
    delete_permissions = list(string)
  })

  default = {
    read_permissions = [
      "secrets:read",
      "secrets:list"
    ]
    write_permissions = [
      "secrets:create",
      "secrets:update"
    ]
    delete_permissions = [
      "secrets:delete"
    ]
  }
}

variable "additional_secrets" {
  description = "Additional secrets to create"
  type = map(object({
    description      = string
    value            = string
    rotation_enabled = bool
  }))

  default = {}
}
