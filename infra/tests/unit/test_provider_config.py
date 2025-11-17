"""Unit tests for Scaleway provider configuration."""

import os
from unittest.mock import MagicMock, patch

import pytest

from infra.config.provider import get_provider_config, validate_provider_config


class TestGetProviderConfig:
    """Tests for get_provider_config function."""

    @patch("infra.config.provider.pulumi.Config")
    @patch.dict(
        os.environ,
        {
            "SCW_ACCESS_KEY": "test-access-key",
            "SCW_SECRET_KEY": "test-secret-key",
            "SCW_PROJECT_ID": "test-project-id",
            "SCW_REGION": "fr-par",
        },
    )
    def test_get_provider_config_from_env(self, mock_config_class):
        """Test loading provider configuration from environment variables."""
        mock_config = MagicMock()
        mock_config.get.return_value = None
        mock_config.get_secret.return_value = None
        mock_config_class.return_value = mock_config

        config = get_provider_config()

        assert config["access_key"] == "test-access-key"
        assert config["secret_key"] == "test-secret-key"
        assert config["project_id"] == "test-project-id"
        assert config["region"] == "fr-par"

    @patch("infra.config.provider.pulumi.Config")
    @patch.dict(
        os.environ,
        {
            "SCW_ACCESS_KEY": "test-access-key",
            "SCW_SECRET_KEY": "test-secret-key",
            "SCW_PROJECT_ID": "test-project-id",
        },
    )
    def test_get_provider_config_default_region(self, mock_config_class):
        """Test that default region is used when not specified."""
        mock_config = MagicMock()
        mock_config.get.return_value = None
        mock_config.get_secret.return_value = None
        mock_config_class.return_value = mock_config

        config = get_provider_config()

        assert config["region"] == "fr-par"  # Default region

    @patch("infra.config.provider.pulumi.Config")
    @patch.dict(
        os.environ,
        {
            "SCW_ACCESS_KEY": "test-access-key",
            "SCW_SECRET_KEY": "test-secret-key",
            "SCW_PROJECT_ID": "test-project-id",
            "SCW_REGION": "nl-ams",
        },
    )
    def test_get_provider_config_custom_region(self, mock_config_class):
        """Test loading provider configuration with custom region."""
        mock_config = MagicMock()
        mock_config.get.return_value = None
        mock_config.get_secret.return_value = None
        mock_config_class.return_value = mock_config

        config = get_provider_config()

        assert config["region"] == "nl-ams"

    @patch("infra.config.provider.pulumi.Config")
    @patch.dict(
        os.environ,
        {
            "SCW_ACCESS_KEY": "test-access-key",
            "SCW_SECRET_KEY": "test-secret-key",
            "SCW_PROJECT_ID": "test-project-id",
            "SCW_REGION": "fr-par",
        },
    )
    def test_get_provider_config_returns_dict(self, mock_config_class):
        """Test that provider configuration returns a dictionary."""
        mock_config = MagicMock()
        mock_config.get.return_value = None
        mock_config.get_secret.return_value = None
        mock_config_class.return_value = mock_config

        config = get_provider_config()

        assert isinstance(config, dict)
        assert "access_key" in config
        assert "secret_key" in config
        assert "project_id" in config
        assert "region" in config

    @patch("infra.config.provider.pulumi.Config")
    def test_get_provider_config_from_pulumi_config(self, mock_config_class):
        """Test loading provider configuration from Pulumi config."""
        mock_config = MagicMock()
        mock_config.get.side_effect = lambda key: {
            "scaleway:region": "nl-ams",
        }.get(key)
        mock_config.get_secret.side_effect = lambda key: {
            "scaleway:access_key": "pulumi-access-key",
            "scaleway:secret_key": "pulumi-secret-key",
        }.get(key)
        mock_config_class.return_value = mock_config

        with patch.dict(
            os.environ,
            {
                "SCW_PROJECT_ID": "test-project-id",
            },
        ):
            config = get_provider_config()

            assert config["region"] == "nl-ams"
            assert config["access_key"] == "pulumi-access-key"
            assert config["secret_key"] == "pulumi-secret-key"


class TestValidateProviderConfig:
    """Tests for validate_provider_config function."""

    def test_validate_provider_config_valid(self):
        """Test validation of valid provider configuration."""
        config = {
            "region": "fr-par",
            "project_id": "test-project-id",
            "access_key": "test-access-key",
            "secret_key": "test-secret-key",
        }

        assert validate_provider_config(config) is True

    def test_validate_provider_config_missing_region(self):
        """Test validation fails when region is missing."""
        config = {
            "project_id": "test-project-id",
            "access_key": "test-access-key",
            "secret_key": "test-secret-key",
        }

        with pytest.raises(ValueError) as exc_info:
            validate_provider_config(config)
        assert "region" in str(exc_info.value)

    def test_validate_provider_config_missing_project_id(self):
        """Test validation fails when project_id is missing."""
        config = {
            "region": "fr-par",
            "access_key": "test-access-key",
            "secret_key": "test-secret-key",
        }

        with pytest.raises(ValueError) as exc_info:
            validate_provider_config(config)
        assert "project_id" in str(exc_info.value)

    def test_validate_provider_config_missing_access_key(self):
        """Test validation fails when access_key is missing."""
        config = {
            "region": "fr-par",
            "project_id": "test-project-id",
            "secret_key": "test-secret-key",
        }

        with pytest.raises(ValueError) as exc_info:
            validate_provider_config(config)
        assert "access_key" in str(exc_info.value)

    def test_validate_provider_config_missing_secret_key(self):
        """Test validation fails when secret_key is missing."""
        config = {
            "region": "fr-par",
            "project_id": "test-project-id",
            "access_key": "test-access-key",
        }

        with pytest.raises(ValueError) as exc_info:
            validate_provider_config(config)
        assert "secret_key" in str(exc_info.value)

    def test_validate_provider_config_empty_values(self):
        """Test validation fails when values are empty."""
        config = {
            "region": "",
            "project_id": "test-project-id",
            "access_key": "test-access-key",
            "secret_key": "test-secret-key",
        }

        with pytest.raises(ValueError):
            validate_provider_config(config)

    def test_validate_provider_config_none_values(self):
        """Test validation fails when values are None."""
        config = {
            "region": "fr-par",
            "project_id": None,
            "access_key": "test-access-key",
            "secret_key": "test-secret-key",
        }

        with pytest.raises(ValueError):
            validate_provider_config(config)
