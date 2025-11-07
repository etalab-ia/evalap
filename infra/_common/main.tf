# Base Terraform Configuration
# This file provides the foundation for all infrastructure modules

# Base networking configuration
resource "scaleway_vpc" "main" {
  name = "${local.resource_name}vpc"

  tags = local.standard_tags
}

# Private networks for each environment
resource "scaleway_vpc_private_network" "main" {
  name   = "${local.resource_name}private-network"
  vpc_id = scaleway_vpc.main.id

  tags = local.standard_tags
}

# Base security group
resource "scaleway_instance_security_group" "main" {
  name = "${local.resource_name}sg"

  # Allow SSH from specific IPs (if needed)
  inbound_rule {
    action   = "accept"
    port     = 22
    ip_range = "0.0.0.0/0" # Restrict in production
  }

  # Allow HTTP/HTTPS for services
  inbound_rule {
    action   = "accept"
    port     = 80
    ip_range = "0.0.0.0/0"
  }

  inbound_rule {
    action   = "accept"
    port     = 443
    ip_range = "0.0.0.0/0"
  }

  # Allow PostgreSQL within VPC
  inbound_rule {
    action   = "accept"
    port     = 5432
    ip_range = scaleway_vpc_private_network.main.ipv4_subnet
  }

  outbound_rule {
    action   = "accept"
    port     = 0
    ip_range = "0.0.0.0/0"
  }

  tags = local.standard_tags
}

# Common outputs
output "vpc_id" {
  description = "ID of the main VPC"
  value       = scaleway_vpc.main.id
}

output "private_network_id" {
  description = "ID of the private network"
  value       = scaleway_vpc_private_network.main.id
}

output "security_group_id" {
  description = "ID of the main security group"
  value       = scaleway_instance_security_group.main.id
}

output "standard_tags" {
  description = "Standard tags applied to resources"
  value       = local.standard_tags
}
