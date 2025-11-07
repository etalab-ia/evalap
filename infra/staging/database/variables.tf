# Staging Database Variables

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

variable "node_type" {
  description = "Database instance type"
  type        = string
  default     = "db-dev-s"

  validation {
    condition = contains([
      "db-dev-s", "db-dev-m", "db-dev-l",
      "db-playground-2-2", "db-playground-4-4",
      "db-general-2-8", "db-general-4-16",
      "db-general-8-32"
    ], var.node_type)
    error_message = "Node type must be a valid Scaleway RDB instance type."
  }
}

variable "storage" {
  description = "Database storage size"
  type        = string
  default     = "10GB"

  validation {
    condition     = can(regex("^[0-9]+(GB|TB)$", var.storage))
    error_message = "Storage must be in GB or TB format (e.g., 10GB, 100GB)."
  }
}

variable "enable_ha" {
  description = "Enable high availability with read replica"
  type        = bool
  default     = false # Disabled for staging to save costs
}

variable "database_password" {
  description = "Database password"
  type        = string
  sensitive   = true

  validation {
    condition     = length(var.database_password) >= 16
    error_message = "Database password must be at least 16 characters long."
  }
}

variable "private_network_id" {
  description = "Private network ID for database"
  type        = string
}

variable "private_network_cidr" {
  description = "Private network CIDR for security rules"
  type        = string
  default     = "10.0.0.0/24"
}

variable "backup_config" {
  description = "Backup configuration"
  type = object({
    frequency           = string
    retention_days      = number
    backup_window_start = string
    backup_window_end   = string
  })

  default = {
    frequency           = "daily"
    retention_days      = 7 # Keep 7 days for staging
    backup_window_start = "02:00"
    backup_window_end   = "04:00"
  }
}

variable "performance_settings" {
  description = "Database performance settings"
  type = object({
    max_connections            = number
    log_statement              = string
    log_min_duration_statement = number
    shared_buffers             = string
    effective_cache_size       = string
    work_mem                   = string
  })

  default = {
    max_connections            = 50
    log_statement              = "all"
    log_min_duration_statement = 1000
    shared_buffers             = "128MB"
    effective_cache_size       = "256MB"
    work_mem                   = "4MB"
  }
}

variable "monitoring_config" {
  description = "Database monitoring configuration"
  type = object({
    enable_query_logs      = bool
    enable_slow_queries    = bool
    slow_query_threshold   = number
    enable_connection_logs = bool
  })

  default = {
    enable_query_logs      = true
    enable_slow_queries    = true
    slow_query_threshold   = 1000 # Log queries > 1s
    enable_connection_logs = true
  }
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)

  default = {
    "Project"     = "EvalAP"
    "Environment" = "staging"
    "ManagedBy"   = "OpenTofu"
    "Component"   = "database"
  }
}

variable "database_extensions" {
  description = "Database extensions to enable"
  type        = list(string)

  default = [
    "pg_stat_statements",
    "uuid-ossp"
  ]
}

variable "connection_pool_config" {
  description = "Connection pool configuration"
  type = object({
    enable_pool         = bool
    pool_size           = number
    client_idle_timeout = number
  })

  default = {
    enable_pool         = false # Disabled for staging
    pool_size           = 20
    client_idle_timeout = 300
  }
}
