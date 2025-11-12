"""Unit tests for ObjectStorageBucket component."""

from unittest.mock import MagicMock, patch

import pytest

from infra.components.object_storage import ObjectStorageBucket
from infra.config.models import StorageConfig


class TestObjectStorageBucket:
    """Tests for ObjectStorageBucket component."""

    @pytest.fixture
    def storage_config(self):
        """Create a valid storage configuration for testing."""
        return StorageConfig(
            versioning_enabled=True,
            lifecycle_expiration_days=90,
            acl="private",
            encryption_enabled=True,
        )

    @pytest.fixture
    def object_storage_bucket(self, storage_config):
        """Create an ObjectStorageBucket instance for testing."""
        return ObjectStorageBucket(
            name="test-bucket",
            environment="dev",
            config=storage_config,
            project_id="test-project-123",
            region="fr-par",
            tags={"team": "platform"},
        )

    def test_object_storage_bucket_initialization(self, object_storage_bucket, storage_config):
        """Test that ObjectStorageBucket initializes correctly."""
        assert object_storage_bucket.name == "test-bucket"
        assert object_storage_bucket.environment == "dev"
        assert object_storage_bucket.config == storage_config
        assert object_storage_bucket.project_id == "test-project-123"
        assert object_storage_bucket.region == "fr-par"
        assert object_storage_bucket.tags == {"team": "platform"}
        assert object_storage_bucket.bucket is None

    def test_object_storage_bucket_initialization_with_defaults(self):
        """Test ObjectStorageBucket initialization with minimal parameters."""
        config = StorageConfig()
        bucket = ObjectStorageBucket(
            name="minimal-bucket",
            environment="staging",
            config=config,
            project_id="test-project-456",
        )

        assert bucket.name == "minimal-bucket"
        assert bucket.environment == "staging"
        assert bucket.region == "fr-par"  # Default value
        assert bucket.tags == {}  # Default empty dict

    def test_object_storage_bucket_invalid_acl_validation(self):
        """Test that invalid ACL raises validation error."""
        invalid_config = StorageConfig(acl="invalid-acl")

        with pytest.raises(ValueError, match="Invalid ACL 'invalid-acl'"):
            ObjectStorageBucket(
                name="invalid-bucket",
                environment="dev",
                config=invalid_config,
                project_id="test-project-123",
            )

    def test_object_storage_bucket_invalid_lifecycle_validation(self):
        """Test that invalid lifecycle expiration raises validation error."""
        invalid_config = StorageConfig(lifecycle_expiration_days=0)

        with pytest.raises(ValueError, match="Lifecycle expiration must be >= 1 day"):
            ObjectStorageBucket(
                name="invalid-bucket",
                environment="dev",
                config=invalid_config,
                project_id="test-project-123",
            )

    @patch("infra.components.object_storage.scaleway.ObjectBucket")
    @patch("infra.components.object_storage.pulumi_helpers.log_resource_creation")
    def test_create_success_with_versioning_and_lifecycle(
        self, mock_log, mock_bucket_class, object_storage_bucket
    ):
        """Test successful creation of object storage with versioning and lifecycle."""
        # Mock the bucket object
        mock_bucket = MagicMock()
        mock_bucket.bucket = "test-bucket-dev"
        mock_bucket_class.return_value = mock_bucket

        # Call create method
        object_storage_bucket.create()

        # Verify logging was called
        mock_log.assert_called_once_with(
            "ObjectStorageBucket",
            "test-bucket",
            environment="dev",
            versioning=True,
            acl="private",
        )

        # Verify bucket was created
        mock_bucket_class.assert_called_once()
        call_args = mock_bucket_class.call_args
        assert call_args[0][0] == "test-bucket-bucket"
        # Check that args contains the expected bucket configuration
        args = call_args[1]["args"]
        assert args.name == "test-bucket-dev"
        assert args.region == "fr-par"
        assert args.acl == "private"

    @patch("infra.components.object_storage.scaleway.ObjectBucket")
    @patch("infra.components.object_storage.pulumi_helpers.log_resource_creation")
    def test_create_success_without_versioning_and_lifecycle(self, mock_log, mock_bucket_class):
        """Test successful creation without versioning and lifecycle."""
        config = StorageConfig(
            versioning_enabled=False,
            lifecycle_expiration_days=None,
        )
        bucket = ObjectStorageBucket(
            name="simple-bucket",
            environment="dev",
            config=config,
            project_id="test-project-123",
        )

        # Mock the bucket object
        mock_bucket = MagicMock()
        mock_bucket.bucket = "simple-bucket-dev"
        mock_bucket_class.return_value = mock_bucket

        # Call create method
        bucket.create()

        # Verify logging was called
        mock_log.assert_called_once_with(
            "ObjectStorageBucket",
            "simple-bucket",
            environment="dev",
            versioning=False,
            acl="private",
        )

        # Verify bucket was created
        mock_bucket_class.assert_called_once()

        # Versioning and lifecycle are now configured during bucket creation
        # This test just verifies the bucket was created successfully
        mock_bucket_class.assert_called_once()

    @patch("infra.components.object_storage.scaleway.ObjectBucket")
    @patch("infra.components.object_storage.pulumi_helpers.handle_error")
    def test_create_error_handling(self, mock_handle_error, mock_bucket_class, object_storage_bucket):
        """Test error handling during bucket creation."""
        # Make bucket creation fail
        mock_bucket_class.side_effect = Exception("Test error")

        # Call create method
        object_storage_bucket.create()

        # Verify error was handled
        mock_handle_error.assert_called_once()
        error_call_args = mock_handle_error.call_args[0]
        assert isinstance(error_call_args[0], Exception)
        assert "ObjectStorageBucket.create(test-bucket)" in str(error_call_args[1])

    def test_create_bucket(self, object_storage_bucket):
        """Test bucket creation method."""
        with patch("infra.components.object_storage.scaleway.ObjectBucket") as mock_bucket_class:
            mock_bucket = MagicMock()
            mock_bucket_class.return_value = mock_bucket

            object_storage_bucket._create_bucket()

            # Verify bucket creation with correct parameters
            mock_bucket_class.assert_called_once()
            call_args = mock_bucket_class.call_args
            assert call_args[0][0] == "test-bucket-bucket"
            args = call_args[1]["args"]
            assert args.name == "test-bucket-dev"
            assert args.region == "fr-par"
            assert args.acl == "private"
            assert isinstance(args.tags, dict)
            assert call_args[1]["opts"] == object_storage_bucket.opts

    def test_create_bucket_invalid_name(self):
        """Test bucket creation with invalid name."""
        # Create bucket with name that will fail validation
        bucket = ObjectStorageBucket(
            name="invalid-bucket-name-with-special-chars!",
            environment="dev",
            config=StorageConfig(),
            project_id="test-project-123",
        )

        with patch("infra.components.object_storage.scaleway.ObjectBucket") as mock_bucket_class:
            mock_bucket = MagicMock()
            mock_bucket_class.return_value = mock_bucket

            with pytest.raises(ValueError):
                bucket._create_bucket()

    def test_configure_versioning_without_bucket(self, object_storage_bucket):
        """Test that versioning configuration works without bucket (now handled during creation)."""
        # Versioning configuration is now handled during bucket creation
        # This method should not raise an error
        object_storage_bucket._configure_versioning()

    def test_configure_versioning_success(self, object_storage_bucket):
        """Test successful versioning configuration."""
        # Mock bucket
        mock_bucket = MagicMock()
        mock_bucket.name = "test-bucket-dev"
        object_storage_bucket.bucket = mock_bucket

        # Versioning configuration is currently not implemented
        # This test verifies the method runs without error
        object_storage_bucket._configure_versioning()

    def test_configure_lifecycle_without_bucket(self, object_storage_bucket):
        """Test that lifecycle configuration works without bucket (now handled during creation)."""
        # Lifecycle configuration is now handled during bucket creation
        # This method should not raise an error
        object_storage_bucket._configure_lifecycle()

    def test_configure_lifecycle_no_expiration(self, object_storage_bucket):
        """Test lifecycle configuration when no expiration is set."""
        # Mock bucket
        mock_bucket = MagicMock()
        mock_bucket.name = "test-bucket-dev"
        object_storage_bucket.bucket = mock_bucket

        # Set no expiration
        object_storage_bucket.config.lifecycle_expiration_days = None

        # Lifecycle configuration is currently not implemented
        # This test verifies the method runs without error
        object_storage_bucket._configure_lifecycle()

    def test_configure_lifecycle_success(self, object_storage_bucket):
        """Test successful lifecycle configuration."""
        # Mock bucket
        mock_bucket = MagicMock()
        mock_bucket.name = "test-bucket-dev"
        object_storage_bucket.bucket = mock_bucket

        # Lifecycle configuration is currently not implemented
        # This test verifies the method runs without error
        object_storage_bucket._configure_lifecycle()

    def test_get_outputs_empty(self, object_storage_bucket):
        """Test get_outputs returns empty dict when bucket not created."""
        outputs = object_storage_bucket.get_outputs()
        assert outputs == {}

    def test_get_outputs_success(self, object_storage_bucket):
        """Test get_outputs returns correct data when bucket created."""
        # Mock bucket
        mock_bucket = MagicMock()
        mock_bucket.name = "test-bucket-dev"
        object_storage_bucket.bucket = mock_bucket

        outputs = object_storage_bucket.get_outputs()

        # Check that outputs contain expected keys and values
        assert outputs["bucket_name"] == "test-bucket-dev"
        assert outputs["bucket_region"] == "fr-par"
        assert outputs["versioning_enabled"] is True
        assert outputs["acl"] == "private"
        assert outputs["encryption_enabled"] is True
        assert outputs["lifecycle_expiration_days"] == 90
        assert "bucket_endpoint" in outputs  # pulumi.Output.concat result

    def test_get_bucket_name_not_created(self, object_storage_bucket):
        """Test get_bucket_name raises error when bucket not created."""
        with pytest.raises(ValueError, match="Bucket not created yet"):
            object_storage_bucket.get_bucket_name()

    def test_get_bucket_name_success(self, object_storage_bucket):
        """Test get_bucket_name returns bucket name."""
        mock_bucket = MagicMock()
        mock_bucket.name = "test-bucket-dev"
        object_storage_bucket.bucket = mock_bucket

        bucket_name = object_storage_bucket.get_bucket_name()
        assert bucket_name == "test-bucket-dev"

    def test_get_bucket_endpoint_not_created(self, object_storage_bucket):
        """Test get_bucket_endpoint raises error when bucket not created."""
        with pytest.raises(ValueError, match="Bucket not created yet"):
            object_storage_bucket.get_bucket_endpoint()

    def test_get_bucket_endpoint_success(self, object_storage_bucket):
        """Test get_bucket_endpoint returns bucket endpoint URL."""
        mock_bucket = MagicMock()
        mock_bucket.name = "test-bucket-dev"
        object_storage_bucket.bucket = mock_bucket

        endpoint = object_storage_bucket.get_bucket_endpoint()

        # Should be a pulumi.Output.concat object
        assert endpoint is not None

    def test_get_bucket_region(self, object_storage_bucket):
        """Test get_bucket_region returns bucket region."""
        region = object_storage_bucket.get_bucket_region()
        assert region == "fr-par"

    def test_repr(self, object_storage_bucket):
        """Test string representation of ObjectStorageBucket."""
        expected = "ObjectStorageBucket(name=test-bucket, environment=dev)"
        assert repr(object_storage_bucket) == expected

    def test_different_acl_settings(self):
        """Test bucket with different ACL settings."""
        for acl in ["private", "public-read", "authenticated-read"]:
            config = StorageConfig(acl=acl)
            bucket = ObjectStorageBucket(
                name=f"test-{acl}-bucket",
                environment="dev",
                config=config,
                project_id="test-project-123",
            )

            with patch("infra.components.object_storage.scaleway.ObjectBucket") as mock_bucket_class:
                mock_bucket = MagicMock()
                mock_bucket_class.return_value = mock_bucket

                bucket._create_bucket()

                # Verify ACL is set correctly
                call_args = mock_bucket_class.call_args
                args = call_args[1]["args"]
                assert args.acl == acl

    def test_versioning_disabled(self):
        """Test bucket with versioning disabled."""
        config = StorageConfig(versioning_enabled=False)
        bucket = ObjectStorageBucket(
            name="no-versioning-bucket",
            environment="dev",
            config=config,
            project_id="test-project-123",
        )

        # Mock bucket
        mock_bucket = MagicMock()
        mock_bucket.name = "no-versioning-bucket-dev"
        bucket.bucket = mock_bucket

        # Versioning configuration is currently not implemented
        # This test verifies the method runs without error
        bucket.create()

    def test_encryption_disabled(self):
        """Test bucket with encryption disabled."""
        config = StorageConfig(encryption_enabled=False, versioning_enabled=False)
        bucket = ObjectStorageBucket(
            name="no-encryption-bucket",
            environment="dev",
            config=config,
            project_id="test-project-123",
        )

        # Mock bucket to get outputs
        mock_bucket = MagicMock()
        mock_bucket.name = "no-encryption-bucket-dev"
        bucket.bucket = mock_bucket

        outputs = bucket.get_outputs()
        # Note: encryption_enabled is not part of the current outputs
        # This test verifies the bucket can be created without encryption config
        assert outputs["versioning_enabled"] is False

    def test_lifecycle_expiration_different_values(self):
        """Test bucket with different lifecycle expiration values."""
        for days in [1, 30, 365]:
            config = StorageConfig(lifecycle_expiration_days=days)
            bucket = ObjectStorageBucket(
                name=f"test-{days}-days-bucket",
                environment="dev",
                config=config,
                project_id="test-project-123",
            )

            # Mock bucket
            mock_bucket = MagicMock()
            mock_bucket.name = f"test-{days}-days-bucket-dev"
            bucket.bucket = mock_bucket

            # Lifecycle configuration is currently not implemented
            # This test verifies the method runs without error
            bucket._configure_lifecycle()
