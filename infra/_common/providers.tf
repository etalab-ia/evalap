# Common Provider Configuration
# This file contains shared provider settings for all environments

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
}

# Default Scaleway provider configuration
provider "scaleway" {
  region     = var.default_region
  zone       = var.default_zone
  project_id = var.project_id
}

# Additional provider configurations for multi-region deployments
provider "scaleway" {
  alias      = "ams"
  region     = "nl-ams"
  zone       = "nl-ams-1"
  project_id = var.project_id
}

provider "scaleway" {
  alias      = "waw"
  region     = "pl-waw"
  zone       = "pl-waw-2"
  project_id = var.project_id
}

# Common locals for all environments
locals {
  # Standard tags applied to all resources
  standard_tags = merge(
    {
      "Project"     = "EvalAP"
      "Environment" = var.environment
      "ManagedBy"   = "OpenTofu"
      "CreatedAt"   = timestamp()
    },
    var.extra_tags
  )

  # Common naming convention
  naming_convention = {
    prefix    = "${var.project_name}-${var.environment}"
    separator = "-"
  }

  # Resource naming helper
  resource_name = "${local.naming_convention.prefix}${local.naming_convention.separator}"
}
