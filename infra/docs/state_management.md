# Pulumi State Management with Scaleway

This document describes how to set up and manage Pulumi state using Scaleway's Object Storage and PostgreSQL services for sovereign data storage.

## Overview

Pulumi state files contain sensitive infrastructure information and must be stored securely. This architecture supports **multiple stacks** (dev, staging, production) with a **single shared bucket**, enabling:

- **Centralized state management**: All stacks store state in one bucket with separate paths
- **Cost efficiency**: Single bucket reduces storage costs
- **Easy state recovery**: Versioning applies to all stacks
- **Team collaboration**: Shared infrastructure for all environments

This guide uses:

- **Scaleway Object Storage** (S3-compatible) for state file storage with versioning
- **Scaleway PostgreSQL** (optional) for distributed state locking across concurrent deployments

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Pulumi CLI / Automation                   │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
    │  State  │    │  Lock   │    │ Backup  │
    │ Storage │    │ Database│    │ History │
    └────┬────┘    └────┬────┘    └────┬────┘
         │               │               │
    ┌────▼───────────────▼───────────────▼────┐
    │   Scaleway Object Storage Bucket         │
    │   (evalap-pulumi-state)                  │
    │   - State files (.pulumi/stacks/)        │
    │   - Backups (.pulumi/backups/)           │
    │   - Versioning enabled                   │
    └─────────────────────────────────────────┘
```

## Multi-Stack Architecture

All stacks (dev, staging, production) share a **single bucket** with separate state paths:

```
evalap-pulumi-state/
├── .pulumi/stacks/dev/.pulumi.dev.json
├── .pulumi/stacks/staging/.pulumi.staging.json
└── .pulumi/stacks/production/.pulumi.production.json
```

**Benefits**:
- Single bucket to manage and secure
- Unified versioning and backup policies
- Simplified access control
- Lower storage costs
- Easy state comparison across environments

## Prerequisites

1. **Scaleway Account** with project access
2. **Scaleway CLI** installed: `brew install scw` (macOS) or `scw init`
3. **Pulumi CLI** installed: `brew install pulumi` (macOS)
4. **Scaleway API credentials**:
   - Access Key ID
   - Secret Access Key
   - Project ID

## Manual Setup: State Storage Bucket

### Step 1: Create the Object Storage Bucket

Create a single bucket to store state for all stacks (dev, staging, production):

```bash
# Using Scaleway Console (recommended for first-time setup)
# 1. Go to https://console.scaleway.com/object-storage/buckets
# 2. Click "Create bucket"
# 3. Name: evalap-pulumi-state
# 4. Region: fr-par (France Paris)
# 5. Enable "Versioning" for state recovery
# 6. Click "Create bucket"

# OR using Scaleway CLI
scw object-storage bucket create \
  name=evalap-pulumi-state \
  region=fr-par \
  project-id=$SCW_PROJECT_ID
```

### Step 2: Enable Versioning

Versioning allows you to recover previous state versions:

```bash
# Using Scaleway Console (recommended)
# 1. Click on the bucket "evalap-pulumi-state"
# 2. Go to "Settings" tab
# 3. Enable "Versioning"
# 4. Save
```

### Step 3: Create Lifecycle Policy (Optional)

Automatically delete old backups after 30 days using the setup script:

```bash
# The setup script will create the lifecycle policy automatically
./infra/scripts/setup_state_backend.sh
```

Or manually via Scaleway Console:
1. Click on the bucket "evalap-pulumi-state"
2. Go to "Lifecycle rules" tab
3. Click "Create rule"
4. Prefix: `.pulumi/backups/`
5. Expiration: 30 days
6. Save

## Manual Setup: State Locking Database (Required)

State locking is **required** for team collaboration and concurrent deployments. Set up a PostgreSQL database for distributed state locking:

### Step 1: Create PostgreSQL Instance

```bash
# Using Scaleway Console (recommended)
# 1. Go to https://console.scaleway.com/rdb/instances
# 2. Click "Create instance"
# 3. Name: evalap-pulumi-state-lock
# 4. Engine: PostgreSQL 15
# 5. Node type: DB-DEV-S (smallest, sufficient for locking)
# 6. Region: fr-par
# 7. Click "Create instance"

# OR using Scaleway CLI
scw rdb instance create \
  name=evalap-pulumi-state-lock \
  engine=PostgreSQL-15 \
  node-type=DB-DEV-S \
  region=fr-par \
  project-id=$SCW_PROJECT_ID
```

### Step 2: Create Lock Database

```bash
# Using Scaleway Console
# 1. Click on the instance "evalap-pulumi-state-lock"
# 2. Go to "Databases" tab
# 3. Click "Create database"
# 4. Name: pulumi_state_lock
# 5. Click "Create database"

# OR using psql
PGPASSWORD=$DB_PASSWORD psql \
  -h <endpoint> \
  -U postgres \
  -c "CREATE DATABASE pulumi_state_lock;"
```

### Step 3: Create Lock Table

```bash
# Connect to the database and create the lock table
PGPASSWORD=$DB_PASSWORD psql \
  -h <endpoint> \
  -U postgres \
  -d pulumi_state_lock \
  << 'EOF'
CREATE TABLE IF NOT EXISTS pulumi_state_locks (
    LockID VARCHAR(255) PRIMARY KEY,
    Data TEXT,
    LeaseExpires TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_pulumi_lock_expires
ON pulumi_state_locks (LeaseExpires);
EOF
```

## Configuring Pulumi Backend

### Step 1: Set Environment Variables

Create or update your `.env` file with Scaleway credentials:

```bash
# .env file
export SCW_PROJECT_ID="your-project-id"
export SCW_ACCESS_KEY="your-access-key"
export SCW_SECRET_KEY="your-secret-key"
export SCW_REGION="fr-par"

# Pulumi passphrase for encryption
export PULUMI_CONFIG_PASSPHRASE="your-secure-passphrase"
```

### Step 2: Login to Pulumi Backend

For each stack, configure the S3-compatible backend:

```bash
# Load environment variables
source .env

# For dev stack
pulumi stack select dev
pulumi login 's3://evalap-pulumi-state?endpoint=s3.fr-par.scw.cloud&region=fr-par&s3ForcePathStyle=true'

# For staging stack
pulumi stack select staging
pulumi login 's3://evalap-pulumi-state?endpoint=s3.fr-par.scw.cloud&region=fr-par&s3ForcePathStyle=true'

# For production stack
pulumi stack select production
pulumi login 's3://evalap-pulumi-state?endpoint=s3.fr-par.scw.cloud&region=fr-par&s3ForcePathStyle=true'
```

### Step 3: Verify Backend Configuration

```bash
# Check current backend
pulumi whoami

# List stacks
pulumi stack ls

# Export stack reference
pulumi stack export --stack dev
```

## State File Structure

State files are organized in the bucket as follows:

```
evalap-pulumi-state/
├── .pulumi/
│   ├── stacks/
│   │   ├── dev/
│   │   │   ├── Pulumi.dev.yaml
│   │   │   └── .pulumi.dev.json (encrypted state)
│   │   ├── staging/
│   │   │   ├── Pulumi.staging.yaml
│   │   │   └── .pulumi.staging.json (encrypted state)
│   │   └── production/
│   │       ├── Pulumi.production.yaml
│   │       └── .pulumi.production.json (encrypted state)
│   └── backups/
│       ├── dev-2025-11-13-120000.json
│       ├── staging-2025-11-13-120000.json
│       └── production-2025-11-13-120000.json
```

## State Recovery and Rollback

### Viewing State History

View previous state versions via Scaleway Console:

1. Go to https://console.scaleway.com/object-storage/buckets
2. Click on "evalap-pulumi-state" bucket
3. Navigate to `.pulumi/stacks/dev/`
4. Click on `.pulumi.dev.json` file
5. Go to "Versions" tab to see all versions
6. Download a specific version by clicking on it

### Rollback to Previous State

```bash
# 1. Export current state for backup
pulumi stack export --stack dev > current-state.json

# 2. Download previous version from Scaleway Console
# (See "Viewing State History" section above)
# Save as: previous-state.json

# 3. Import previous state
pulumi stack import --stack dev < previous-state.json

# 4. Verify the rollback
pulumi stack export --stack dev
```

## Concurrent Deployments and Locking

### Without State Locking (Default)

When multiple team members deploy simultaneously without locking:

```bash
# Developer A
pulumi up --stack dev --yes

# Developer B (concurrent)
pulumi up --stack dev --yes  # May conflict with Developer A
```

**Risk**: State corruption or lost updates.

### With State Locking (PostgreSQL)

Configure Pulumi to use PostgreSQL for distributed locking:

```bash
# Set lock database environment variables
export PULUMI_BACKEND_URL="s3://evalap-pulumi-state?endpoint=s3.fr-par.scw.cloud&region=fr-par&s3ForcePathStyle=true"
export PULUMI_LOCK_DB_HOST="<postgres-endpoint>"
export PULUMI_LOCK_DB_PORT="5432"
export PULUMI_LOCK_DB_NAME="pulumi_state_lock"
export PULUMI_LOCK_DB_USER="postgres"
export PULUMI_LOCK_DB_PASSWORD="$DB_PASSWORD"

# Now concurrent deployments are serialized
pulumi up --stack dev --yes  # Acquires lock
pulumi up --stack staging --yes  # Waits for lock release
```

### Best Practices

1. **Always use `--yes` flag** in CI/CD to avoid interactive prompts
2. **Set lock timeout** to prevent deadlocks: `PULUMI_LOCK_TIMEOUT=300`
3. **Monitor lock table** for stuck locks:
   ```bash
   PGPASSWORD=$DB_PASSWORD psql \
     -h <endpoint> \
     -U postgres \
     -d pulumi_state_lock \
     -c "SELECT * FROM pulumi_state_locks WHERE LeaseExpires < NOW();"
   ```
4. **Implement deployment queuing** in CI/CD to avoid concurrent deployments

## Troubleshooting

### Issue: "Access Denied" when accessing bucket

**Cause**: Incorrect Scaleway credentials or IAM permissions

**Solution**:
1. Verify credentials in `.env` file are correct
2. Check Scaleway Console that your API key has Object Storage permissions
3. Ensure `SCW_ACCESS_KEY` and `SCW_SECRET_KEY` are set correctly
4. Run the setup script to verify: `./infra/scripts/setup_state_backend.sh`

### Issue: "Bucket not found" error

**Cause**: Bucket doesn't exist or wrong region

**Solution**:
```bash
# List all buckets
scw object-storage bucket list

# Verify bucket name and region match configuration
# Expected: evalap-pulumi-state in fr-par region
```

### Issue: "State lock timeout" during deployment

**Cause**: Previous deployment didn't release lock or lock table is corrupted

**Solution**:
```bash
# Check lock status
PGPASSWORD=$DB_PASSWORD psql \
  -h <endpoint> \
  -U postgres \
  -d pulumi_state_lock \
  -c "SELECT * FROM pulumi_state_locks;"

# Force release stuck lock (use with caution)
PGPASSWORD=$DB_PASSWORD psql \
  -h <endpoint> \
  -U postgres \
  -d pulumi_state_lock \
  -c "DELETE FROM pulumi_state_locks WHERE LeaseExpires < NOW();"
```

### Issue: "Passphrase incorrect" error

**Cause**: `PULUMI_CONFIG_PASSPHRASE` not set or incorrect

**Solution**:
```bash
# Set passphrase
export PULUMI_CONFIG_PASSPHRASE="your-secure-passphrase"

# Verify it's set
echo $PULUMI_CONFIG_PASSPHRASE

# Use with uv
uv run --env-file .env pulumi up --stack dev --yes
```

## Security Considerations

1. **Encrypt credentials**: Store `PULUMI_CONFIG_PASSPHRASE` in secure secret manager
2. **Restrict bucket access**: Use Scaleway IAM policies to limit who can access the bucket
3. **Enable audit logging**: Monitor all state file access via Scaleway Cockpit
4. **Rotate credentials**: Regularly rotate Scaleway API keys
5. **Backup state files**: Regularly export and backup state to secure location

## References

- [Pulumi State and Backends](https://www.pulumi.com/docs/iac/concepts/state-and-backends/)
- [Scaleway Object Storage](https://www.scaleway.com/en/docs/object-storage/)
- [Scaleway Managed PostgreSQL](https://www.scaleway.com/en/docs/managed-databases/postgresql/)
- [AWS S3 CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/s3/)
