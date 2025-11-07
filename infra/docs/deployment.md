# Deployment Guide

## Overview

This guide covers deploying the EvalAP infrastructure to Scaleway using OpenTofu.

## Prerequisites

1. **OpenTofu Installation**
   ```bash
   # macOS
   brew install opentofu

   # Linux
   curl https://get.opentofu.org/install.sh | sh
   ```

2. **Scaleway Account Setup**
   - Create a Scaleway account at https://console.scaleway.com
   - Generate API credentials (Access Key and Secret Key)
   - Note your Project ID

3. **Environment Variables**
   ```bash
   export SCW_ACCESS_KEY="your_access_key"
   export SCW_SECRET_KEY="your_secret_key"
   export SCW_DEFAULT_PROJECT_ID="your_project_id"
   ```

## Environment Setup

### Staging Environment

```bash
cd infra/staging
tofu init
tofu plan
tofu apply
```

### Production Environment

```bash
cd infra/production
tofu init
tofu plan
tofu apply
```

## State Management

- State files are stored in Scaleway Object Storage
- State locking is enabled via DynamoDB
- Each environment has isolated state

## Monitoring

- Access Scaleway Cockpit for monitoring
- Check logs and metrics in the console
- Set up alerts as needed

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for common issues.
