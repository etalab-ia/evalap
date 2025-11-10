"""Base component structure for infrastructure components."""

from abc import ABC, abstractmethod
from typing import Any, Optional

import pulumi


class BaseComponent(ABC):
    """Abstract base class for all infrastructure components."""

    def __init__(
        self,
        name: str,
        environment: str,
        tags: Optional[dict[str, str]] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        """
        Initialize base component.

        Args:
            name: Component name
            environment: Environment (dev, staging, production)
            tags: Optional tags for resources
            opts: Optional Pulumi resource options
        """
        self.name = name
        self.environment = environment
        self.tags = tags or {}
        self.opts = opts or pulumi.ResourceOptions()
        self.outputs = {}

    @abstractmethod
    def create(self) -> None:
        """Create the infrastructure component. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def get_outputs(self) -> dict[str, Any]:
        """
        Get component outputs.

        Returns:
            dict: Dictionary of component outputs
        """
        pass

    def export_outputs(self, prefix: str = "") -> None:
        """
        Export component outputs to Pulumi stack.

        Args:
            prefix: Optional prefix for output names
        """
        outputs = self.get_outputs()
        for key, value in outputs.items():
            output_name = f"{prefix}_{key}" if prefix else key
            pulumi.export(output_name, value)

    def add_tag(self, key: str, value: str) -> None:
        """
        Add a tag to the component.

        Args:
            key: Tag key
            value: Tag value
        """
        self.tags[key] = value

    def get_tags(self) -> dict[str, str]:
        """
        Get all tags for the component.

        Returns:
            dict: Tags dictionary
        """
        return self.tags.copy()

    def __repr__(self) -> str:
        """String representation of component."""
        return f"{self.__class__.__name__}(name={self.name}, environment={self.environment})"
