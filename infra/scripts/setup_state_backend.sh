#!/bin/bash
# Setup Pulumi state backend on Scaleway with state locking
#
# This script automates the creation of:
# 1. Object Storage bucket for state files with versioning
# 2. PostgreSQL database for distributed state locking
#
# State locking is required for team collaboration and concurrent deployments.
#
# Usage: ./setup_state_backend.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BUCKET_NAME="${BUCKET_NAME:-evalap-pulumi-state}"
REGION="${REGION:-fr-par}"
DB_NAME="${DB_NAME:-evalap-pulumi-state-lock}"
DB_ENGINE="${DB_ENGINE:-PostgreSQL-15}"
DB_NODE_TYPE="${DB_NODE_TYPE:-DB-DEV-S}"
LOCK_DB_NAME="${LOCK_DB_NAME:-pulumi_state_lock}"
LOCK_TABLE_NAME="${LOCK_TABLE_NAME:-pulumi_state_locks}"

# State locking is always enabled for team collaboration
WITH_LOCKING=true

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check Scaleway CLI
    if ! command -v scw &> /dev/null; then
        log_error "Scaleway CLI not found. Install with: brew install scw"
        exit 1
    fi

    # Check environment variables
    if [[ -z "$SCW_PROJECT_ID" ]]; then
        log_error "SCW_PROJECT_ID not set"
        exit 1
    fi

    if [[ -z "$SCW_ACCESS_KEY" ]]; then
        log_error "SCW_ACCESS_KEY not set"
        exit 1
    fi

    if [[ -z "$SCW_SECRET_KEY" ]]; then
        log_error "SCW_SECRET_KEY not set"
        exit 1
    fi

    log_info "Prerequisites check passed"
}

create_bucket() {
    log_info "Creating Object Storage bucket: $BUCKET_NAME"

    # Check if bucket already exists
    if scw object-storage bucket list | grep -q "$BUCKET_NAME"; then
        log_warn "Bucket $BUCKET_NAME already exists, skipping creation"
        return
    fi

    # Create bucket
    scw object-storage bucket create \
        name="$BUCKET_NAME" \
        region="$REGION" \
        project-id="$SCW_PROJECT_ID"

    log_info "Bucket created successfully"
}

enable_versioning() {
    log_info "Enabling versioning on bucket: $BUCKET_NAME"

    log_warn "Please enable versioning manually via Scaleway Console:"
    echo ""
    echo "  1. Go to https://console.scaleway.com/object-storage/buckets"
    echo "  2. Click on bucket: $BUCKET_NAME"
    echo "  3. Go to 'Settings' tab"
    echo "  4. Enable 'Versioning'"
    echo "  5. Click 'Save'"
    echo ""

    log_info "Versioning setup instructions provided"
}

create_lifecycle_policy() {
    log_info "Creating lifecycle policy for backup retention"

    log_warn "Please create lifecycle policy manually via Scaleway Console:"
    echo ""
    echo "  1. Go to https://console.scaleway.com/object-storage/buckets"
    echo "  2. Click on bucket: $BUCKET_NAME"
    echo "  3. Go to 'Lifecycle rules' tab"
    echo "  4. Click 'Create rule'"
    echo "  5. Set:"
    echo "     - Prefix: .pulumi/backups/"
    echo "     - Expiration: 30 days"
    echo "  6. Click 'Create rule'"
    echo ""

    log_info "Lifecycle policy setup instructions provided"
}

create_lock_database() {
    log_info "Creating PostgreSQL instance for state locking: $DB_NAME"

    # Check if instance already exists
    if scw rdb instance list | grep -q "$DB_NAME"; then
        log_warn "Instance $DB_NAME already exists, skipping creation"
        return
    fi

    # Create RDB instance
    scw rdb instance create \
        name="$DB_NAME" \
        engine="$DB_ENGINE" \
        node-type="$DB_NODE_TYPE" \
        region="$REGION" \
        project-id="$SCW_PROJECT_ID"

    log_info "PostgreSQL instance created successfully"
    log_warn "Note: Instance creation may take 5-10 minutes. Check status in Scaleway Console."
}

create_lock_database_schema() {
    log_info "Creating lock database schema"

    # Get instance details
    INSTANCE_ID=$(scw rdb instance list | grep "$DB_NAME" | awk '{print $1}')

    if [[ -z "$INSTANCE_ID" ]]; then
        log_error "Could not find instance $DB_NAME"
        return 1
    fi

    log_info "Instance ID: $INSTANCE_ID"
    log_warn "Please manually create the lock database using:"
    echo ""
    echo "  1. Get the endpoint from Scaleway Console"
    echo "  2. Run the following commands:"
    echo ""
    echo "  PGPASSWORD=\$DB_PASSWORD psql \\"
    echo "    -h <endpoint> \\"
    echo "    -U postgres \\"
    echo "    -c \"CREATE DATABASE $LOCK_DB_NAME;\""
    echo ""
    echo "  PGPASSWORD=\$DB_PASSWORD psql \\"
    echo "    -h <endpoint> \\"
    echo "    -U postgres \\"
    echo "    -d $LOCK_DB_NAME \\"
    echo "    << 'SQL'"
    echo "  CREATE TABLE IF NOT EXISTS $LOCK_TABLE_NAME ("
    echo "      LockID VARCHAR(255) PRIMARY KEY,"
    echo "      Data TEXT,"
    echo "      LeaseExpires TIMESTAMP WITH TIME ZONE"
    echo "  );"
    echo ""
    echo "  CREATE INDEX IF NOT EXISTS idx_pulumi_lock_expires"
    echo "  ON $LOCK_TABLE_NAME (LeaseExpires);"
    echo "  SQL"
    echo ""
}

configure_pulumi() {
    log_info "Configuring Pulumi backend"

    # Check if Pulumi is installed
    if ! command -v pulumi &> /dev/null; then
        log_error "Pulumi CLI not found. Install with: brew install pulumi"
        return 1
    fi

    # Get current directory
    CURRENT_DIR=$(pwd)

    log_info "Pulumi backend configuration:"
    echo ""
    echo "  Backend URL:"
    echo "  s3://$BUCKET_NAME?endpoint=s3.${REGION}.scw.cloud&region=${REGION}&s3ForcePathStyle=true"
    echo ""
    echo "  To configure each stack, run:"
    echo ""
    echo "  pulumi stack select dev"
    echo "  pulumi login 's3://$BUCKET_NAME?endpoint=s3.${REGION}.scw.cloud&region=${REGION}&s3ForcePathStyle=true'"
    echo ""
    echo "  pulumi stack select staging"
    echo "  pulumi login 's3://$BUCKET_NAME?endpoint=s3.${REGION}.scw.cloud&region=${REGION}&s3ForcePathStyle=true'"
    echo ""
    echo "  pulumi stack select production"
    echo "  pulumi login 's3://$BUCKET_NAME?endpoint=s3.${REGION}.scw.cloud&region=${REGION}&s3ForcePathStyle=true'"
    echo ""
}

verify_setup() {
    log_info "Verifying setup..."

    # Check bucket exists
    if scw object-storage bucket list | grep -q "$BUCKET_NAME"; then
        log_info "✓ Bucket $BUCKET_NAME exists"
    else
        log_error "✗ Bucket $BUCKET_NAME not found"
        return 1
    fi

    log_warn "Please verify via Scaleway Console:"
    echo ""
    echo "  1. Go to https://console.scaleway.com/object-storage/buckets"
    echo "  2. Click on bucket: $BUCKET_NAME"
    echo "  3. Verify versioning is enabled in 'Settings' tab"
    echo "  4. Verify lifecycle rule exists in 'Lifecycle rules' tab"
    echo ""

    log_info "Setup verification complete"
}

main() {
    echo "=========================================="
    echo "Pulumi State Backend Setup for Scaleway"
    echo "=========================================="
    echo ""

    check_prerequisites
    echo ""

    create_bucket
    echo ""

    enable_versioning
    echo ""

    create_lifecycle_policy
    echo ""

    if [[ "$WITH_LOCKING" == true ]]; then
        create_lock_database
        echo ""

        create_lock_database_schema
        echo ""
    fi

    verify_setup
    echo ""

    configure_pulumi
    echo ""

    log_info "Setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. Configure Pulumi backend for each stack (see commands above)"
    echo "2. Set PULUMI_CONFIG_PASSPHRASE environment variable"
    echo "3. Run: pulumi up --stack dev --yes"
    echo ""
}

main "$@"
