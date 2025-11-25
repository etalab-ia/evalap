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
- **Built-in file-based locking** (automatic with S3 backend) for concurrent deployment protection

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
    │ Storage │    │  Files  │    │ History │
    └────┬────┘    └────┬────┘    └────┬────┘
         │               │               │
    ┌────▼───────────────▼───────────────▼────┐
    │   Scaleway Object Storage Bucket         │
    │   (evalap-pulumi-state)                  │
    │   - State files (.pulumi/stacks/)        │
    │   - Lock files (.pulumi/locks/)          │
    │   - History (.pulumi/history/)           │
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

Pulumi's S3-compatible backend includes **built-in file-based locking** that automatically prevents concurrent operations on the same stack.

### How It Works

When you run `pulumi up`, Pulumi:

1. Creates a lock file in `.pulumi/locks/<stack>/<lock-id>.json`
2. Performs the deployment
3. Removes the lock file on completion

If another deployment attempts to run concurrently:

```bash
# Developer A
pulumi up --stack dev --yes  # Acquires lock, proceeds

# Developer B (concurrent)
pulumi up --stack dev --yes  # Waits or fails with lock error
```

### Lock File Location

Lock files are stored in the same bucket as state files:

```
evalap-pulumi-state/
├── .pulumi/
│   ├── stacks/dev.json
│   ├── locks/dev/<uuid>.json    ← Lock file (temporary)
│   └── history/dev/...
```

### Best Practices

1. **Always use `--yes` flag** in CI/CD to avoid interactive prompts
2. **Implement deployment queuing** in CI/CD to avoid concurrent deployments
3. **Check for stale locks** if deployments fail unexpectedly:
   - View `.pulumi/locks/` in Scaleway Console
   - Delete stale lock files if a deployment crashed without cleanup

### Handling Stuck Locks

If a deployment crashes without releasing its lock:

1. Go to Scaleway Console → Object Storage → `evalap-pulumi-state`
2. Navigate to `.pulumi/locks/<stack>/`
3. Delete any `.json` lock files
4. Retry your deployment

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

### Issue: "State lock timeout" or "lock already held" during deployment

**Cause**: Previous deployment crashed without releasing its lock file

**Solution**:

1. Go to Scaleway Console → Object Storage → `evalap-pulumi-state`
2. Navigate to `.pulumi/locks/<stack>/`
3. Delete any stale `.json` lock files
4. Retry your deployment

Alternatively, use the AWS CLI (with Scaleway credentials):

```bash
# List lock files
aws s3 ls s3://evalap-pulumi-state/.pulumi/locks/ \
  --endpoint-url https://s3.fr-par.scw.cloud --recursive

# Delete a specific lock file (use with caution)
aws s3 rm s3://evalap-pulumi-state/.pulumi/locks/dev/<lock-id>.json \
  --endpoint-url https://s3.fr-par.scw.cloud
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
