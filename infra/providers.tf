# Scaleway Provider Configuration
# This file configures additional Scaleway providers for different regions

# Provider configuration for Amsterdam region
provider "scaleway" {
  alias  = "ams"
  region = "nl-ams"
  zone   = "nl-ams-1"

  project_id = var.project_id
}

# Provider configuration for Warsaw region
provider "scaleway" {
  alias  = "waw"
  region = "pl-waw"
  zone   = "pl-waw-2"

  project_id = var.project_id
}
