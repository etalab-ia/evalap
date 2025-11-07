# Staging Monitoring Variables

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

variable "enable_alerts" {
  description = "Enable alerting for staging"
  type        = bool
  default     = false # Disabled for staging to reduce noise
}

variable "retention_days" {
  description = "Data retention period in days"
  type        = number
  default     = 7 # Keep 7 days for staging

  validation {
    condition     = var.retention_days >= 1 && var.retention_days <= 30
    error_message = "Retention days must be between 1 and 30 for staging."
  }
}

variable "documentation_container_id" {
  description = "Documentation container ID for monitoring"
  type        = string
}

variable "runners_container_id" {
  description = "Runners container ID for monitoring"
  type        = string
}

variable "streamlit_container_id" {
  description = "Streamlit container ID for monitoring"
  type        = string
}

variable "database_id" {
  description = "Database instance ID for monitoring"
  type        = string
}

variable "metrics_config" {
  description = "Metrics collection configuration"
  type = object({
    enable_custom_metrics = bool
    collection_interval   = number
    retention_policy      = string
  })

  default = {
    enable_custom_metrics = true
    collection_interval   = 60 # Collect every 60 seconds
    retention_policy      = "standard"
  }
}

variable "alert_thresholds" {
  description = "Alert thresholds for monitoring"
  type = object({
    error_rate_threshold         = number
    response_time_threshold      = number
    cpu_utilization_threshold    = number
    memory_utilization_threshold = number
    disk_utilization_threshold   = number
  })

  default = {
    error_rate_threshold         = 0.1 # 10% error rate
    response_time_threshold      = 5.0 # 5 seconds
    cpu_utilization_threshold    = 80  # 80% CPU
    memory_utilization_threshold = 85  # 85% memory
    disk_utilization_threshold   = 90  # 90% disk
  }
}

variable "dashboard_config" {
  description = "Dashboard configuration"
  type = object({
    refresh_interval   = string
    default_time_range = string
    enable_annotations = bool
  })

  default = {
    refresh_interval   = "5m"
    default_time_range = "1h"
    enable_annotations = true
  }
}

variable "log_config" {
  description = "Log collection configuration"
  type = object({
    enable_log_collection  = bool
    log_level              = string
    enable_structured_logs = bool
    log_parsing_enabled    = bool
  })

  default = {
    enable_log_collection  = true
    log_level              = "INFO"
    enable_structured_logs = true
    log_parsing_enabled    = true
  }
}

variable "notification_config" {
  description = "Notification configuration for alerts"
  type = object({
    enable_email_notifications   = bool
    enable_slack_notifications   = bool
    enable_webhook_notifications = bool
    notification_cooldown        = number
  })

  default = {
    enable_email_notifications   = false # Disabled for staging
    enable_slack_notifications   = false # Disabled for staging
    enable_webhook_notifications = false # Disabled for staging
    notification_cooldown        = 300   # 5 minutes
  }
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)

  default = {
    "Project"     = "EvalAP"
    "Environment" = "staging"
    "ManagedBy"   = "OpenTofu"
    "Component"   = "monitoring"
  }
}

variable "custom_metrics" {
  description = "Custom metrics to collect"
  type = list(object({
    name        = string
    unit        = string
    type        = string
    description = string
  }))

  default = [
    {
      name        = "evalap_experiments_total"
      unit        = "count"
      type        = "counter"
      description = "Total number of experiments created"
    },
    {
      name        = "evalap_models_evaluated"
      unit        = "count"
      type        = "counter"
      description = "Total number of models evaluated"
    },
    {
      name        = "evalap_evaluation_duration_seconds"
      unit        = "seconds"
      type        = "histogram"
      description = "Duration of model evaluations"
    }
  ]
}

variable "cost_optimization" {
  description = "Cost optimization settings for staging"
  type = object({
    enable_sampling    = bool
    sampling_rate      = number
    reduce_granularity = bool
  })

  default = {
    enable_sampling    = true
    sampling_rate      = 0.1 # Sample 10% of metrics for staging
    reduce_granularity = true
  }
}
