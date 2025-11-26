"""Common Pulumi utilities for resource patterns and output handling."""

import json
import logging
import os
import traceback
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Optional, TypeVar

import pulumi

logger = logging.getLogger(__name__)

# Audit logger for structured audit events
audit_logger = logging.getLogger("infra.audit")

T = TypeVar("T")


# =============================================================================
# Audit Logging for Infrastructure Changes
# =============================================================================


class AuditOperation(Enum):
    """Types of infrastructure operations for audit logging."""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    DEPLOY = "deploy"
    PREVIEW = "preview"
    REFRESH = "refresh"
    DESTROY = "destroy"


class AuditSeverity(Enum):
    """Severity levels for audit events."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class AuditEvent:
    """
    Structured audit event for infrastructure changes.

    Captures all relevant information about an infrastructure operation
    for compliance, debugging, and operational visibility.
    """

    timestamp: str
    operation: str
    resource_type: str
    resource_name: str
    stack: str
    project: str
    environment: str
    severity: str = "info"
    actor: str = field(default_factory=lambda: os.environ.get("USER", "unknown"))
    details: dict[str, Any] = field(default_factory=dict)
    success: bool = True
    error_message: Optional[str] = None
    duration_ms: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert audit event to dictionary for JSON serialization."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert audit event to JSON string."""
        return json.dumps(self.to_dict(), default=str)


class AuditLogger:
    """
    Audit logger for infrastructure changes.

    Provides structured logging of all infrastructure operations with:
    - Timestamps in ISO 8601 format
    - Actor identification (user/service account)
    - Operation details (create/update/delete)
    - Resource information (type, name, stack)
    - Success/failure status with error details
    - Duration tracking for performance monitoring
    """

    def __init__(self, environment: str = "unknown"):
        """
        Initialize audit logger.

        Args:
            environment: Environment name (dev, staging, production)
        """
        self.environment = environment
        self._start_times: dict[str, datetime] = {}

    def _get_context(self) -> tuple[str, str]:
        """Get Pulumi stack and project context."""
        try:
            stack = pulumi.get_stack()
        except Exception:
            stack = "unknown"
        try:
            project = pulumi.get_project()
        except Exception:
            project = "unknown"
        return stack, project

    def _create_event(
        self,
        operation: AuditOperation,
        resource_type: str,
        resource_name: str,
        severity: AuditSeverity = AuditSeverity.INFO,
        details: Optional[dict[str, Any]] = None,
        success: bool = True,
        error_message: Optional[str] = None,
        duration_ms: Optional[int] = None,
    ) -> AuditEvent:
        """Create a structured audit event."""
        stack, project = self._get_context()
        return AuditEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            operation=operation.value,
            resource_type=resource_type,
            resource_name=resource_name,
            stack=stack,
            project=project,
            environment=self.environment,
            severity=severity.value,
            details=details or {},
            success=success,
            error_message=error_message,
            duration_ms=duration_ms,
        )

    def start_operation(self, resource_type: str, resource_name: str) -> None:
        """
        Mark the start of an operation for duration tracking.

        Args:
            resource_type: Type of resource being operated on
            resource_name: Name of the resource
        """
        key = f"{resource_type}:{resource_name}"
        self._start_times[key] = datetime.now(timezone.utc)

    def _get_duration_ms(self, resource_type: str, resource_name: str) -> Optional[int]:
        """Get duration in milliseconds since operation start."""
        key = f"{resource_type}:{resource_name}"
        start_time = self._start_times.pop(key, None)
        if start_time:
            delta = datetime.now(timezone.utc) - start_time
            return int(delta.total_seconds() * 1000)
        return None

    def log_create(
        self,
        resource_type: str,
        resource_name: str,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Log a resource creation event.

        Args:
            resource_type: Type of resource (e.g., "DatabaseInstance", "Container")
            resource_name: Name of the resource
            details: Optional additional details about the creation
        """
        duration_ms = self._get_duration_ms(resource_type, resource_name)
        event = self._create_event(
            operation=AuditOperation.CREATE,
            resource_type=resource_type,
            resource_name=resource_name,
            details=details,
            duration_ms=duration_ms,
        )
        audit_logger.info(event.to_json())
        logger.info(f"AUDIT: Created {resource_type} '{resource_name}' in {self.environment}")

    def log_update(
        self,
        resource_type: str,
        resource_name: str,
        changes: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Log a resource update event.

        Args:
            resource_type: Type of resource
            resource_name: Name of the resource
            changes: Optional dictionary of changes made
        """
        duration_ms = self._get_duration_ms(resource_type, resource_name)
        details = {"changes": changes} if changes else {}
        event = self._create_event(
            operation=AuditOperation.UPDATE,
            resource_type=resource_type,
            resource_name=resource_name,
            details=details,
            duration_ms=duration_ms,
        )
        audit_logger.info(event.to_json())
        logger.info(f"AUDIT: Updated {resource_type} '{resource_name}' in {self.environment}")

    def log_delete(
        self,
        resource_type: str,
        resource_name: str,
        reason: Optional[str] = None,
    ) -> None:
        """
        Log a resource deletion event.

        Args:
            resource_type: Type of resource
            resource_name: Name of the resource
            reason: Optional reason for deletion
        """
        duration_ms = self._get_duration_ms(resource_type, resource_name)
        details = {"reason": reason} if reason else {}
        event = self._create_event(
            operation=AuditOperation.DELETE,
            resource_type=resource_type,
            resource_name=resource_name,
            severity=AuditSeverity.WARNING,
            details=details,
            duration_ms=duration_ms,
        )
        audit_logger.warning(event.to_json())
        logger.warning(f"AUDIT: Deleted {resource_type} '{resource_name}' in {self.environment}")

    def log_error(
        self,
        resource_type: str,
        resource_name: str,
        operation: AuditOperation,
        error: Exception,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Log an operation error.

        Args:
            resource_type: Type of resource
            resource_name: Name of the resource
            operation: Operation that failed
            error: Exception that occurred
            details: Optional additional details
        """
        duration_ms = self._get_duration_ms(resource_type, resource_name)
        event = self._create_event(
            operation=operation,
            resource_type=resource_type,
            resource_name=resource_name,
            severity=AuditSeverity.ERROR,
            details=details or {},
            success=False,
            error_message=str(error),
            duration_ms=duration_ms,
        )
        audit_logger.error(event.to_json())
        logger.error(f"AUDIT: Failed to {operation.value} {resource_type} '{resource_name}': {error}")

    def log_deployment_start(
        self,
        stack_name: str,
        resources: Optional[list[str]] = None,
    ) -> None:
        """
        Log the start of a deployment.

        Args:
            stack_name: Name of the stack being deployed
            resources: Optional list of resources to be deployed
        """
        self.start_operation("Stack", stack_name)
        event = self._create_event(
            operation=AuditOperation.DEPLOY,
            resource_type="Stack",
            resource_name=stack_name,
            details={"resources": resources or [], "phase": "start"},
        )
        audit_logger.info(event.to_json())
        logger.info(f"AUDIT: Starting deployment of stack '{stack_name}'")

    def log_deployment_complete(
        self,
        stack_name: str,
        resources_created: int = 0,
        resources_updated: int = 0,
        resources_deleted: int = 0,
    ) -> None:
        """
        Log the completion of a deployment.

        Args:
            stack_name: Name of the stack deployed
            resources_created: Number of resources created
            resources_updated: Number of resources updated
            resources_deleted: Number of resources deleted
        """
        duration_ms = self._get_duration_ms("Stack", stack_name)
        event = self._create_event(
            operation=AuditOperation.DEPLOY,
            resource_type="Stack",
            resource_name=stack_name,
            details={
                "phase": "complete",
                "resources_created": resources_created,
                "resources_updated": resources_updated,
                "resources_deleted": resources_deleted,
            },
            duration_ms=duration_ms,
        )
        audit_logger.info(event.to_json())
        logger.info(
            f"AUDIT: Deployment complete for stack '{stack_name}' - "
            f"created={resources_created}, updated={resources_updated}, deleted={resources_deleted}"
        )

    def log_deployment_failed(
        self,
        stack_name: str,
        error: Exception,
        partial_resources: Optional[dict[str, int]] = None,
    ) -> None:
        """
        Log a failed deployment.

        Args:
            stack_name: Name of the stack
            error: Exception that caused the failure
            partial_resources: Optional count of partially deployed resources
        """
        duration_ms = self._get_duration_ms("Stack", stack_name)
        event = self._create_event(
            operation=AuditOperation.DEPLOY,
            resource_type="Stack",
            resource_name=stack_name,
            severity=AuditSeverity.CRITICAL,
            details={
                "phase": "failed",
                "partial_resources": partial_resources or {},
            },
            success=False,
            error_message=str(error),
            duration_ms=duration_ms,
        )
        audit_logger.critical(event.to_json())
        logger.critical(f"AUDIT: Deployment FAILED for stack '{stack_name}': {error}")


# Global audit logger instance (can be configured per environment)
_audit_logger_instance: Optional[AuditLogger] = None


def get_audit_logger(environment: Optional[str] = None) -> AuditLogger:
    """
    Get or create the global audit logger instance.

    Args:
        environment: Optional environment name to configure the logger

    Returns:
        AuditLogger: The audit logger instance
    """
    global _audit_logger_instance
    if _audit_logger_instance is None or environment is not None:
        env = environment or os.environ.get("PULUMI_STACK", "unknown")
        _audit_logger_instance = AuditLogger(environment=env)
    return _audit_logger_instance


def configure_audit_logging(
    log_file: Optional[str] = None,
    log_level: int = logging.INFO,
    json_format: bool = True,
) -> None:
    """
    Configure audit logging output.

    Args:
        log_file: Optional file path for audit logs (in addition to console)
        log_level: Logging level for audit events
        json_format: Whether to use JSON format for file output
    """
    audit_logger.setLevel(log_level)

    # Console handler with human-readable format
    if not audit_logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter("%(asctime)s - AUDIT - %(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)
        audit_logger.addHandler(console_handler)

    # File handler with JSON format if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        if json_format:
            # JSON format - the message is already JSON from AuditEvent.to_json()
            file_formatter = logging.Formatter("%(message)s")
        else:
            file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        audit_logger.addHandler(file_handler)


def create_resource_name(base_name: str, suffix: str = "") -> str:
    """
    Create a resource name following Scaleway naming conventions.

    Args:
        base_name: Base name for the resource
        suffix: Optional suffix to append

    Returns:
        str: Formatted resource name
    """
    stack_name = pulumi.get_stack()
    name = f"{base_name}-{stack_name}"
    if suffix:
        name = f"{name}-{suffix}"
    return name.lower().replace("_", "-")


def export_output(name: str, value: Any, description: str = "") -> None:
    """
    Export a stack output with logging.

    Args:
        name: Output name
        value: Output value
        description: Optional description
    """
    pulumi.export(name, value)
    if description:
        logger.info(f"Exported output '{name}': {description}")
    else:
        logger.info(f"Exported output '{name}'")


def get_output_value(output: pulumi.Output) -> Any:
    """
    Get the value from a Pulumi output (for testing/debugging).

    Args:
        output: Pulumi output object

    Returns:
        Any: The output value
    """
    return output.get_future().result()


def apply_with_logging(output: pulumi.Output, func, log_message: str = "") -> pulumi.Output:
    """
    Apply a function to an output with logging.

    Args:
        output: Pulumi output to apply function to
        func: Function to apply
        log_message: Optional log message

    Returns:
        pulumi.Output: Result of applying function
    """
    if log_message:
        logger.debug(log_message)
    return output.apply(func)


def combine_outputs(*outputs: pulumi.Output) -> pulumi.Output:
    """
    Combine multiple outputs into a single output.

    Args:
        *outputs: Variable number of Pulumi outputs

    Returns:
        pulumi.Output: Combined output as a list
    """
    return pulumi.Output.all(*outputs)


def create_tags(
    environment: str,
    component: str,
    additional_tags: Optional[dict[str, str]] = None,
) -> dict[str, str]:
    """
    Create standardized tags for resources.

    Args:
        environment: Environment name (dev, staging, production)
        component: Component name
        additional_tags: Optional additional tags

    Returns:
        dict: Tags dictionary
    """
    tags = {
        "Environment": environment,
        "Component": component,
        "ManagedBy": "Pulumi",
        "Stack": pulumi.get_stack(),
    }

    if additional_tags:
        tags.update(additional_tags)

    return tags


def log_resource_creation(resource_type: str, resource_name: str, **kwargs) -> None:
    """
    Log resource creation with details.

    Args:
        resource_type: Type of resource being created
        resource_name: Name of the resource
        **kwargs: Additional details to log
    """
    details = " | ".join(f"{k}={v}" for k, v in kwargs.items())
    logger.info(f"Creating {resource_type}: {resource_name} | {details}")


def handle_error(error: Exception, context: str = "") -> None:
    """
    Handle and log errors during infrastructure deployment.

    Args:
        error: Exception that occurred
        context: Context where error occurred

    Raises:
        Exception: Re-raises the original exception after logging
    """
    error_msg = f"Error in {context}: {str(error)}" if context else f"Error: {str(error)}"
    logger.error(error_msg)
    logger.debug(f"Traceback: {traceback.format_exc()}")
    raise error


def handle_deployment_error(error: Exception, resource_type: str, resource_name: str) -> None:
    """
    Handle deployment errors with detailed logging.

    Args:
        error: Exception that occurred
        resource_type: Type of resource that failed
        resource_name: Name of the resource that failed

    Raises:
        Exception: Re-raises the original exception after logging
    """
    error_msg = f"Deployment failed for {resource_type} '{resource_name}': {str(error)}"
    logger.error(error_msg)
    logger.debug(f"Full traceback:\n{traceback.format_exc()}")

    # Log additional context
    logger.error(f"Stack: {pulumi.get_stack()}")
    logger.error(f"Project: {pulumi.get_project()}")

    raise error


def retry_with_backoff(
    func: Callable[..., T],
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    *args,
    **kwargs,
) -> T:
    """
    Retry a function with exponential backoff.

    Args:
        func: Function to retry
        max_retries: Maximum number of retries
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for delay after each retry
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func

    Returns:
        Result of the function call

    Raises:
        Exception: If all retries fail
    """
    import time

    delay = initial_delay
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            logger.debug(f"Attempt {attempt + 1}/{max_retries + 1} for {func.__name__}")
            return func(*args, **kwargs)
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                logger.warning(
                    f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}. Retrying in {delay}s..."
                )
                time.sleep(delay)
                delay *= backoff_factor
            else:
                logger.error(f"All {max_retries + 1} attempts failed for {func.__name__}: {str(e)}")

    raise last_error


def validate_deployment_prerequisites() -> bool:
    """
    Validate that deployment prerequisites are met.

    Returns:
        bool: True if all prerequisites are met

    Raises:
        ValueError: If any prerequisite is missing
    """
    logger.info("Validating deployment prerequisites")

    # Check Pulumi stack is selected
    try:
        stack = pulumi.get_stack()
        logger.debug(f"Pulumi stack: {stack}")
    except Exception as e:
        raise ValueError(f"Failed to get Pulumi stack: {str(e)}") from e

    # Check Pulumi project is configured
    try:
        project = pulumi.get_project()
        logger.debug(f"Pulumi project: {project}")
    except Exception as e:
        raise ValueError(f"Failed to get Pulumi project: {str(e)}") from e

    logger.info("Deployment prerequisites validated successfully")
    return True


def log_deployment_summary(
    resources_created: int = 0,
    resources_updated: int = 0,
    resources_deleted: int = 0,
) -> None:
    """
    Log a summary of deployment changes.

    Args:
        resources_created: Number of resources created
        resources_updated: Number of resources updated
        resources_deleted: Number of resources deleted
    """
    summary = (
        f"Deployment summary: "
        f"Created={resources_created}, Updated={resources_updated}, Deleted={resources_deleted}"
    )
    logger.info(summary)
