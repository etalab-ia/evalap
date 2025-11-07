# Staging Environment Configuration
# Deploys complete EvalAP infrastructure to staging for safe testing

terraform {
  required_version = ">= 1.0"

  required_providers {
    scaleway = {
      source  = "scaleway/scaleway"
      version = ">= 2.0"
    }
  }

  # Staging backend configuration
  backend "s3" {
    bucket = "evalap-terraform-state"
    key    = "staging/terraform.tfstate"
    region = "fr-par"

    # Scaleway S3-compatible configuration
    endpoint = "s3.fr-par.scw.cloud"

    # Security settings
    encrypt                     = true
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    force_path_style            = true

    # State locking (using Object Storage's built-in locking)
    # Note: Scaleway Object Storage provides atomic operations
    # that can be used for basic state locking
  }
}

# Provider configuration
provider "scaleway" {
  zone   = "fr-par-2"
  region = "fr-par"
}

# Regional provider aliases for multi-region resources
provider "scaleway" {
  alias  = "par"
  zone   = "fr-par-2"
  region = "fr-par"
}

provider "scaleway" {
  alias  = "ams"
  zone   = "nl-ams-2"
  region = "nl-ams"
}

provider "scaleway" {
  alias  = "waw"
  zone   = "pl-waw-2"
  region = "pl-waw"
}

# Local values for configuration
locals {
  environment = "staging"
  tags = {
    "Project"     = "EvalAP"
    "Environment" = "staging"
    "ManagedBy"   = "OpenTofu"
  }
}

# Staging modules
module "networking" {
  source = "../_common"

  environment    = local.environment
  project_id     = var.project_id
  default_region = var.default_region
  default_zone   = var.default_zone
}

module "container" {
  source = "./container"

  environment = local.environment
  project_id  = var.project_id

  # Staging-specific configuration
  container_config = {
    documentation = {
      image     = "evalap/documentation:latest"
      port      = 8080
      cpu       = 256
      memory    = 512
      min_scale = 0
      max_scale = 1
      protocol  = "HTTP"
    }
    runners = {
      image     = "evalap/runners:latest"
      port      = 8081
      cpu       = 512
      memory    = 1024
      min_scale = 0
      max_scale = 1
      protocol  = "HTTP"
    }
    streamlit = {
      image     = "evalap/streamlit:latest"
      port      = 8501
      cpu       = 256
      memory    = 512
      min_scale = 0
      max_scale = 1
      protocol  = "HTTP"
    }
  }

  # Required attributes
  private_network_id = module.networking.private_network_id

  tags = local.tags
}

module "database" {
  source = "./database"

  environment = local.environment
  project_id  = var.project_id
  region      = var.default_region

  # Staging database configuration
  node_type = "db-dev-s"
  storage   = "10GB"

  # Staging doesn't need HA (single instance is fine for testing)
  enable_ha = false

  # Required attributes
  database_password  = var.database_password
  private_network_id = module.networking.private_network_id

  tags = local.tags
}

module "secrets" {
  source = "./secrets"

  environment = local.environment
  project_id  = var.project_id
  region      = var.default_region

  # Staging secrets configuration
  secret_names = [
    "database_url",
    "api_key",
    "jwt_secret"
  ]

  # Required secret values
  database_url = var.database_url
  api_key      = var.api_key
  jwt_secret   = var.jwt_secret

  tags = local.tags
}

module "monitoring" {
  source = "./monitoring"

  environment = local.environment
  project_id  = var.project_id
  region      = var.default_region

  # Container IDs for monitoring
  documentation_container_id = module.container.container_ids.documentation
  runners_container_id       = module.container.container_ids.runners
  streamlit_container_id     = module.container.container_ids.streamlit

  # Database ID for monitoring
  database_id = module.database.instance_id

  # Staging monitoring configuration
  enable_alerts  = false # No alerts needed for staging
  retention_days = 7     # Shorter retention for staging

  tags = local.tags
}

# Outputs for staging deployment
output "container_endpoints" {
  description = "Container service endpoints"
  value       = module.container.service_endpoints
}

output "database_endpoint" {
  description = "Database connection endpoint"
  value       = module.database.endpoint
}

output "database_connection_string" {
  description = "Database connection string"
  value       = module.database.connection_string
  sensitive   = true
}

output "secrets_manager_id" {
  description = "Secrets manager ID"
  value       = module.secrets.manager_id
}

output "monitoring_endpoint" {
  description = "Monitoring dashboard endpoint"
  value       = module.monitoring.dashboard_endpoint
}

output "vpc_id" {
  description = "VPC ID"
  value       = module.networking.vpc_id
}

output "private_network_id" {
  description = "Private network ID"
  value       = module.networking.private_network_id
}

output "security_group_id" {
  description = "Security group ID"
  value       = module.networking.security_group_id
}

output "deployment_timestamp" {
  description = "Deployment timestamp"
  value       = timestamp()
}

output "environment" {
  description = "Environment name"
  value       = local.environment
}
