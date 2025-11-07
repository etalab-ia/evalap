# Staging Container Module
# Deploys serverless containers for EvalAP services

terraform {
  required_providers {
    scaleway = {
      source  = "scaleway/scaleway"
      version = ">= 2.0"
    }
  }
}

# Container namespace for all services
resource "scaleway_container_namespace" "staging" {
  name        = "evalap-staging"
  description = "EvalAP staging container namespace"
  region      = var.region

  tags = values(var.tags)
}

# Documentation service container
resource "scaleway_container" "documentation" {
  name         = "evalap-documentation-staging"
  description  = "Documentation service for staging"
  namespace_id = scaleway_container_namespace.staging.id
  region       = var.region

  registry_image = var.container_config["documentation"]["image"]
  command        = ["npm", "start"]

  cpu_limit    = var.container_config["documentation"]["cpu"]
  memory_limit = var.container_config["documentation"]["memory"]

  min_scale = var.container_config["documentation"]["min_scale"]
  max_scale = var.container_config["documentation"]["max_scale"]

  protocol = var.container_config["documentation"]["protocol"]
  port     = var.container_config["documentation"]["port"]

  # Environment variables
  environment_variables = {
    NODE_ENV = "staging"
    PORT     = tostring(var.container_config["documentation"]["port"])
  }

  # Health check
  health_check {
    http {
      path = "/health"
    }
    interval          = "30s"
    failure_threshold = 3
  }

  # Privacy settings (public for staging)
  privacy = "public"

  tags = merge(var.tags, {
    "Service" = "documentation"
  })

  depends_on = [scaleway_container_namespace.staging]
}

# Runners service container
resource "scaleway_container" "runners" {
  name         = "evalap-runners-staging"
  description  = "Runners service for staging"
  namespace_id = scaleway_container_namespace.staging.id
  region       = var.region

  registry_image = var.container_config["runners"]["image"]
  command        = ["python", "-m", "evalap.runners"]

  cpu_limit    = var.container_config["runners"]["cpu"]
  memory_limit = var.container_config["runners"]["memory"]

  min_scale = var.container_config["runners"]["min_scale"]
  max_scale = var.container_config["runners"]["max_scale"]

  protocol = var.container_config["runners"]["protocol"]
  port     = var.container_config["runners"]["port"]

  # Environment variables
  environment_variables = {
    PYTHONPATH = "/app"
    LOG_LEVEL  = "INFO"
  }

  # Health check
  health_check {
    http {
      path = "/health"
    }
    interval          = "30s"
    failure_threshold = 3
  }

  # Privacy settings (public for staging)
  privacy = "public"

  tags = merge(var.tags, {
    "Service" = "runners"
  })

  depends_on = [scaleway_container_namespace.staging]
}

# Streamlit service container
resource "scaleway_container" "streamlit" {
  name         = "evalap-streamlit-staging"
  description  = "Streamlit UI service for staging"
  namespace_id = scaleway_container_namespace.staging.id
  region       = var.region

  registry_image = var.container_config["streamlit"]["image"]
  command        = ["streamlit", "run", "ui/streamlit_app.py", "--server.port=8501"]

  cpu_limit    = var.container_config["streamlit"]["cpu"]
  memory_limit = var.container_config["streamlit"]["memory"]

  min_scale = var.container_config["streamlit"]["min_scale"]
  max_scale = var.container_config["streamlit"]["max_scale"]

  protocol = var.container_config["streamlit"]["protocol"]
  port     = var.container_config["streamlit"]["port"]

  # Environment variables
  environment_variables = {
    STREAMLIT_SERVER_PORT    = tostring(var.container_config["streamlit"]["port"])
    STREAMLIT_SERVER_ADDRESS = "0.0.0.0"
  }

  # Health check
  health_check {
    http {
      path = "/_stcore/health"
    }
    interval          = "30s"
    failure_threshold = 3
  }

  # Privacy settings (public for staging)
  privacy = "public"

  tags = merge(var.tags, {
    "Service" = "streamlit"
  })

  depends_on = [scaleway_container_namespace.staging]
}

# Container triggers for deployment - commented out due to schema issues
# resource "scaleway_container_trigger" "documentation_deploy" {
#   name         = "documentation-deploy-trigger"
#   namespace_id = scaleway_container_namespace.staging.id
#   region       = var.region
#
#   container_id = scaleway_container.documentation.id
#
#   # Trigger on registry events (for future CI/CD integration)
#   # registry {
#   #   registry_id = scaleway_registry.main.id
#   #   image_name  = "documentation"
#   #   tag         = "latest"
#   # }
#
#   depends_on = [
#     scaleway_container_namespace.staging,
#     scaleway_container.documentation
#   ]
# }

# resource "scaleway_container_trigger" "runners_deploy" {
#   name         = "runners-deploy-trigger"
#   namespace_id = scaleway_container_namespace.staging.id
#   region       = var.region
#
#   container_id = scaleway_container.runners.id
#
#   # Trigger on registry events
#   # registry {
#   #   registry_id = scaleway_registry.main.id
#   #   image_name  = "runners"
#   #   tag         = "latest"
#   # }
#
#   depends_on = [
#     scaleway_container_namespace.staging,
#     scaleway_container.runners
#   ]
# }

# resource "scaleway_container_trigger" "streamlit_deploy" {
#   name         = "streamlit-deploy-trigger"
#   namespace_id = scaleway_container_namespace.staging.id
#   region       = var.region
#
#   container_id = scaleway_container.streamlit.id
#
#   # Trigger on registry events
#   # registry {
#   #   registry_id = scaleway_registry.main.id
#   #   image_name  = "streamlit"
#   #   tag         = "latest"
#   # }
#
#   depends_on = [
#     scaleway_container_namespace.staging,
#     scaleway_container.streamlit
#   ]
# }

# Container registry for images
resource "scaleway_registry_namespace" "main" {
  name        = "evalap-staging-registry"
  description = "EvalAP staging container registry"
  region      = var.region
}

# Note: scaleway_registry resource removed - not supported by provider

# Outputs are defined in outputs.tf
