# Staging Container Outputs

output "service_endpoints" {
  description = "Container service endpoints"
  value = {
    documentation = "https://${scaleway_container.documentation.domain_name}"
    runners       = "https://${scaleway_container.runners.domain_name}"
    streamlit     = "https://${scaleway_container.streamlit.domain_name}"
  }
}

output "container_ids" {
  description = "Container resource IDs"
  value = {
    documentation = scaleway_container.documentation.id
    runners       = scaleway_container.runners.id
    streamlit     = scaleway_container.streamlit.id
  }
}

output "container_names" {
  description = "Container names"
  value = {
    documentation = scaleway_container.documentation.name
    runners       = scaleway_container.runners.name
    streamlit     = scaleway_container.streamlit.name
  }
}

output "namespace_id" {
  description = "Container namespace ID"
  value       = scaleway_container_namespace.staging.id
}

output "namespace_name" {
  description = "Container namespace name"
  value       = scaleway_container_namespace.staging.name
}

output "registry_id" {
  description = "Container registry ID - removed as scaleway_registry resource is not supported"
  value       = null
}

output "registry_namespace_id" {
  description = "Container registry namespace ID"
  value       = scaleway_registry_namespace.main.id
}

output "container_status" {
  description = "Container deployment status"
  value = {
    documentation = scaleway_container.documentation.status
    runners       = scaleway_container.runners.status
    streamlit     = scaleway_container.streamlit.status
  }
}

output "container_urls" {
  description = "Full container URLs with protocol"
  value = {
    documentation = "https://${scaleway_container.documentation.domain_name}"
    runners       = "https://${scaleway_container.runners.domain_name}"
    streamlit     = "https://${scaleway_container.streamlit.domain_name}"
  }
}

output "health_endpoints" {
  description = "Health check endpoints"
  value = {
    documentation = "https://${scaleway_container.documentation.domain_name}/health"
    runners       = "https://${scaleway_container.runners.domain_name}/health"
    streamlit     = "https://${scaleway_container.streamlit.domain_name}/_stcore/health"
  }
}

output "container_config" {
  description = "Current container configuration"
  value = {
    documentation = {
      port         = scaleway_container.documentation.port
      cpu_limit    = scaleway_container.documentation.cpu_limit
      memory_limit = scaleway_container.documentation.memory_limit
      min_scale    = scaleway_container.documentation.min_scale
      max_scale    = scaleway_container.documentation.max_scale
    }
    runners = {
      port         = scaleway_container.runners.port
      cpu_limit    = scaleway_container.runners.cpu_limit
      memory_limit = scaleway_container.runners.memory_limit
      min_scale    = scaleway_container.runners.min_scale
      max_scale    = scaleway_container.runners.max_scale
    }
    streamlit = {
      port         = scaleway_container.streamlit.port
      cpu_limit    = scaleway_container.streamlit.cpu_limit
      memory_limit = scaleway_container.streamlit.memory_limit
      min_scale    = scaleway_container.streamlit.min_scale
      max_scale    = scaleway_container.streamlit.max_scale
    }
  }
}

output "trigger_ids" {
  description = "Container trigger IDs - disabled due to removed registry dependency"
  value = {
    documentation = null
    runners       = null
    streamlit     = null
  }
}

output "environment_variables" {
  description = "Container environment variables"
  value = {
    documentation = scaleway_container.documentation.environment_variables
    runners       = scaleway_container.runners.environment_variables
    streamlit     = scaleway_container.streamlit.environment_variables
  }
}

output "scaling_config" {
  description = "Auto-scaling configuration"
  value = {
    documentation = {
      min_scale = scaleway_container.documentation.min_scale
      max_scale = scaleway_container.documentation.max_scale
    }
    runners = {
      min_scale = scaleway_container.runners.min_scale
      max_scale = scaleway_container.runners.max_scale
    }
    streamlit = {
      min_scale = scaleway_container.streamlit.min_scale
      max_scale = scaleway_container.streamlit.max_scale
    }
  }
}
