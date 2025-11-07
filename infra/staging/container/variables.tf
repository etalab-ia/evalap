# Staging Container Variables

variable "environment" {
  description = "Environment name (staging)"
  type        = string
}

variable "project_id" {
  description = "Scaleway project ID"
  type        = string
}

variable "region" {
  description = "Scaleway region"
  type        = string
  default     = "fr-par"
}

variable "zone" {
  description = "Scaleway availability zone"
  type        = string
  default     = "fr-par-2"
}

variable "container_config" {
  description = "Container configuration for services"
  type = object({
    documentation = object({
      image     = string
      port      = number
      cpu       = number
      memory    = number
      min_scale = number
      max_scale = number
      protocol  = string
    })
    runners = object({
      image     = string
      port      = number
      cpu       = number
      memory    = number
      min_scale = number
      max_scale = number
      protocol  = string
    })
    streamlit = object({
      image     = string
      port      = number
      cpu       = number
      memory    = number
      min_scale = number
      max_scale = number
      protocol  = string
    })
  })

  default = {
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
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)

  default = {
    "Project"     = "EvalAP"
    "Environment" = "staging"
    "ManagedBy"   = "OpenTofu"
  }
}

variable "private_network_id" {
  description = "Private network ID for containers"
  type        = string
}

variable "private_network_cidr" {
  description = "Private network CIDR block"
  type        = string
  default     = "10.0.0.0/24"
}

variable "security_group_rules" {
  description = "Security group rules for containers"
  type = list(object({
    action   = string
    port     = number
    protocol = string
    ip_range = string
  }))

  default = [
    {
      action   = "accept"
      port     = 80
      protocol = "TCP"
      ip_range = "0.0.0.0/0"
    },
    {
      action   = "accept"
      port     = 443
      protocol = "TCP"
      ip_range = "0.0.0.0/0"
    },
    {
      action   = "accept"
      port     = 8080
      protocol = "TCP"
      ip_range = "0.0.0.0/0"
    },
    {
      action   = "accept"
      port     = 8081
      protocol = "TCP"
      ip_range = "0.0.0.0/0"
    },
    {
      action   = "accept"
      port     = 8501
      protocol = "TCP"
      ip_range = "0.0.0.0/0"
    }
  ]
}

variable "health_check_config" {
  description = "Health check configuration for containers"
  type = object({
    path             = string
    interval_seconds = number
    timeout_seconds  = number
    retry_count      = number
  })

  default = {
    path             = "/health"
    interval_seconds = 30
    timeout_seconds  = 10
    retry_count      = 3
  }
}

variable "scaling_config" {
  description = "Auto-scaling configuration"
  type = object({
    enable_auto_scaling = bool
    cpu_threshold       = number
    memory_threshold    = number
    scale_up_cooldown   = number
    scale_down_cooldown = number
  })

  default = {
    enable_auto_scaling = false # Disabled for staging
    cpu_threshold       = 80
    memory_threshold    = 80
    scale_up_cooldown   = 300
    scale_down_cooldown = 300
  }
}
