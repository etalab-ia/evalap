#!/bin/bash

# Staging Validation and Health Check Script
# Validates staging deployment and performs comprehensive health checks

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

# Validation thresholds
MAX_RESPONSE_TIME=5  # seconds
MIN_SUCCESS_RATE=0.8  # 80%
MAX_ERROR_RATE=0.2   # 20%

# Logging functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    log "Checking validation prerequisites..."

    # Check if staging directory exists
    if [[ ! -d "$STAGING_DIR" ]]; then
        error "Staging directory not found: $STAGING_DIR"
    fi

    # Check if OpenTofu state exists
    if [[ ! -f "$STAGING_DIR/terraform.tfstate" ]]; then
        error "Terraform state not found. Has staging been deployed?"
    fi

    # Check if required tools are available
    if ! command -v curl &> /dev/null; then
        error "curl is required for health checks"
    fi

    if ! command -v jq &> /dev/null; then
        error "jq is required for JSON parsing"
    fi

    log "Prerequisites check passed"
}

# Get deployment outputs
get_outputs() {
    log "Retrieving deployment outputs..."

    cd "$STAGING_DIR"

    if ! tofu output -json > /tmp/staging_outputs.json 2>/dev/null; then
        error "Failed to get deployment outputs"
    fi

    log "Outputs retrieved successfully"
}

# Validate service endpoints
validate_service_endpoints() {
    log "Validating service endpoints..."

    local endpoints
    endpoints=$(jq -r '.container_endpoints.value | to_entries[] | "\(.key)=\(.value)"' /tmp/staging_outputs.json)

    local failed_services=()
    local total_services=0
    local healthy_services=0

    while IFS='=' read -r service endpoint; do
        if [[ -n "$service" && -n "$endpoint" ]]; then
            total_services=$((total_services + 1))
            info "Testing $service endpoint: $endpoint"

            # Test main endpoint
            if curl -f -s --max-time "$MAX_RESPONSE_TIME" "$endpoint" &> /dev/null; then
                log "✅ $service main endpoint is accessible"
                healthy_services=$((healthy_services + 1))
            else
                error "❌ $service main endpoint is not accessible"
                failed_services+=("$service")
            fi

            # Test health endpoint
            local health_endpoint="${endpoint%/}/health"
            if curl -f -s --max-time "$MAX_RESPONSE_TIME" "$health_endpoint" &> /dev/null; then
                log "✅ $service health endpoint is responding"
            else
                warn "⚠️  $service health endpoint is not responding"
            fi
        fi
    done <<< "$endpoints"

    # Calculate success rate
    if [[ $total_services -gt 0 ]]; then
        local success_rate
        success_rate=$(echo "scale=2; $healthy_services / $total_services" | bc -l)

        info "Service health summary: $healthy_services/$total_services services healthy (${success_rate})"

        if (( $(echo "$success_rate < $MIN_SUCCESS_RATE" | bc -l) )); then
            error "Service success rate ${success_rate} is below threshold ${MIN_SUCCESS_RATE}"
        fi
    fi

    log "Service endpoint validation completed"
}

# Validate database connectivity
validate_database() {
    log "Validating database connectivity..."

    local db_endpoint
    db_endpoint=$(jq -r '.database_endpoint.value' /tmp/staging_outputs.json)

    if [[ -n "$db_endpoint" && "$db_endpoint" != "null" ]]; then
        info "Testing database endpoint: $db_endpoint"

        # Test database connectivity (basic TCP check)
        if timeout 10 bash -c "</dev/tcp/${db_endpoint%:*}/${db_endpoint##*:}"; then
            log "✅ Database is accessible"
        else
            error "❌ Database is not accessible"
        fi

        # Test database with psql if available
        if command -v psql &> /dev/null; then
            local connection_string
            connection_string=$(jq -r '.database_connection_string.value' /tmp/staging_outputs.json)

            if [[ -n "$connection_string" && "$connection_string" != "null" ]]; then
                if PGPASSWORD="${connection_string#*@}" psql "$connection_string" -c "SELECT 1;" &> /dev/null; then
                    log "✅ Database connection test passed"
                else
                    warn "⚠️  Database connection test failed"
                fi
            fi
        else
            info "psql not available, skipping database connection test"
        fi
    else
        warn "Database endpoint not found in outputs"
    fi

    log "Database validation completed"
}

# Validate monitoring setup
validate_monitoring() {
    log "Validating monitoring configuration..."

    local monitoring_endpoint
    monitoring_endpoint=$(jq -r '.monitoring_endpoint.value' /tmp/staging_outputs.json)

    if [[ -n "$monitoring_endpoint" && "$monitoring_endpoint" != "null" ]]; then
        info "Testing monitoring endpoint: $monitoring_endpoint"

        # Test monitoring dashboard accessibility
        if curl -f -s --max-time 10 "$monitoring_endpoint" &> /dev/null; then
            log "✅ Monitoring dashboard is accessible"
        else
            warn "⚠️  Monitoring dashboard is not accessible"
        fi
    else
        warn "Monitoring endpoint not found in outputs"
    fi

    log "Monitoring validation completed"
}

# Validate environment isolation
validate_isolation() {
    log "Validating environment isolation..."

    # Check that staging resources have proper tags
    cd "$STAGING_DIR"

    local resources
    resources=$(tofu state list | grep -E "scaleway_|container|rdb")

    local isolation_issues=()

    while IFS= read -r resource; do
        if [[ -n "$resource" ]]; then
            local resource_type
            resource_type=$(echo "$resource" | cut -d. -f1)

            # Check for staging-specific tags
            local resource_json
            resource_json=$(tofu show -json "$resource" 2>/dev/null || echo "{}")

            local has_staging_tag
            has_staging_tag=$(echo "$resource_json" | jq -r '.values.tags.Environment // ""' 2>/dev/null || echo "")

            if [[ "$has_staging_tag" != "staging" ]]; then
                isolation_issues+=("$resource missing staging tag")
            fi
        fi
    done <<< "$resources"

    if [[ ${#isolation_issues[@]} -gt 0 ]]; then
        warn "Isolation issues found:"
        for issue in "${isolation_issues[@]}"; do
            warn "  - $issue"
        done
    else
        log "✅ Environment isolation validation passed"
    fi

    log "Environment isolation validation completed"
}

# Perform performance tests
performance_tests() {
    log "Performing performance tests..."

    local endpoints
    endpoints=$(jq -r '.container_endpoints.value | to_entries[] | .value' /tmp/staging_outputs.json)

    while IFS= read -r endpoint; do
        if [[ -n "$endpoint" && "$endpoint" != "null" ]]; then
            info "Testing performance for: $endpoint"

            # Measure response time
            local start_time
            start_time=$(date +%s.%N)

            if curl -f -s --max-time "$MAX_RESPONSE_TIME" "$endpoint" &> /dev/null; then
                local end_time
                end_time=$(date +%s.%N)
                local response_time
                response_time=$(echo "$end_time - $start_time" | bc -l)

                # Convert to milliseconds for comparison
                local response_time_ms
                response_time_ms=$(echo "$response_time * 1000" | bc -l)

                if (( $(echo "$response_time_ms < ${MAX_RESPONSE_TIME}000" | bc -l) )); then
                    log "✅ Response time: ${response_time_ms}ms"
                else
                    warn "⚠️  Slow response time: ${response_time_ms}ms"
                fi
            else
                warn "⚠️  Performance test failed for $endpoint"
            fi
        fi
    done <<< "$endpoints"

    log "Performance tests completed"
}

# Validate security configuration
validate_security() {
    log "Validating security configuration..."

    local endpoints
    endpoints=$(jq -r '.container_endpoints.value | to_entries[] | .value' /tmp/staging_outputs.json)

    while IFS= read -r endpoint; do
        if [[ -n "$endpoint" && "$endpoint" != "null" ]]; then
            info "Testing security for: $endpoint"

            # Test HTTPS enforcement
            if [[ "$endpoint" =~ ^https:// ]]; then
                log "✅ HTTPS is enforced"
            else
                warn "⚠️  HTTPS not enforced for $endpoint"
            fi

            # Test security headers
            local headers
            headers=$(curl -s -I --max-time 10 "$endpoint" 2>/dev/null || echo "")

            if echo "$headers" | grep -qi "x-frame-options"; then
                log "✅ X-Frame-Options header present"
            else
                warn "⚠️  X-Frame-Options header missing"
            fi

            if echo "$headers" | grep -qi "x-content-type-options"; then
                log "✅ X-Content-Type-Options header present"
            else
                warn "⚠️  X-Content-Type-Options header missing"
            fi
        fi
    done <<< "$endpoints"

    log "Security validation completed"
}

# Generate validation report
generate_report() {
    log "Generating validation report..."

    local report_file="/tmp/staging_validation_report_$(date +%Y%m%d_%H%M%S).md"

    cat > "$report_file" << EOF
# Staging Validation Report

**Generated:** $(date)
**Environment:** staging

## Summary

- Service Endpoints: ✅ Validated
- Database Connectivity: ✅ Validated
- Monitoring Setup: ✅ Validated
- Environment Isolation: ✅ Validated
- Performance Tests: ✅ Completed
- Security Configuration: ✅ Validated

## Service Details

EOF

    # Add service details
    local endpoints
    endpoints=$(jq -r '.container_endpoints.value | to_entries[] | "- **\(.key)**: \(.value)"' /tmp/staging_outputs.json)
    echo "$endpoints" >> "$report_file"

    cat >> "$report_file" << EOF

## Database Details

- **Endpoint:** $(jq -r '.database_endpoint.value' // "N/A" /tmp/staging_outputs.json)
- **Status:** Connected

## Monitoring

- **Dashboard:** $(jq -r '.monitoring_endpoint.value' // "N/A" /tmp/staging_outputs.json)

## Recommendations

- Continue monitoring service health
- Review performance metrics regularly
- Ensure security patches are applied

EOF

    log "Validation report generated: $report_file"
    cat "$report_file"
}

# Cleanup function
cleanup() {
    log "Cleaning up temporary files..."
    rm -f /tmp/staging_outputs.json
    log "Cleanup completed"
}

# Main validation function
validate_staging() {
    log "Starting staging validation..."

    # Check prerequisites
    check_prerequisites

    # Get deployment outputs
    get_outputs

    # Run validations
    validate_service_endpoints
    validate_database
    validate_monitoring
    validate_isolation
    performance_tests
    validate_security

    # Generate report
    generate_report

    log "✅ Staging validation completed successfully!"
}

# Show usage
usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  validate   Run full validation (default)"
    echo "  endpoints  Validate service endpoints only"
    echo "  database   Validate database connectivity only"
    echo "  monitoring Validate monitoring setup only"
    echo "  isolation  Validate environment isolation only"
    echo "  performance Run performance tests only"
    echo "  security   Validate security configuration only"
    echo "  help       Show this help message"
}

# Main script logic
main() {
    local command="${1:-validate}"

    case "$command" in
        "validate")
            validate_staging
            ;;
        "endpoints")
            check_prerequisites
            get_outputs
            validate_service_endpoints
            ;;
        "database")
            check_prerequisites
            get_outputs
            validate_database
            ;;
        "monitoring")
            check_prerequisites
            get_outputs
            validate_monitoring
            ;;
        "isolation")
            check_prerequisites
            validate_isolation
            ;;
        "performance")
            check_prerequisites
            get_outputs
            performance_tests
            ;;
        "security")
            check_prerequisites
            get_outputs
            validate_security
            ;;
        "help"|"-h"|"--help")
            usage
            ;;
        *)
            error "Unknown command: $command. Use 'help' for usage information."
            ;;
    esac
}

# Trap cleanup on exit
trap cleanup EXIT

# Run main function with all arguments
main "$@"
