# Quick Start Guide: Scaleway Infrastructure Setup with Pure Terraform

**Purpose**: Quick start guide for deploying EvalAP infrastructure with Pure Terraform

## Prerequisites

### Required Tools

- **Terraform** >= 1.0.0 (Infrastructure provisioning)
- **Scaleway CLI** (scw) for authentication
- **Docker** for container image building
- **GitHub CLI** (gh) for workflow management

### Scaleway Account Setup

1. **Create Scaleway Account**:
   ```bash
   # Sign up at https://console.scaleway.com/
   # Verify email and enable billing
   ```

2. **Generate API Credentials**:
   ```bash
   # Install Scaleway CLI
   curl -L https://github.com/scaleway/scaleway-cli/releases/download/v2.26.1/scw-2.26.1-darwin-x86_64 -o scw
   sudo mv scw /usr/local/bin/
   sudo chmod +x /usr/local/bin/scw
   
   # Authenticate
   scw login
   ```

3. **Set Default Configuration**:
   ```bash
   # Set default project and region
   scw config set project-id=YOUR_PROJECT_ID
   scw config set region=fr-par
   scw config set zone=fr-par-2
   ```

### Environment Variables

Create `.env.local` file (never commit to version control):

```bash
# Scaleway credentials
export SCW_ACCESS_KEY="YOUR_ACCESS_KEY"
export SCW_SECRET_KEY="YOUR_SECRET_KEY"
export SCW_ORGANIZATION_ID="YOUR_ORG_ID"
export SCW_PROJECT_ID="YOUR_PROJECT_ID"

# Infrastructure settings
export TF_VAR_region="fr-par"
export TF_VAR_zone="fr-par-2"
```

## Project Setup

### 1. Clone Repository and Setup

```bash
# Clone the repository
git clone https://github.com/etalab-ia/evalap.git
cd evalap

# Switch to infrastructure branch
git checkout 001-scaleway-infra

# Install dependencies
uv sync

# Source environment variables
source .env.local
```

### 2. Initialize Infrastructure

```bash
# Navigate to infrastructure directory
cd infra

# Initialize Terraform (downloads providers and modules)
cd staging
terraform init

# Validate configuration
terraform validate
```

### 3. Configure Remote State

The infrastructure uses Scaleway Object Storage for Terraform state:

```bash
# Create state bucket (one-time setup)
scw object bucket create evalap-terraform-state --region fr-par

# Enable versioning and encryption
scw object bucket config update evalap-terraform-state \
  --versioning-enabled \
  --object-lock-enabled \
  --region fr-par
```

## Staging Deployment

### 1. Deploy Staging Infrastructure

```bash
# Navigate to staging configuration
cd infra/staging

# Review deployment plan
terraform plan

# Deploy staging infrastructure
terraform apply
```

### 2. Build and Push Container Images

```bash
# Build application containers
docker build -t rg.fr-par.scw.cloud/evalap/documentation:latest -f Dockerfile.documentation .
docker build -t rg.fr-par.scw.cloud/evalap/runners:latest -f Dockerfile.runners .
docker build -t rg.fr-par.scw.cloud/evalap/streamlit:latest -f Dockerfile.streamlit .

# Push to Scaleway Container Registry
docker push rg.fr-par.scw.cloud/evalap/documentation:latest
docker push rg.fr-par.scw.cloud/evalap/runners:latest
docker push rg.fr-par.scw.cloud/evalap/streamlit:latest
```

### 3. Deploy Database and Run Migrations

```bash
# Deploy database (already done with terraform apply, but showing individual steps)
cd infra/staging
terraform apply -target=module.database

# Get database connection string
terraform output -raw database_url

# Run Alembic migrations
export DATABASE_URL=$(terraform output -raw database_url)
cd ../../
alembic upgrade head
```

### 4. Verify Staging Deployment

```bash
# Get service endpoints
cd infra/staging
terraform output -raw documentation_url
terraform output -raw runners_url
terraform output -raw streamlit_url

# Test health endpoints
curl -f https://documentation.staging.evalap.fr/health
curl -f https://runners.staging.evalap.fr/health
curl -f https://streamlit.staging.evalap.fr/health
```

## Production Deployment

### 1. Deploy Production Infrastructure

```bash
# Navigate to production configuration
cd infra/production

# Review deployment plan (carefully!)
terraform plan

# Deploy production infrastructure
terraform apply
```

### 2. Deploy Services with Rolling Updates

```bash
# Deploy containers with rolling update strategy
cd infra/production

# Update container images (triggers rolling update)
terraform apply -var="documentation_image=rg.fr-par.scw.cloud/evalap/documentation:v1.0.0"
terraform apply -var="runners_image=rg.fr-par.scw.cloud/evalap/runners:v1.0.0"
terraform apply -var="streamlit_image=rg.fr-par.scw.cloud/evalap/streamlit:v1.0.0"
```

### 3. Configure Monitoring and Alerts

```bash
# Deploy monitoring configuration
cd infra/production
terraform apply -target=module.monitoring

# Verify monitoring is active
scw cockpit alert list --region fr-par
```

### 4. Verify Production Deployment

```bash
# Get production endpoints
cd infra/production
terraform output -raw documentation_url
terraform output -raw runners_url
terraform output -raw streamlit_url

# Test health and load balancing
curl -f https://documentation.evalap.fr/health
curl -f https://runners.evalap.fr/health
curl -f https://streamlit.evalap.fr/health

# Verify multiple instances are running
scw container instance list --region fr-par
```

## GitHub Actions Integration

### 1. Configure GitHub Secrets

```bash
# Set up GitHub repository secrets
gh secret set SCW_ACCESS_KEY --body="$SCW_ACCESS_KEY"
gh secret set SCW_SECRET_KEY --body="$SCW_SECRET_KEY"
gh secret set SCW_ORGANIZATION_ID --body="$SCW_ORGANIZATION_ID"
gh secret set SCW_PROJECT_ID --body="$SCW_PROJECT_ID"
```

### 2. Enable Workflows

```bash
# Enable GitHub Actions workflows
gh workflow enable "Infrastructure - Staging"
gh workflow enable "Infrastructure - Production"
gh workflow enable "Infrastructure - Validate"
```

### 3. Trigger Deployment via Git

```bash
# Deploy to staging (automatic on push to staging branch)
git push origin staging

# Deploy to production (automatic on merge to main)
git checkout main
git merge staging
git push origin main
```

## Common Operations

### Update Container Images

```bash
# Build new version
docker build -t rg.fr-par.scw.cloud/evalap/documentation:v1.1.0 -f Dockerfile.documentation .
docker push rg.fr-par.scw.cloud/evalap/documentation:v1.1.0

# Update infrastructure
cd infra/production
terraform apply -var="documentation_image=rg.fr-par.scw.cloud/evalap/documentation:v1.1.0"
```

### Scale Services

```bash
# Adjust scaling parameters
cd infra/production
terraform apply -var="documentation_min_scale=3" -var="documentation_max_scale=10"
```

### Database Operations

```bash
# Create database backup
cd infra/production
terraform apply -var="create_backup=true"

# Restore database (emergency)
terraform apply -var="restore_from_backup=backup_id"
```

### View Logs and Monitoring

```bash
# View container logs
scw container logs CONTAINER_ID --region fr-par

# View Cockpit metrics
scw cockpit metric list --region fr-par

# Check alert status
scw cockpit alert list --region fr-par
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   ```bash
   # Verify Scaleway credentials
   scw info
   scw iam user list
   ```

2. **State Lock Issues**:
   ```bash
   # Force unlock state (emergency only)
   terraform force-unlock LOCK_ID
   ```

3. **Container Health Issues**:
   ```bash
   # Check container logs
   scw container logs CONTAINER_ID --region fr-par
   
   # Check health check configuration
   terraform show | grep health_check
   ```

4. **Database Connection Issues**:
   ```bash
   # Test database connectivity
   psql $(terraform output -raw database_url)
   
   # Check database status
   scw rdb instance list --region fr-par
   ```

### Emergency Procedures

1. **Rollback Deployment**:
   ```bash
   # Rollback to previous container version
   terraform apply -var="documentation_image=previous_image_tag"
   ```

2. **Scale Down Services**:
   ```bash
   # Emergency scale down
   terraform apply -var="documentation_min_scale=0"
   ```

3. **Disable Monitoring**:
   ```bash
   # Disable alerts during maintenance
   cd infra/production
   terraform apply -var="alerts_enabled=false"
   ```

## Cleanup

### Remove Staging Environment

```bash
cd infra/staging
terraform destroy
```

### Remove Production Environment

```bash
cd infra/production
terraform destroy
```

### Remove State Bucket

```bash
# Delete state objects
scw object delete --recursive evalap-terraform-state

# Delete bucket
scw object bucket delete evalap-terraform-state --region fr-par
```

## Next Steps

1. **Configure Custom Domains** - Set up DNS for service endpoints
2. **Set Up SSL Certificates** - Configure HTTPS for all services  
3. **Implement Backup Monitoring** - Set up alerts for backup failures
4. **Configure Log Aggregation** - Centralize logs from all services
5. **Set Up Cost Monitoring** - Track infrastructure spending

## Support

- **Scaleway Documentation**: https://www.scaleway.com/en/docs/
- **Terraform Documentation**: https://www.terraform.io/docs/
- **EvalAP Repository**: https://github.com/etalab-ia/evalap/issues

For infrastructure-specific issues, check the GitHub Actions workflow logs or use the Scaleway console for detailed diagnostics.
