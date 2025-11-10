"""Unit tests for Pulumi helper utilities."""

from unittest.mock import MagicMock, patch

import pytest

from infra.utils.pulumi_helpers import (
    apply_with_logging,
    combine_outputs,
    create_resource_name,
    create_tags,
    export_output,
    get_output_value,
    handle_error,
    log_resource_creation,
)


class TestCreateResourceName:
    """Tests for create_resource_name function."""

    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    def test_create_resource_name_basic(self, mock_get_stack):
        """Test basic resource name creation."""
        mock_get_stack.return_value = "dev"
        name = create_resource_name("api")
        assert name == "api-dev"

    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    def test_create_resource_name_with_suffix(self, mock_get_stack):
        """Test resource name creation with suffix."""
        mock_get_stack.return_value = "prod"
        name = create_resource_name("database", suffix="primary")
        assert name == "database-prod-primary"

    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    def test_create_resource_name_lowercase_and_dash(self, mock_get_stack):
        """Test that resource names are lowercased and underscores converted to dashes."""
        mock_get_stack.return_value = "staging"
        name = create_resource_name("My_Service")
        assert name == "my-service-staging"
        assert "_" not in name  # Underscores are converted to dashes

    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    def test_create_resource_name_empty_suffix(self, mock_get_stack):
        """Test that empty suffix is ignored."""
        mock_get_stack.return_value = "dev"
        name = create_resource_name("service", suffix="")
        assert name == "service-dev"


class TestExportOutput:
    """Tests for export_output function."""

    @patch("infra.utils.pulumi_helpers.pulumi.export")
    @patch("infra.utils.pulumi_helpers.logger")
    def test_export_output_with_description(self, mock_logger, mock_export):
        """Test exporting output with description."""
        export_output("endpoint", "http://example.com", "API endpoint")
        mock_export.assert_called_once_with("endpoint", "http://example.com")
        mock_logger.info.assert_called_once()

    @patch("infra.utils.pulumi_helpers.pulumi.export")
    @patch("infra.utils.pulumi_helpers.logger")
    def test_export_output_without_description(self, mock_logger, mock_export):
        """Test exporting output without description."""
        export_output("bucket_name", "my-bucket")
        mock_export.assert_called_once_with("bucket_name", "my-bucket")
        mock_logger.info.assert_called_once()


class TestGetOutputValue:
    """Tests for get_output_value function."""

    def test_get_output_value(self):
        """Test getting value from Pulumi output."""
        mock_output = MagicMock()
        mock_future = MagicMock()
        mock_future.result.return_value = "test_value"
        mock_output.get_future.return_value = mock_future

        result = get_output_value(mock_output)
        assert result == "test_value"
        mock_output.get_future.assert_called_once()


class TestApplyWithLogging:
    """Tests for apply_with_logging function."""

    @patch("infra.utils.pulumi_helpers.logger")
    def test_apply_with_logging_with_message(self, mock_logger):
        """Test applying function with logging message."""
        mock_output = MagicMock()
        mock_output.apply.return_value = "result"

        def test_func(x):
            return x.upper()

        apply_with_logging(mock_output, test_func, "Processing output")
        mock_logger.debug.assert_called_once_with("Processing output")
        mock_output.apply.assert_called_once_with(test_func)

    @patch("infra.utils.pulumi_helpers.logger")
    def test_apply_with_logging_without_message(self, mock_logger):
        """Test applying function without logging message."""
        mock_output = MagicMock()
        mock_output.apply.return_value = "result"

        def test_func(x):
            return x.upper()

        apply_with_logging(mock_output, test_func)
        mock_logger.debug.assert_not_called()
        mock_output.apply.assert_called_once_with(test_func)


class TestCombineOutputs:
    """Tests for combine_outputs function."""

    @patch("infra.utils.pulumi_helpers.pulumi.Output.all")
    def test_combine_outputs(self, mock_all):
        """Test combining multiple outputs."""
        mock_output1 = MagicMock()
        mock_output2 = MagicMock()
        mock_output3 = MagicMock()
        mock_all.return_value = "combined"

        combined = combine_outputs(mock_output1, mock_output2, mock_output3)
        mock_all.assert_called_once_with(mock_output1, mock_output2, mock_output3)
        assert combined == "combined"

    @patch("infra.utils.pulumi_helpers.pulumi.Output.all")
    def test_combine_outputs_single(self, mock_all):
        """Test combining single output."""
        mock_output = MagicMock()
        mock_all.return_value = "combined"

        combined = combine_outputs(mock_output)
        mock_all.assert_called_once_with(mock_output)
        assert combined == "combined"


class TestCreateTags:
    """Tests for create_tags function."""

    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    def test_create_tags_basic(self, mock_get_stack):
        """Test creating basic tags."""
        mock_get_stack.return_value = "dev"
        tags = create_tags("dev", "api")

        assert tags["Environment"] == "dev"
        assert tags["Component"] == "api"
        assert tags["ManagedBy"] == "Pulumi"
        assert tags["Stack"] == "dev"

    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    def test_create_tags_with_additional(self, mock_get_stack):
        """Test creating tags with additional tags."""
        mock_get_stack.return_value = "staging"
        additional = {"team": "platform", "cost-center": "engineering"}
        tags = create_tags("staging", "database", additional_tags=additional)

        assert tags["Environment"] == "staging"
        assert tags["Component"] == "database"
        assert tags["team"] == "platform"
        assert tags["cost-center"] == "engineering"

    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    def test_create_tags_no_additional(self, mock_get_stack):
        """Test creating tags without additional tags."""
        mock_get_stack.return_value = "prod"
        tags = create_tags("prod", "storage", additional_tags=None)

        assert len(tags) == 4  # Only standard tags
        assert "team" not in tags


class TestLogResourceCreation:
    """Tests for log_resource_creation function."""

    @patch("infra.utils.pulumi_helpers.logger")
    def test_log_resource_creation_with_details(self, mock_logger):
        """Test logging resource creation with details."""
        log_resource_creation(
            "Container",
            "api-container",
            cpu="1000m",
            memory="1024MB",
            port="8080",
        )
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]
        assert "Container" in call_args
        assert "api-container" in call_args
        assert "cpu=1000m" in call_args

    @patch("infra.utils.pulumi_helpers.logger")
    def test_log_resource_creation_no_details(self, mock_logger):
        """Test logging resource creation without details."""
        log_resource_creation("Database", "postgres-db")
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]
        assert "Database" in call_args
        assert "postgres-db" in call_args


class TestHandleError:
    """Tests for handle_error function."""

    @patch("infra.utils.pulumi_helpers.logger")
    def test_handle_error_with_context(self, mock_logger):
        """Test error handling with context."""
        error = ValueError("Test error")
        with pytest.raises(ValueError):
            handle_error(error, context="deployment")
        mock_logger.error.assert_called_once()
        call_args = mock_logger.error.call_args[0][0]
        assert "deployment" in call_args
        assert "Test error" in call_args

    @patch("infra.utils.pulumi_helpers.logger")
    def test_handle_error_without_context(self, mock_logger):
        """Test error handling without context."""
        error = RuntimeError("Runtime error")
        with pytest.raises(RuntimeError):
            handle_error(error)
        mock_logger.error.assert_called_once()
        call_args = mock_logger.error.call_args[0][0]
        assert "Runtime error" in call_args

    @patch("infra.utils.pulumi_helpers.logger")
    def test_handle_error_reraises(self, mock_logger):
        """Test that handle_error re-raises the exception."""
        error = Exception("Original error")
        with pytest.raises(Exception) as exc_info:
            handle_error(error)
        assert exc_info.value is error
