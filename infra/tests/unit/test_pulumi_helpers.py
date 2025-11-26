"""Unit tests for Pulumi helper utilities."""

import json
from unittest.mock import MagicMock, patch

import pytest

from infra.utils.pulumi_helpers import (
    AuditEvent,
    AuditLogger,
    AuditOperation,
    AuditSeverity,
    apply_with_logging,
    combine_outputs,
    configure_audit_logging,
    create_resource_name,
    create_tags,
    export_output,
    get_audit_logger,
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


# =============================================================================
# Audit Logging Tests
# =============================================================================


class TestAuditOperation:
    """Tests for AuditOperation enum."""

    def test_audit_operation_values(self):
        """Test that all expected operations are defined."""
        assert AuditOperation.CREATE.value == "create"
        assert AuditOperation.UPDATE.value == "update"
        assert AuditOperation.DELETE.value == "delete"
        assert AuditOperation.DEPLOY.value == "deploy"
        assert AuditOperation.PREVIEW.value == "preview"
        assert AuditOperation.REFRESH.value == "refresh"
        assert AuditOperation.DESTROY.value == "destroy"


class TestAuditSeverity:
    """Tests for AuditSeverity enum."""

    def test_audit_severity_values(self):
        """Test that all expected severities are defined."""
        assert AuditSeverity.INFO.value == "info"
        assert AuditSeverity.WARNING.value == "warning"
        assert AuditSeverity.ERROR.value == "error"
        assert AuditSeverity.CRITICAL.value == "critical"


class TestAuditEvent:
    """Tests for AuditEvent dataclass."""

    def test_audit_event_creation(self):
        """Test creating an audit event with required fields."""
        event = AuditEvent(
            timestamp="2024-01-15T10:30:00Z",
            operation="create",
            resource_type="DatabaseInstance",
            resource_name="evalap-db-dev",
            stack="dev",
            project="evalap",
            environment="dev",
        )
        assert event.timestamp == "2024-01-15T10:30:00Z"
        assert event.operation == "create"
        assert event.resource_type == "DatabaseInstance"
        assert event.resource_name == "evalap-db-dev"
        assert event.stack == "dev"
        assert event.project == "evalap"
        assert event.environment == "dev"
        assert event.severity == "info"  # Default
        assert event.success is True  # Default
        assert event.error_message is None  # Default
        assert event.duration_ms is None  # Default

    def test_audit_event_to_dict(self):
        """Test converting audit event to dictionary."""
        event = AuditEvent(
            timestamp="2024-01-15T10:30:00Z",
            operation="create",
            resource_type="Container",
            resource_name="api-container",
            stack="staging",
            project="evalap",
            environment="staging",
            details={"cpu": "1000m", "memory": "1024MB"},
        )
        result = event.to_dict()
        assert isinstance(result, dict)
        assert result["timestamp"] == "2024-01-15T10:30:00Z"
        assert result["operation"] == "create"
        assert result["details"] == {"cpu": "1000m", "memory": "1024MB"}

    def test_audit_event_to_json(self):
        """Test converting audit event to JSON string."""
        event = AuditEvent(
            timestamp="2024-01-15T10:30:00Z",
            operation="delete",
            resource_type="ObjectBucket",
            resource_name="storage-bucket",
            stack="dev",
            project="evalap",
            environment="dev",
            severity="warning",
        )
        json_str = event.to_json()
        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert parsed["operation"] == "delete"
        assert parsed["severity"] == "warning"

    def test_audit_event_with_error(self):
        """Test audit event with error details."""
        event = AuditEvent(
            timestamp="2024-01-15T10:30:00Z",
            operation="create",
            resource_type="DatabaseInstance",
            resource_name="evalap-db",
            stack="prod",
            project="evalap",
            environment="production",
            severity="error",
            success=False,
            error_message="Connection timeout",
            duration_ms=5000,
        )
        assert event.success is False
        assert event.error_message == "Connection timeout"
        assert event.duration_ms == 5000


class TestAuditLogger:
    """Tests for AuditLogger class."""

    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    @patch("infra.utils.pulumi_helpers.pulumi.get_project")
    def test_audit_logger_initialization(self, mock_project, mock_stack):
        """Test AuditLogger initialization."""
        mock_stack.return_value = "dev"
        mock_project.return_value = "evalap"

        audit_log = AuditLogger(environment="dev")
        assert audit_log.environment == "dev"
        assert audit_log._start_times == {}

    @patch("infra.utils.pulumi_helpers.audit_logger")
    @patch("infra.utils.pulumi_helpers.logger")
    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    @patch("infra.utils.pulumi_helpers.pulumi.get_project")
    def test_log_create(self, mock_project, mock_stack, mock_logger, mock_audit_logger):
        """Test logging a create operation."""
        mock_stack.return_value = "dev"
        mock_project.return_value = "evalap"

        audit_log = AuditLogger(environment="dev")
        audit_log.log_create(
            resource_type="DatabaseInstance",
            resource_name="evalap-db",
            details={"engine": "PostgreSQL-15"},
        )

        mock_audit_logger.info.assert_called_once()
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]
        assert "AUDIT" in call_args
        assert "Created" in call_args
        assert "DatabaseInstance" in call_args

    @patch("infra.utils.pulumi_helpers.audit_logger")
    @patch("infra.utils.pulumi_helpers.logger")
    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    @patch("infra.utils.pulumi_helpers.pulumi.get_project")
    def test_log_update(self, mock_project, mock_stack, mock_logger, mock_audit_logger):
        """Test logging an update operation."""
        mock_stack.return_value = "staging"
        mock_project.return_value = "evalap"

        audit_log = AuditLogger(environment="staging")
        audit_log.log_update(
            resource_type="Container",
            resource_name="api-container",
            changes={"cpu": "2000m"},
        )

        mock_audit_logger.info.assert_called_once()
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]
        assert "Updated" in call_args

    @patch("infra.utils.pulumi_helpers.audit_logger")
    @patch("infra.utils.pulumi_helpers.logger")
    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    @patch("infra.utils.pulumi_helpers.pulumi.get_project")
    def test_log_delete(self, mock_project, mock_stack, mock_logger, mock_audit_logger):
        """Test logging a delete operation."""
        mock_stack.return_value = "dev"
        mock_project.return_value = "evalap"

        audit_log = AuditLogger(environment="dev")
        audit_log.log_delete(
            resource_type="ObjectBucket",
            resource_name="old-bucket",
            reason="Cleanup",
        )

        mock_audit_logger.warning.assert_called_once()
        mock_logger.warning.assert_called_once()
        call_args = mock_logger.warning.call_args[0][0]
        assert "Deleted" in call_args

    @patch("infra.utils.pulumi_helpers.audit_logger")
    @patch("infra.utils.pulumi_helpers.logger")
    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    @patch("infra.utils.pulumi_helpers.pulumi.get_project")
    def test_log_error(self, mock_project, mock_stack, mock_logger, mock_audit_logger):
        """Test logging an error."""
        mock_stack.return_value = "prod"
        mock_project.return_value = "evalap"

        audit_log = AuditLogger(environment="production")
        error = ValueError("Invalid configuration")
        audit_log.log_error(
            resource_type="DatabaseInstance",
            resource_name="evalap-db",
            operation=AuditOperation.CREATE,
            error=error,
        )

        mock_audit_logger.error.assert_called_once()
        mock_logger.error.assert_called_once()
        call_args = mock_logger.error.call_args[0][0]
        assert "Failed" in call_args
        assert "Invalid configuration" in call_args

    @patch("infra.utils.pulumi_helpers.audit_logger")
    @patch("infra.utils.pulumi_helpers.logger")
    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    @patch("infra.utils.pulumi_helpers.pulumi.get_project")
    def test_log_deployment_start(self, mock_project, mock_stack, mock_logger, mock_audit_logger):
        """Test logging deployment start."""
        mock_stack.return_value = "staging"
        mock_project.return_value = "evalap"

        audit_log = AuditLogger(environment="staging")
        audit_log.log_deployment_start(
            stack_name="staging",
            resources=["database", "container", "storage"],
        )

        mock_audit_logger.info.assert_called_once()
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]
        assert "Starting deployment" in call_args

    @patch("infra.utils.pulumi_helpers.audit_logger")
    @patch("infra.utils.pulumi_helpers.logger")
    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    @patch("infra.utils.pulumi_helpers.pulumi.get_project")
    def test_log_deployment_complete(self, mock_project, mock_stack, mock_logger, mock_audit_logger):
        """Test logging deployment completion."""
        mock_stack.return_value = "staging"
        mock_project.return_value = "evalap"

        audit_log = AuditLogger(environment="staging")
        audit_log.log_deployment_complete(
            stack_name="staging",
            resources_created=3,
            resources_updated=1,
            resources_deleted=0,
        )

        mock_audit_logger.info.assert_called_once()
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]
        assert "Deployment complete" in call_args
        assert "created=3" in call_args

    @patch("infra.utils.pulumi_helpers.audit_logger")
    @patch("infra.utils.pulumi_helpers.logger")
    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    @patch("infra.utils.pulumi_helpers.pulumi.get_project")
    def test_log_deployment_failed(self, mock_project, mock_stack, mock_logger, mock_audit_logger):
        """Test logging deployment failure."""
        mock_stack.return_value = "prod"
        mock_project.return_value = "evalap"

        audit_log = AuditLogger(environment="production")
        error = RuntimeError("Deployment timeout")
        audit_log.log_deployment_failed(
            stack_name="prod",
            error=error,
            partial_resources={"created": 2, "failed": 1},
        )

        mock_audit_logger.critical.assert_called_once()
        mock_logger.critical.assert_called_once()
        call_args = mock_logger.critical.call_args[0][0]
        assert "FAILED" in call_args

    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    @patch("infra.utils.pulumi_helpers.pulumi.get_project")
    def test_duration_tracking(self, mock_project, mock_stack):
        """Test operation duration tracking."""
        mock_stack.return_value = "dev"
        mock_project.return_value = "evalap"

        audit_log = AuditLogger(environment="dev")

        # Start operation
        audit_log.start_operation("DatabaseInstance", "evalap-db")
        assert "DatabaseInstance:evalap-db" in audit_log._start_times

        # Get duration (should remove from tracking)
        duration = audit_log._get_duration_ms("DatabaseInstance", "evalap-db")
        assert duration is not None
        assert duration >= 0
        assert "DatabaseInstance:evalap-db" not in audit_log._start_times

    @patch("infra.utils.pulumi_helpers.pulumi.get_stack")
    @patch("infra.utils.pulumi_helpers.pulumi.get_project")
    def test_duration_tracking_no_start(self, mock_project, mock_stack):
        """Test duration tracking when operation was not started."""
        mock_stack.return_value = "dev"
        mock_project.return_value = "evalap"

        audit_log = AuditLogger(environment="dev")
        duration = audit_log._get_duration_ms("Container", "api")
        assert duration is None


class TestGetAuditLogger:
    """Tests for get_audit_logger function."""

    @patch("infra.utils.pulumi_helpers._audit_logger_instance", None)
    @patch("infra.utils.pulumi_helpers.os.environ.get")
    def test_get_audit_logger_creates_instance(self, mock_env_get):
        """Test that get_audit_logger creates a new instance."""
        mock_env_get.return_value = "dev"
        audit_log = get_audit_logger()
        assert isinstance(audit_log, AuditLogger)
        assert audit_log.environment == "dev"

    @patch("infra.utils.pulumi_helpers._audit_logger_instance", None)
    def test_get_audit_logger_with_environment(self):
        """Test get_audit_logger with explicit environment."""
        audit_log = get_audit_logger(environment="production")
        assert audit_log.environment == "production"


class TestConfigureAuditLogging:
    """Tests for configure_audit_logging function."""

    @patch("infra.utils.pulumi_helpers.audit_logger")
    def test_configure_audit_logging_default(self, mock_audit_logger):
        """Test configuring audit logging with defaults."""
        mock_audit_logger.handlers = []
        configure_audit_logging()
        mock_audit_logger.setLevel.assert_called()

    @patch("infra.utils.pulumi_helpers.audit_logger")
    def test_configure_audit_logging_with_file(self, mock_audit_logger):
        """Test configuring audit logging with file output."""
        import tempfile

        mock_audit_logger.handlers = []
        with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
            configure_audit_logging(log_file=f.name)
        mock_audit_logger.setLevel.assert_called()
        # File handler should be added
        assert mock_audit_logger.addHandler.call_count >= 1
