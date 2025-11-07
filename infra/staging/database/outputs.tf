# Staging Database Outputs

output "instance_id" {
  description = "Database instance ID"
  value       = scaleway_rdb_instance.staging.id
}

output "instance_name" {
  description = "Database instance name"
  value       = scaleway_rdb_instance.staging.name
}

output "node_type" {
  description = "Database instance type"
  value       = scaleway_rdb_instance.staging.node_type
}

output "engine" {
  description = "Database engine and version"
  value       = scaleway_rdb_instance.staging.engine
}

output "storage_size" {
  description = "Database storage size in GB"
  value       = scaleway_rdb_instance.staging.volume_size_in_gb
}

output "database_name" {
  description = "Database name"
  value       = scaleway_rdb_database.evalap.name
}

output "username" {
  description = "Database username"
  value       = scaleway_rdb_user.evalap.name
}

output "connection_string" {
  description = "Database connection string"
  value       = "postgresql://${scaleway_rdb_user.evalap.name}:${var.database_password}@${scaleway_rdb_instance.staging.endpoint_ip}:${scaleway_rdb_instance.staging.endpoint_port}/${scaleway_rdb_database.evalap.name}"
  sensitive   = true
}

output "backup_enabled" {
  description = "Whether backup is enabled"
  value       = !scaleway_rdb_instance.staging.disable_backup
}

output "ha_enabled" {
  description = "Whether high availability is enabled"
  value       = scaleway_rdb_instance.staging.is_ha_cluster
}

output "replica_count" {
  description = "Number of read replicas"
  value       = scaleway_rdb_instance.staging.is_ha_cluster ? 1 : 0
}
