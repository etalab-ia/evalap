# Staging Database Module
# Deploys managed PostgreSQL database for staging

terraform {
  required_providers {
    scaleway = {
      source  = "scaleway/scaleway"
      version = ">= 2.0"
    }
  }
}

# Database instance for staging
resource "scaleway_rdb_instance" "staging" {
  name           = "evalap-staging-db"
  engine         = "PostgreSQL-15"
  node_type      = var.node_type
  region         = var.region
  disable_backup = false
  is_ha_cluster  = var.enable_ha

  # Storage configuration
  volume_size_in_gb = 10 # Small storage for staging

  # Network configuration
  private_network {
    pn_id       = var.private_network_id
    enable_ipam = true
  }

  # Database settings
  settings = {
    max_connections            = 50
    log_statement              = "all"
    log_min_duration_statement = 1000 # Log queries > 1s
  }

  tags = merge(var.tags, {
    "Component" = "database"
    "Engine"    = "postgresql"
  })
}

# Database for the application
resource "scaleway_rdb_database" "evalap" {
  instance_id = scaleway_rdb_instance.staging.id
  name        = "evalap_staging"

  # Import initial schema if needed
  # managed = false  # Set to true if we want Terraform to manage schema
}

# Database user for the application
resource "scaleway_rdb_user" "evalap" {
  instance_id = scaleway_rdb_instance.staging.id
  name        = "evalap"
  password    = var.database_password
  is_admin    = false

  # Grant permissions on the database
  depends_on = [scaleway_rdb_database.evalap]
}

# Grant user permissions on database
resource "scaleway_rdb_privilege" "evalap_db" {
  instance_id   = scaleway_rdb_instance.staging.id
  database_name = scaleway_rdb_database.evalap.name
  user_name     = scaleway_rdb_user.evalap.name
  permission    = "all"

  depends_on = [
    scaleway_rdb_database.evalap,
    scaleway_rdb_user.evalap
  ]
}
