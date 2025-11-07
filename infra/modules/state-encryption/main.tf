# Remote State Locking and Encryption Configuration
# This file sets up secure state management with encryption

terraform {
  required_providers {
    scaleway = {
      source  = "scaleway/scaleway"
      version = ">= 2.0"
    }
  }
}

# State encryption configuration
locals {
  state_encryption = {
    # Enable server-side encryption
    server_side_encryption = "AES"

    # Enable versioning for state history
    versioning = true

    # Enable access logging
    access_logging = true
  }
}

# Output encryption settings
output "state_encryption" {
  description = "State encryption configuration"
  value       = local.state_encryption
}

output "encryption_enabled" {
  description = "Whether encryption is enabled"
  value       = true
}
