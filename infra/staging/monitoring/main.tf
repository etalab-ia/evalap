# Staging Monitoring Module
# Configures monitoring and alerting for staging environment

terraform {
  required_providers {
    scaleway = {
      source  = "scaleway/scaleway"
      version = ">= 2.0"
    }
  }
}

# Note: Monitoring will be configured at the project level
# Individual service metrics are collected automatically

# Create logs data source
resource "scaleway_cockpit_source" "staging_logs" {
  project_id     = var.project_id
  name           = "evalap-staging-logs"
  type           = "logs"
  retention_days = var.retention_days
}

# Outputs
output "logs_source_id" {
  description = "Logs source ID"
  value       = scaleway_cockpit_source.staging_logs.id
}

output "monitoring_enabled" {
  description = "Whether monitoring is enabled"
  value       = true
}

output "alerts_enabled" {
  description = "Whether alerts are enabled"
  value       = var.enable_alerts
}

output "retention_days" {
  description = "Data retention period in days"
  value       = var.retention_days
}

output "dashboard_endpoint" {
  description = "Monitoring dashboard endpoint"
  value       = "https://console.scaleway.com/cockpit/monitoring/${var.project_id}"
}
