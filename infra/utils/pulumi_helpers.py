"""Common Pulumi utilities for resource patterns and output handling."""

import logging
from typing import Any, Optional

import pulumi

logger = logging.getLogger(__name__)


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
    """
    error_msg = f"Error in {context}: {str(error)}" if context else f"Error: {str(error)}"
    logger.error(error_msg)
    raise error
