# Scaleway Infrastructure Setup with Pure OpenTofu

This directory contains the Infrastructure as Code (IaC) setup for EvalAP on Scaleway using OpenTofu.

## Structure

- `staging/` - Staging environment configuration
- `production/` - Production environment configuration
- `modules/` - Reusable OpenTofu modules
- `scripts/` - Deployment and utility scripts
- `docs/` - Infrastructure documentation

## Quick Start

1. Install OpenTofu: `brew install opentofu` (macOS) or see https://opentofu.org/docs/intro/install.html
2. Set up Scaleway credentials: `export SCW_ACCESS_KEY=...` and `export SCW_SECRET_KEY=...`
3. Initialize OpenTofu: `tofu init`
4. Plan changes: `tofu plan`
5. Apply changes: `tofu apply`

## Environment Isolation

Each environment (staging/production) has:
- Separate OpenTofu state files
- Independent Scaleway resources
- Environment-specific configurations
- No shared infrastructure components

## Modules

Reusable infrastructure components:
- `serverless-container/` - Scaleway Serverless Containers
- `managed-postgresql/` - PostgreSQL database with HA
- `secret-manager/` - IAM Secret Manager integration
- `cockpit-monitoring/` - Monitoring and alerting

## Security

- No hardcoded secrets
- All secrets stored in Scaleway IAM Secret Manager
- Least privilege IAM roles
- Encrypted state storage

## Documentation

See `docs/` for detailed guides:
- `deployment.md` - Deployment procedures
- `troubleshooting.md` - Common issues and solutions
- `architecture.md` - Infrastructure architecture overview
