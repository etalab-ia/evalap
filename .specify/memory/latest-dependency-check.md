# Latest Dependency Check Method

**Date**: 2025-11-08 | **Status**: ✅ Active

## Preferred Method: Use `pip index versions`

Always use `pip index versions <package-name>` to check the latest available versions from PyPI. This is more reliable than web scraping or manual checking.

### Command Examples

```bash
# Check latest version
pip index versions pulumi

# Check multiple packages
pip index versions pulumi-scaleway pydantic pytest

# Output format:
# package-name (latest-version)
# Available versions: latest, previous, older...
```

## Version Specification Best Practices

### Use Latest Versions with Flexible Constraints

When updating dependency specifications, use the latest version with flexible constraints to avoid compatibility issues:

**❌ Too Specific (may cause conflicts):**
```toml
pulumi==3.206.0
pulumi-scaleway==0.3.0
pydantic==2.12.4
pytest==9.0.0
```

**✅ Flexible Constraints (recommended):**
```toml
pulumi>=3.206.0,<4.0.0
pulumi-scaleway>=0.3.0,<1.0.0
pydantic>=2.12.4,<3.0.0
pytest>=9.0.0,<10.0.0
```

### Why Flexible Constraints?

1. **uv Compatibility**: uv may fail to install if version constraints are too specific and conflict with transitive dependencies
2. **Security Updates**: Allows automatic patch updates within compatible ranges
3. **Dependency Resolution**: Better resolution of complex dependency trees
4. **Future-Proofing**: Less likely to break when new patch versions are released

## Current Latest Versions (2025-11-08)

Based on `pip index versions`:

- **pulumi**: 3.206.0 (released Nov 5, 2025)
- **pulumi-scaleway**: 0.3.0 (latest)
- **pydantic**: 2.12.4 (latest)
- **pytest**: 9.0.0 (latest)

## Recommended Version Specs for EvalAP

```toml
[project.optional-dependencies]
infra = [
    "pulumi>=3.206.0,<4.0.0",
    "pulumi-scaleway>=0.3.0,<1.0.0",
    "pydantic>=2.12.4,<3.0.0",
    "pytest>=9.0.0,<10.0.0",
]
```

## Implementation Checklist

When updating dependencies:

1. **Check Latest Versions**: `pip index versions <package1> <package2> ...`
2. **Use Flexible Constraints**: `>=latest,<next-major`
3. **Test Installation**: `uv sync --all-extras`
4. **Verify Compatibility**: Run tests to ensure no breaking changes
5. **Update Documentation**: Update quickstart guides and plan files

## Automation Opportunity

Consider adding this check to CI/CD pipeline:

```yaml
- name: Check for outdated dependencies
  run: |
    pip index versions pulumi pulumi-scaleway pydantic pytest
    # Compare with current specs and create PR if updates available
```

## Memory Tags

dependency-management, latest-versions, pip-index, uv-compatibility, version-specs

## Related Files

- `pyproject.toml` - Central dependency configuration
- `specs/*/quickstart.md` - Installation guides
- `specs/*/plan.md` - Technical context with dependencies
