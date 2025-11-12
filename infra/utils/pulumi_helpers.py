"""Common Pulumi utilities for resource patterns and output handling."""

import logging
import traceback
from typing import Any, Callable, Optional, TypeVar

import pulumi

logger = logging.getLogger(__name__)

T = TypeVar("T")


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
