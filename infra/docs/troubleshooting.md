# Troubleshooting Guide

## Common Issues

### Authentication Errors

**Error**: `authentication failed`

**Solution**:
1. Verify environment variables are set:
   ```bash
   echo $SCW_ACCESS_KEY
   echo $SCW_SECRET_KEY
   echo $SCW_DEFAULT_PROJECT_ID
   ```
2. Check API key permissions in Scaleway console
3. Ensure keys are not expired

### State Lock Issues

**Error**: `Error locking state`

**Solution**:
1. Check if another deployment is running
2. Force unlock if necessary:
   ```bash
   tofu force-unlock LOCK_ID
   ```
3. Verify DynamoDB table exists and is accessible

### Resource Creation Failures

**Error**: `quota exceeded` or `insufficient capacity`

**Solution**:
1. Check Scaleway quotas in console
2. Try a different availability zone
3. Contact Scaleway support to increase quotas

### Network Issues

**Error**: `timeout` or `connection refused`

**Solution**:
1. Check network connectivity
2. Verify security group rules
3. Check firewall settings

## Debugging Commands

### Validate Configuration
```bash
tofu validate
tofu fmt -check
```

### Debug State
```bash
tofu show
tofu state list
```

### Import Existing Resources
```bash
tofu import scaleway_container.namespace.my_namespace namespace_id
```

## Getting Help

1. Check OpenTofu documentation: https://opentofu.org/docs/
2. Check Scaleway provider docs: https://registry.opentofu.org/providers/scaleway/scaleway/latest/docs
3. Review OpenTofu state and logs
4. Contact Scaleway support for platform issues
