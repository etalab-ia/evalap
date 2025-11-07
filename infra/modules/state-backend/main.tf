# Scaleway Object Storage Backend Configuration
# This file configures the remote state backend for OpenTofu

terraform {
  required_providers {
    scaleway = {
      source  = "scaleway/scaleway"
      version = ">= 2.0"
    }
  }

  backend "s3" {
    # Bucket configuration
    bucket = var.state_bucket_name

    # State file configuration
    key = "${var.environment}/terraform.tfstate"

    # Scaleway S3-compatible configuration
    region   = var.default_region
    endpoint = "s3.${var.default_region}.scw.cloud"

    # Authentication and security
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    force_path_style            = true
    encrypt                     = true

    # State locking configuration
    dynamodb_table    = var.state_lock_table
    dynamodb_endpoint = "dynamodb.${var.default_region}.scw.cloud"

    # Additional settings
    skip_region_validation = true
    skip_s3_checksum       = true
  }
}

# Create the S3 bucket for state storage
resource "scaleway_object_bucket" "terraform_state" {
  name   = var.state_bucket_name
  region = var.default_region

  tags = merge(var.tags, {
    "Purpose" = "Terraform State Storage"
  })
}

# Note: Scaleway doesn't have a managed DynamoDB service
# State locking will be handled via Object Storage locking mechanism
# This is a limitation of Scaleway's current offerings
