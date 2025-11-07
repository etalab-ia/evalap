# Infrastructure Architecture

## Overview

The EvalAP infrastructure is deployed on Scaleway using OpenTofu with complete environment isolation.

## Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐
│   Staging Env   │    │ Production Env  │
├─────────────────┤    ├─────────────────┤
│ • Containers    │    │ • Containers    │
│ • PostgreSQL    │    │ • PostgreSQL HA │
│ • Secrets       │    │ • Secrets       │
│ • Monitoring    │    │ • Monitoring    │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────────────────┘
                 │
         ┌─────────────────┐
         │   Scaleway      │
         │   Object Storage│
         │   (State Files) │
         └─────────────────┘
```

## Components

### Compute
- **Scaleway Serverless Containers**: Host documentation, runners, and Streamlit services
- **Auto-scaling**: Configurable min/max instances
- **Load Balancing**: Automatic for production environment

### Database
- **Managed PostgreSQL**: High availability with replicas
- **Automated Backups**: Daily, weekly, monthly retention
- **Point-in-time Recovery**: 7-day window

### Security
- **IAM Secret Manager**: Centralized secret management
- **Network Isolation**: Private networks where appropriate
- **Least Privilege**: Minimal required permissions

### Monitoring
- **Scaleway Cockpit**: Metrics, logs, and alerts
- **Custom Dashboards**: Application-specific monitoring
- **Notification System**: Alert routing

## Environment Isolation

Each environment has:
- Separate OpenTofu state
- Independent resources
- No shared infrastructure
- Isolated networking

## Scalability

- Horizontal scaling via container instances
- Database read replicas
- CDN integration for static assets
- Auto-scaling based on metrics

## Disaster Recovery

- Multi-AZ deployment
- Automated backups
- State file versioning
- Rollback capabilities
