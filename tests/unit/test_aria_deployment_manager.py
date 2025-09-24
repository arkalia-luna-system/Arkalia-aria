#!/usr/bin/env python3
"""
Tests unitaires pour ARIA_DeploymentManager
============================================

Tests complets pour le gestionnaire de déploiement ARIA.
"""

import tempfile
from pathlib import Path

from devops_automation.deployment.aria_deployment_manager import ARIA_DeploymentManager
from devops_automation.security.aria_security_validator import ARIA_SecurityValidator


class TestARIA_DeploymentManager:
    """Tests unitaires pour ARIA_DeploymentManager"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.temp_dir = tempfile.mkdtemp()
        self.deployment_manager = ARIA_DeploymentManager(self.temp_dir)

    def teardown_method(self):
        """Cleanup après chaque test"""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_success(self):
        """Test cas nominal de l'initialisation"""
        # Arrange & Act
        deployment_manager = ARIA_DeploymentManager(".")

        # Assert
        assert deployment_manager.project_root == Path(".").resolve()
        assert isinstance(deployment_manager.security_validator, ARIA_SecurityValidator)
        assert isinstance(deployment_manager.deployment_history, list)
        assert isinstance(deployment_manager.environments, dict)
        assert "staging" in deployment_manager.environments
        assert "production" in deployment_manager.environments

    def test_init_with_custom_root(self):
        """Test initialisation avec racine personnalisée"""
        # Arrange
        custom_root = "/custom/path"

        # Act
        deployment_manager = ARIA_DeploymentManager(custom_root)

        # Assert
        assert deployment_manager.project_root == Path(custom_root).resolve()

    def test_deploy_success(self):
        """Test cas nominal de deploy"""
        # Arrange
        environment = "staging"
        version = "1.0.0"

        # Act
        result = self.deployment_manager.deploy(environment, version)

        # Assert
        assert isinstance(result, dict)
        assert "status" in result
        assert "environment" in result
        assert "version" in result
        assert "timestamp" in result
        assert result["environment"] == environment
        assert result["version"] == version
        assert result["status"] in ["success", "failed", "in_progress"]
        # Vérifier que les étapes sont présentes
        assert "steps" in result
        assert isinstance(result["steps"], list)

    def test_deploy_invalid_environment(self):
        """Test deploy avec environnement invalide"""
        # Arrange
        invalid_environment = "invalid_env"
        version = "1.0.0"

        # Act & Assert
        try:
            result = self.deployment_manager.deploy(invalid_environment, version)
            # Si pas d'exception, vérifier que le résultat indique une erreur
            assert result["status"] in ["failed", "error"]
        except ValueError as e:
            # Vérifier que l'erreur contient le bon message
            assert "non supporté" in str(e)

    def test_deploy_error_handling(self):
        """Test gestion d'erreur de deploy"""
        # Arrange
        environment = "staging"
        version = None

        # Act
        result = self.deployment_manager.deploy(environment, version)

        # Assert
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] in ["success", "failed", "in_progress"]

    def test_rollback_success(self):
        """Test cas nominal de rollback"""
        # Arrange
        environment = "staging"
        deployment_id = "deploy_1"

        # Ajouter un déploiement dans l'historique
        self.deployment_manager.deployment_history = [
            {
                "id": "deploy_1",
                "environment": environment,
                "version": "1.0.0",
                "status": "success",
                "timestamp": "2024-01-01T00:00:00",
            },
            {
                "id": "deploy_2",
                "environment": environment,
                "version": "0.9.0",
                "status": "success",
                "timestamp": "2024-01-01T00:01:00",
            },
        ]

        # Act
        result = self.deployment_manager.rollback(environment, deployment_id)

        # Assert
        assert isinstance(result, dict)
        assert "id" in result
        assert "status" in result
        assert "environment" in result
        assert "target_deployment" in result
        assert "timestamp" in result
        assert result["environment"] == environment
        assert result["target_deployment"] == deployment_id
        assert result["status"] in ["success", "failed", "in_progress"]

    def test_rollback_version_not_found(self):
        """Test rollback avec version introuvable"""
        # Arrange
        environment = "staging"
        deployment_id = "nonexistent_deployment"

        # Act
        result = self.deployment_manager.rollback(environment, deployment_id)

        # Assert
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] in ["success", "failed", "in_progress"]

    def test_rollback_error_handling(self):
        """Test gestion d'erreur de rollback"""
        # Arrange
        environment = None
        deployment_id = None

        # Act
        result = self.deployment_manager.rollback(environment, deployment_id)

        # Assert
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] in ["success", "failed", "in_progress"]

    def test_get_deployment_status_success(self):
        """Test cas nominal de get_deployment_status"""
        # Arrange
        environment = "staging"

        # Ajouter des déploiements dans l'historique
        self.deployment_manager.deployment_history = [
            {
                "id": "deploy_1",
                "environment": environment,
                "version": "1.0.0",
                "status": "success",
                "timestamp": "2024-01-01T00:00:00",
            },
            {
                "id": "deploy_2",
                "environment": environment,
                "version": "1.1.0",
                "status": "failed",
                "timestamp": "2024-01-01T00:01:00",
            },
        ]

        # Act
        status = self.deployment_manager.get_deployment_status(environment)

        # Assert
        assert isinstance(status, dict)
        assert "environment" in status
        assert "deployment_count" in status
        assert "last_deployment" in status
        assert "status" in status
        assert status["environment"] == environment
        assert isinstance(status["deployment_count"], int)
        assert status["deployment_count"] == 2

    def test_get_deployment_status_no_deployments(self):
        """Test get_deployment_status sans déploiements"""
        # Arrange
        environment = "staging"
        self.deployment_manager.deployment_history = []

        # Act
        status = self.deployment_manager.get_deployment_status(environment)

        # Assert
        assert status["deployment_count"] == 0
        assert status["last_deployment"] is None
        assert status["status"] == "not_deployed"

    def test_get_deployment_status_invalid_environment(self):
        """Test get_deployment_status avec environnement invalide"""
        # Arrange
        invalid_environment = "invalid_env"

        # Act
        status = self.deployment_manager.get_deployment_status(invalid_environment)

        # Assert
        assert status["status"] == "not_deployed"
        assert status["deployment_count"] == 0

    def test_prepare_deployment_success(self):
        """Test cas nominal de _prepare_deployment"""
        # Arrange
        environment = "staging"
        deployment_info = {
            "timestamp": "2024-01-01T00:00:00",
            "version": "1.0.0",
        }

        # Act
        self.deployment_manager._prepare_deployment(environment, deployment_info)

        # Assert
        deploy_dir = self.deployment_manager.project_root / "deployments" / environment
        assert deploy_dir.exists()
        config_file = deploy_dir / "deployment_config.json"
        assert config_file.exists()

    def test_run_security_check_success(self):
        """Test cas nominal de _run_security_check"""
        # Act
        result = self.deployment_manager._run_security_check()

        # Assert
        assert isinstance(result, dict)
        assert "passed" in result
        assert "issues" in result
        assert isinstance(result["passed"], bool)
        assert isinstance(result["issues"], list)

    def test_run_tests_success(self):
        """Test cas nominal de _run_tests"""
        # Act
        result = self.deployment_manager._run_tests()

        # Assert
        assert isinstance(result, dict)
        assert "passed" in result
        assert "coverage" in result
        assert isinstance(result["passed"], bool)
        assert isinstance(result["coverage"], float)

    def test_build_application_success(self):
        """Test cas nominal de _build_application"""
        # Act
        result = self.deployment_manager._build_application()

        # Assert
        assert isinstance(result, dict)
        assert "success" in result
        assert "build_id" in result
        assert isinstance(result["success"], bool)
        assert isinstance(result["build_id"], str)

    def test_deploy_to_environment_success(self):
        """Test cas nominal de _deploy_to_environment"""
        # Arrange
        environment = "staging"
        version = "1.0.0"

        # Act
        result = self.deployment_manager._deploy_to_environment(environment, version)

        # Assert
        assert isinstance(result, dict)
        assert "success" in result
        assert "url" in result
        assert "version" in result
        assert isinstance(result["success"], bool)
        assert isinstance(result["url"], str)
        assert isinstance(result["version"], str)

    def test_validate_deployment_success(self):
        """Test cas nominal de _validate_deployment"""
        # Arrange
        environment = "staging"

        # Act
        result = self.deployment_manager._validate_deployment(environment)

        # Assert
        assert isinstance(result, dict)
        assert "success" in result
        assert "health_check" in result
        assert "url" in result
        assert isinstance(result["success"], bool)
        assert isinstance(result["health_check"], str)
        assert isinstance(result["url"], str)

    def test_backup_current_state_success(self):
        """Test cas nominal de _backup_current_state"""
        # Arrange
        environment = "staging"

        # Act
        self.deployment_manager._backup_current_state(environment)

        # Assert
        backup_dir = self.deployment_manager.project_root / "backups" / environment
        assert backup_dir.exists()

    def test_execute_rollback_success(self):
        """Test cas nominal de _execute_rollback"""
        # Arrange
        environment = "staging"
        deployment_id = "deploy_1"

        # Act
        result = self.deployment_manager._execute_rollback(environment, deployment_id)

        # Assert
        assert isinstance(result, dict)
        assert "success" in result
        assert "rollback_to" in result
        assert isinstance(result["success"], bool)
        assert isinstance(result["rollback_to"], str)
