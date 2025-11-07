# Main OpenTofu configuration
# This file contains the core configuration for Scaleway infrastructure

terraform {
  required_version = ">= 1.0"

  required_providers {
    scaleway = {
      source  = "scaleway/scaleway"
      version = ">= 2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
    time = {
      source  = "hashicorp/time"
      version = ">= 0.9"
    }
  }

  backend "s3" {
    bucket = "evalap-terraform-state"
    key    = "infra/terraform.tfstate"
    region = "fr-par"

    # Scaleway S3-compatible configuration
    endpoint = "s3.fr-par.scw.cloud"

    # State locking and encryption
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    force_path_style            = true

    # Enable state locking
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

# Configure Scaleway provider
provider "scaleway" {
  zone       = var.default_zone
  region     = var.default_region
  project_id = var.project_id
}

# Common locals
locals {
  tags = {
    "Project"     = "EvalAP"
    "Environment" = var.environment
    "ManagedBy"   = "OpenTofu"
  }
}

# Common outputs for all environments
output "project_id" {
  description = "Scaleway Project ID"
  value       = var.project_id
  sensitive   = true
}

output "environment" {
  description = "Current environment"
  value       = var.environment
}
