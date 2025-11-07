#!/bin/bash

# Staging Deployment Script
# Deploys EvalAP infrastructure to staging environment

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
STAGING_DIR="$PROJECT_ROOT/infra/staging"

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."

    # Check if OpenTofu is installed
    if ! command -v tofu &> /dev/null; then
        error "OpenTofu (tofu) is not installed or not in PATH"
    fi

    # Check if Scaleway CLI is installed (optional)
    if ! command -v scw &> /dev/null; then
        warn "Scaleway CLI (scw) is not installed. Some features may not work."
    fi

    # Check if we're in the right directory
    if [[ ! -d "$STAGING_DIR" ]]; then
        error "Staging directory not found: $STAGING_DIR"
    fi

    # Check if Terraform/OpenTofu files exist
    if [[ ! -f "$STAGING_DIR/main.tf" ]]; then
        error "main.tf not found in staging directory"
    fi

    # Check environment variables
    if [[ -z "${SCW_ACCESS_KEY:-}" ]]; then
        error "SCW_ACCESS_KEY environment variable is not set"
    fi

    if [[ -z "${SCW_SECRET_KEY:-}" ]]; then
        error "SCW_SECRET_KEY environment variable is not set"
    fi

    if [[ -z "${SCW_DEFAULT_PROJECT_ID:-}" ]]; then
        error "SCW_DEFAULT_PROJECT_ID environment variable is not set"
    fi

    log "Prerequisites check passed"
}

# Initialize OpenTofu
initialize_terraform() {
    log "Initializing OpenTofu..."

    cd "$STAGING_DIR"

    # Initialize OpenTofu
    tofu init

    log "OpenTofu initialization completed"
}

# Validate configuration
validate_configuration() {
    log "Validating OpenTofu configuration..."

    cd "$STAGING_DIR"

    # Validate OpenTofu configuration
    tofu validate

    # Check format
    tofu fmt -check

    log "Configuration validation passed"
}

# Plan deployment
plan_deployment() {
    log "Planning deployment..."

    cd "$STAGING_DIR"

    # Create plan
    tofu plan -out=staging.plan

    log "Deployment plan created"
}

# Apply deployment
apply_deployment() {
    log "Applying deployment to staging..."

    cd "$STAGING_DIR"

    # Apply the plan
    tofu apply -auto-approve staging.plan

    log "Deployment applied successfully"
}

# Run validation tests
run_validation() {
    log "Running validation tests..."

    cd "$PROJECT_ROOT"

    # Run staging deployment tests
    if command -v pytest &> /dev/null; then
        pytest tests/infra/test_staging_deployment.py -v
        pytest tests/infra/test_environment_isolation.py -v
    else
        warn "pytest not found. Skipping validation tests."
    fi

    log "Validation tests completed"
}

# Generate outputs
generate_outputs() {
    log "Generating deployment outputs..."

    cd "$STAGING_DIR"

    # Get outputs
    tofu output -json > "$STAGING_DIR/outputs.json"

    # Display key outputs
    echo ""
    info "=== Staging Deployment Outputs ==="

    if tofu output container_endpoints &> /dev/null; then
        echo "Service Endpoints:"
        tofu output container_endpoints
        echo ""
    fi

    if tofu output database_endpoint &> /dev/null; then
        echo "Database Endpoint:"
        tofu output database_endpoint
        echo ""
    fi

    if tofu output monitoring_endpoint &> /dev/null; then
        echo "Monitoring Dashboard:"
        tofu output monitoring_endpoint
        echo ""
    fi

    log "Outputs generated and saved to $STAGING_DIR/outputs.json"
}

# Cleanup function
cleanup() {
    log "Cleaning up temporary files..."

    cd "$STAGING_DIR"

    # Remove plan file
    if [[ -f "staging.plan" ]]; then
        rm -f staging.plan
    fi

    log "Cleanup completed"
}

# Health check function
health_check() {
    log "Performing health checks..."

    cd "$STAGING_DIR"

    # Get service endpoints
    if tofu output container_endpoints &> /dev/null; then
        local endpoints
        endpoints=$(tofu output -json container_endpoints | jq -r '.value | to_entries[] | "\(.key): \(.value)"')

        while IFS= read -r line; do
            if [[ -n "$line" ]]; then
                local service_name
                local endpoint
                service_name=$(echo "$line" | cut -d: -f1)
                endpoint=$(echo "$line" | cut -d: -f2- | xargs)  # xargs trims whitespace

                info "Checking $service_name service at $endpoint"

                # Check if endpoint is accessible (with timeout)
                if curl -f -s --max-time 30 "$endpoint/health" &> /dev/null; then
                    log "✅ $service_name service is healthy"
                else
                    warn "⚠️  $service_name service health check failed"
                fi
            fi
        done <<< "$endpoints"
    fi

    log "Health checks completed"
}

# Main deployment function
deploy_staging() {
    log "Starting staging deployment..."

    # Check prerequisites
    check_prerequisites

    # Initialize OpenTofu
    initialize_terraform

    # Validate configuration
    validate_configuration

    # Plan deployment
    plan_deployment

    # Apply deployment
    apply_deployment

    # Generate outputs
    generate_outputs

    # Run health checks
    health_check

    # Run validation tests
    run_validation

    log "✅ Staging deployment completed successfully!"
}

# Destroy function
destroy_staging() {
    warn "This will destroy all staging infrastructure. Are you sure?"
    read -p "Type 'destroy' to confirm: " confirmation

    if [[ "$confirmation" != "destroy" ]]; then
        error "Destruction cancelled"
    fi

    log "Destroying staging infrastructure..."

    cd "$STAGING_DIR"

    # Destroy infrastructure
    tofu destroy -auto-approve

    log "✅ Staging infrastructure destroyed"
}

# Show usage
usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy    Deploy staging infrastructure (default)"
    echo "  destroy   Destroy staging infrastructure"
    echo "  plan      Show deployment plan"
    echo "  validate  Validate configuration"
    echo "  outputs   Show deployment outputs"
    echo "  health    Run health checks"
    echo "  help      Show this help message"
    echo ""
    echo "Environment variables required:"
    echo "  SCW_ACCESS_KEY           Scaleway access key"
    echo "  SCW_SECRET_KEY           Scaleway secret key"
    echo "  SCW_DEFAULT_PROJECT_ID   Scaleway project ID"
}

# Main script logic
main() {
    local command="${1:-deploy}"

    case "$command" in
        "deploy")
            deploy_staging
            ;;
        "destroy")
            destroy_staging
            ;;
        "plan")
            check_prerequisites
            initialize_terraform
            plan_deployment
            ;;
        "validate")
            check_prerequisites
            initialize_terraform
            validate_configuration
            ;;
        "outputs")
            check_prerequisites
            initialize_terraform
            generate_outputs
            ;;
        "health")
            check_prerequisites
            initialize_terraform
            health_check
            ;;
        "help"|"-h"|"--help")
            usage
            ;;
        *)
            error "Unknown command: $command. Use 'help' for usage information."
            ;;
    esac

    # Cleanup on successful completion
    if [[ "$command" != "help" && "$command" != "-h" && "$command" != "--help" ]]; then
        cleanup
    fi
}

# Trap cleanup on exit
trap cleanup EXIT

# Run main function with all arguments
main "$@"
